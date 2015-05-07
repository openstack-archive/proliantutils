# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""Provides iLO management interface. Talks to the iLO management engine
over RIBCL scripting language
"""

import re
import xml.etree.ElementTree as etree

from oslo_utils import strutils
import six
from six.moves.urllib import error as urllib_error
from six.moves.urllib import request

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import operations


POWER_STATE = {
    'ON': 'Yes',
    'OFF': 'No',
}

BOOT_MODE_CMDS = [
    'GET_CURRENT_BOOT_MODE',
    'GET_PENDING_BOOT_MODE',
    'GET_SUPPORTED_BOOT_MODE',
    'SET_PENDING_BOOT_MODE'
]


class RIBCLOperations(operations.IloOperations):
    """iLO class for RIBCL interface for iLO.

    Implements the base class using RIBCL scripting language to talk
    to the iLO.
    """
    def __init__(self, host, login, password, timeout=60, port=443):
        self.host = host
        self.login = login
        self.password = password
        self.timeout = timeout
        self.port = port

    def _request_ilo(self, root):
        """Send RIBCL XML data to iLO.

        This function sends the XML request to the ILO and
        receives the output from ILO.

        :raises: IloConnectionError() if unable to send the request.
        """
        if self.port:
            urlstr = 'https://%s:%d/ribcl' % (self.host, self.port)
        else:
            urlstr = 'https://%s/ribcl' % (self.host)
        xml = self._serialize_xml(root)
        try:
            req = request.Request(url=urlstr, data=xml.encode('ascii'))
            req.add_header("Content-length", len(xml))
            data = request.urlopen(req).read()
        except (ValueError, urllib_error.URLError,
                urllib_error.HTTPError) as e:
            raise exception.IloConnectionError(e)
        return data

    def _create_dynamic_xml(self, cmdname, tag_name, mode, subelements=None):
        """Create RIBCL XML to send to iLO.

        This function creates the dynamic xml required to be sent
        to the ILO for all the APIs.

        :param cmdname: the API which needs to be implemented.
        :param tag_name: the tag info under which ILO has defined
                         the particular API.
        :param mode: 'read' or 'write'
        :param subelements: dictionary containing subelements of the
                            particular API tree.
        :returns: the etree.Element for the root of the RIBCL XML
        """
        root = etree.Element('RIBCL', VERSION="2.0")
        login = etree.SubElement(
            root, 'LOGIN', USER_LOGIN=self.login, PASSWORD=self.password)
        tagname = etree.SubElement(login, tag_name, MODE=mode)
        subelements = subelements or {}

        etree.SubElement(tagname, cmdname)

        if six.PY2:
            root_iterator = root.getiterator(cmdname)
        else:
            root_iterator = root.iter(cmdname)

        for cmd in root_iterator:
            for key, value in subelements.items():
                cmd.set(key, value)

        return root

    def _serialize_xml(self, root):
        """Serialize XML data into string

        It serializes the dynamic xml created and converts
        it to a string. This is done before sending the
        xml to the ILO.

        :param root: root of the dynamic xml.
        """
        if hasattr(etree, 'tostringlist'):
            if six.PY3:
                xml_content_list = [
                    x.decode("utf-8") for x in etree.tostringlist(root)]
            else:
                xml_content_list = etree.tostringlist(root)

            xml = '\r\n'.join(xml_content_list) + '\r\n'
        else:
            if six.PY3:
                xml_content = etree.tostring(root).decode("utf-8")
            else:
                xml_content = etree.tostring(root)
            xml = xml_content + '\r\n'
        return xml

    def _parse_output(self, xml_response):
        """Parse the response XML from iLO.

        This function parses the output received from ILO.
        As the output contains multiple XMLs, it extracts
        one xml at a time and loops over till all the xmls
        in the response are exhausted.

        It returns the data to APIs either in dictionary
        format or as the string.
        It creates the dictionary only if the Ilo response
        contains the data under the requested RIBCL command.
        If the Ilo response contains only the string,
        then the string is returned back.
        """
        count = 0
        xml_dict = {}
        resp_message = None
        xml_start_pos = []
        for m in re.finditer(r"\<\?xml", xml_response):
            xml_start_pos.append(m.start())
        while count < len(xml_start_pos):
            if (count == len(xml_start_pos) - 1):
                result = xml_response[xml_start_pos[count]:]
            else:
                start = xml_start_pos[count]
                end = xml_start_pos[count + 1]
                result = xml_response[start:end]
            result = result.strip()
            message = etree.fromstring(result)
            resp = self._validate_message(message)
            if hasattr(resp, 'tag'):
                xml_dict = self._elementtree_to_dict(resp)
            elif resp is not None:
                resp_message = resp
            count = count + 1

        if xml_dict:
            return xml_dict
        elif resp_message is not None:
            return resp_message

    def _elementtree_to_dict(self, element):
        """Convert XML elementtree to dictionary.

        Converts the actual response from the ILO for an API
        to the dictionary.
        """
        node = dict()
        text = getattr(element, 'text')
        if text is not None:
            text = text.strip()
            if len(text) != 0:
                node['text'] = text
        node.update(element.items())  # element's attributes
        child_nodes = {}
        for child in element:  # element's children
            child_nodes.setdefault(child.tag, []).append(
                self._elementtree_to_dict(child))
        # convert all single-element lists into non-lists
        for key, value in child_nodes.items():
            if len(value) == 1:
                child_nodes[key] = value[0]
        node.update(child_nodes.items())
        return node

    def _validate_message(self, message):
        """Validate XML response from iLO.

        This function validates the XML response to see
        if the exit status is 0 or not in the response.
        If the status is non-zero it raises exception.
        """
        if message.tag != 'RIBCL':
            # the true case shall be unreachable for response
            # XML from Ilo as all messages are tagged with RIBCL
            # but still raise an exception if any invalid
            # XML response is returned by Ilo. Set status to some
            # arbitary non-zero value.
            status = -1
            raise exception.IloClientInternalError(message, status)

        for child in message:
            if child.tag != 'RESPONSE':
                return message
            status = int(child.get('STATUS'), 16)
            msg = child.get('MESSAGE')
            if status == 0 and msg != 'No error':
                return msg
            if status != 0:
                if 'syntax error' in msg or 'Feature not supported' in msg:
                    for cmd in BOOT_MODE_CMDS:
                        if cmd in msg:
                            platform = self.get_product_name()
                            msg = ("%(cmd)s is not supported on %(platform)s" %
                                   {'cmd': cmd, 'platform': platform})
                            raise (exception.IloCommandNotSupportedError
                                   (msg, status))
                    else:
                        raise exception.IloClientInternalError(msg, status)
                if (status in exception.IloLoginFailError.statuses or
                        msg in exception.IloLoginFailError.messages):
                    raise exception.IloLoginFailError(msg, status)
                raise exception.IloError(msg, status)

    def _execute_command(self, create_command, tag_info, mode, dic={}):
        """Execute a command on the iLO.

        Common infrastructure used by all APIs to send/get
        response from ILO.
        """
        xml = self._create_dynamic_xml(
            create_command, tag_info, mode, dic)
        d = self._request_ilo(xml)
        data = self._parse_output(d)
        return data

    def get_all_licenses(self):
        """Retrieve license type, key, installation date, etc."""
        data = self._execute_command('GET_ALL_LICENSES', 'RIB_INFO', 'read')
        d = {}
        for key, val in data['GET_ALL_LICENSES']['LICENSE'].items():
            if isinstance(val, dict):
                d[key] = data['GET_ALL_LICENSES']['LICENSE'][key]['VALUE']
        return d

    def get_product_name(self):
        """Get the model name of the queried server."""
        data = self._execute_command(
            'GET_PRODUCT_NAME', 'SERVER_INFO', 'read')

        return data['GET_PRODUCT_NAME']['PRODUCT_NAME']['VALUE']

    def get_host_power_status(self):
        """Request the power state of the server."""
        data = self._execute_command(
            'GET_HOST_POWER_STATUS', 'SERVER_INFO', 'read')
        return data['GET_HOST_POWER']['HOST_POWER']

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot."""
        data = self._execute_command(
            'GET_ONE_TIME_BOOT', 'SERVER_INFO', 'read')
        return data['ONE_TIME_BOOT']['BOOT_TYPE']['VALUE']

    def get_vm_status(self, device='FLOPPY'):
        """Returns the virtual media drive status."""
        dic = {'DEVICE': device.upper()}
        data = self._execute_command(
            'GET_VM_STATUS', 'RIB_INFO', 'read', dic)
        return data['GET_VM_STATUS']

    def reset_server(self):
        """Resets the server."""
        data = self._execute_command('RESET_SERVER', 'SERVER_INFO', 'write')
        return data

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button."""
        data = self._execute_command('PRESS_PWR_BTN', 'SERVER_INFO', 'write')
        return data

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button."""
        dic = {'TOGGLE': 'NO'}
        data = self._execute_command(
            'HOLD_PWR_BTN', 'SERVER_INFO', 'write', dic)
        return data

    def set_host_power(self, power):
        """Toggle the power button of server.

        :param power: 'ON' or 'OFF'
        """
        if power.upper() in POWER_STATE:
            dic = {'HOST_POWER': POWER_STATE[power.upper()]}
            data = self._execute_command(
                'SET_HOST_POWER', 'SERVER_INFO', 'write', dic)
            return data
        else:
            raise exception.IloInvalidInputError(
                "Invalid input. The expected input is ON or OFF.")

    def set_one_time_boot(self, value):
        """Configures a single boot from a specific device."""
        dic = {'value': value}
        data = self._execute_command(
            'SET_ONE_TIME_BOOT', 'SERVER_INFO', 'write', dic)
        return data

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image."""
        dic = {
            'DEVICE': device.upper(),
            'IMAGE_URL': url,
        }
        data = self._execute_command(
            'INSERT_VIRTUAL_MEDIA', 'RIB_INFO', 'write', dic)
        return data

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted."""
        dic = {'DEVICE': device.upper()}
        data = self._execute_command(
            'EJECT_VIRTUAL_MEDIA', 'RIB_INFO', 'write', dic)
        return data

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status

        It also allows the boot options for booting from the virtual media.
        """
        dic = {'DEVICE': device.upper()}
        xml = self._create_dynamic_xml(
            'SET_VM_STATUS', 'RIB_INFO', 'write', dic)

        if six.PY2:
            child_iterator = xml.getiterator()
        else:
            child_iterator = xml.iter()

        for child in child_iterator:
            if child.tag == 'SET_VM_STATUS':
                etree.SubElement(child, 'VM_BOOT_OPTION',
                                 VALUE=boot_option.upper())
                etree.SubElement(child, 'VM_WRITE_PROTECT',
                                 VALUE=write_protect.upper())

        d = self._request_ilo(xml)
        data = self._parse_output(d)
        return data

    def get_current_boot_mode(self):
        """Retrieves the current boot mode settings."""
        data = self._execute_command(
            'GET_CURRENT_BOOT_MODE', 'SERVER_INFO', 'read')
        return data['GET_CURRENT_BOOT_MODE']['BOOT_MODE']['VALUE']

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode settings."""
        data = self._execute_command(
            'GET_PENDING_BOOT_MODE', 'SERVER_INFO', 'read')
        return data['GET_PENDING_BOOT_MODE']['BOOT_MODE']['VALUE']

    def get_supported_boot_mode(self):
        """Retrieves the supported boot mode."""
        data = self._execute_command(
            'GET_SUPPORTED_BOOT_MODE', 'SERVER_INFO', 'read')
        return data['GET_SUPPORTED_BOOT_MODE']['SUPPORTED_BOOT_MODE']['VALUE']

    def set_pending_boot_mode(self, value):
        """Configures the boot mode of the system from a specific boot mode."""
        dic = {'value': value}
        data = self._execute_command(
            'SET_PENDING_BOOT_MODE', 'SERVER_INFO', 'write', dic)
        return data

    def get_persistent_boot(self):
        """Retrieves the current boot mode settings."""
        data = self._execute_command(
            'GET_PERSISTENT_BOOT', 'SERVER_INFO', 'read')
        if data is not None:
            return data['PERSISTENT_BOOT']['DEVICE']

    def get_persistent_boot_device(self):
        """Get the current persistent boot device set for the host."""
        result = self.get_persistent_boot()
        boot_mode = self._check_boot_mode(result)

        if boot_mode == 'bios':
            return result[0]['value']

        value = result[0]['DESCRIPTION']
        if 'HP iLO Virtual USB CD' in value:
            return 'CDROM'

        elif 'NIC' in value or 'PXE' in value:
            return 'NETWORK'

        elif self._isDisk(value):
            return 'HDD'

        else:
            return None

    def set_persistent_boot(self, values=[]):
        """Configures a boot from a specific device."""

        xml = self._create_dynamic_xml(
            'SET_PERSISTENT_BOOT', 'SERVER_INFO', 'write')

        if six.PY2:
            child_iterator = xml.getiterator()
        else:
            child_iterator = xml.iter()

        for child in child_iterator:
            for val in values:
                if child.tag == 'SET_PERSISTENT_BOOT':
                    etree.SubElement(child, 'DEVICE', VALUE=val)
        d = self._request_ilo(xml)
        data = self._parse_output(d)
        return data

    def update_persistent_boot(self, device_type=[]):

        valid_devices = ['NETWORK',
                         'HDD',
                         'CDROM']

        # Check if the input is valid
        for item in device_type:
            if item.upper() not in valid_devices:
                raise exception.IloInvalidInputError(
                    "Invalid input. Valid devices: NETWORK, HDD or CDROM.")

        result = self.get_persistent_boot()
        boot_mode = self._check_boot_mode(result)
        if boot_mode == 'bios':
            self.set_persistent_boot(device_type)
            return

        device_list = []
        for item in device_type:
            dev = item.upper()
            if dev == 'NETWORK':
                nic_list = self._get_nic_boot_devices(result)
                device_list.extend(nic_list)
            if dev == 'HDD':
                disk_list = self._get_disk_boot_devices(result)
                device_list.extend(disk_list)
            if dev == 'CDROM':
                virtual_list = self._get_virtual_boot_devices(result)
                device_list.extend(virtual_list)

        if not device_list:
            platform = self.get_product_name()
            msg = ("\'%(device)s\' is not configured as boot device on "
                   "this system of type %(platform)s."
                   % {'device': device_type[0], 'platform': platform})
            raise (exception.IloInvalidInputError(msg))

        self.set_persistent_boot(device_list)

    def _check_boot_mode(self, result):

        if 'DESCRIPTION' in result[0]:
            return 'uefi'
        else:
            return 'bios'

    def _get_nic_boot_devices(self, result):
        nw_identifier = "NIC"
        pxe_enabled = "PXE"
        iscsi_identifier = "iSCSI"
        nic_list = []
        pxe_nic_list = []
        iscsi_nic_list = []
        try:
            for item in result:
                if pxe_enabled in item["DESCRIPTION"]:
                    pxe_nic_list.append(item["value"])
                elif iscsi_identifier in item["DESCRIPTION"]:
                    iscsi_nic_list.append(item["value"])
                elif nw_identifier in item["DESCRIPTION"]:
                    nic_list.append(item["value"])
        except KeyError as e:
            msg = "_get_nic_boot_devices failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        all_nics = pxe_nic_list + nic_list + iscsi_nic_list
        return all_nics

    def _isDisk(self, result):
        disk_identifier = ["Logical Drive", "HDD", "Storage", "LogVol"]
        return any(e in result for e in disk_identifier)

    def _get_disk_boot_devices(self, result):
        disk_list = []
        try:
            for item in result:
                if self._isDisk(item["DESCRIPTION"]):
                    disk_list.append(item["value"])
        except KeyError as e:
            msg = "_get_disk_boot_devices failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        return disk_list

    def _request_host(self):
        """Request host info from the server."""
        urlstr = 'http://%s/xmldata?item=all' % (self.host)
        try:
            req = request.Request(url=urlstr)
            xml = request.urlopen(req).read()
        except (ValueError, urllib_error.URLError,
                urllib_error.HTTPError) as e:
            raise IloConnectionError(e)

        return xml

    def get_host_uuid(self):
        """Request host UUID of the server.

        :returns: the host UUID of the server
        :raises: IloConnectionError if failed connecting to the iLO.
        """
        xml = self._request_host()
        root = etree.fromstring(xml)
        data = self._elementtree_to_dict(root)
        return data['HSI']['SPN']['text'], data['HSI']['cUUID']['text']

    def get_host_health_data(self, data=None):
        """Request host health data of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the embedded health data.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        if not data or data and "GET_EMBEDDED_HEALTH_DATA" not in data:
            data = self._execute_command(
                'GET_EMBEDDED_HEALTH', 'SERVER_INFO', 'read')
        return data

    def get_host_health_present_power_reading(self, data=None):
        """Request the power consumption of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self.get_host_health_data(data)
        return (data['GET_EMBEDDED_HEALTH_DATA']['POWER_SUPPLIES']
                    ['POWER_SUPPLY_SUMMARY']
                    ['PRESENT_POWER_READING']['VALUE'])

    def get_host_health_power_supplies(self, data=None):
        """Request the health power supply information.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power supply information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self.get_host_health_data(data)
        d = (data['GET_EMBEDDED_HEALTH_DATA']['POWER_SUPPLIES']['SUPPLY'])
        if not isinstance(d, list):
            d = [d]
        return d

    def get_host_health_temperature_sensors(self, data=None):
        """Get the health Temp Sensor report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the temperature sensors
            information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self.get_host_health_data(data)
        d = data['GET_EMBEDDED_HEALTH_DATA']['TEMPERATURE']['TEMP']
        if not isinstance(d, list):
            d = [d]
        return d

    def get_host_health_fan_sensors(self, data=None):
        """Get the health Fan Sensor Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the fan sensor information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self.get_host_health_data(data)
        d = data['GET_EMBEDDED_HEALTH_DATA']['FANS']['FAN']
        if not isinstance(d, list):
            d = [d]
        return d

    def get_host_health_at_a_glance(self, data=None):
        """Get the health at a glance Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the health at a glance information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self.get_host_health_data(data)
        return data['GET_EMBEDDED_HEALTH_DATA']['HEALTH_AT_A_GLANCE']

    def get_host_power_readings(self):
        """Retrieves the host power readings.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        data = self._execute_command(
            'GET_POWER_READINGS', 'SERVER_INFO', 'read')
        return data['GET_POWER_READINGS']

    def reset_ilo(self):
        """Resets the iLO.

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        """
        self._execute_command('RESET_RIB', 'RIB_INFO', 'write')
        # Check if iLO is up again after reset.
        common.wait_for_ilo_after_reset(self)

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        """

        dic = {'USER_LOGIN': self.login}
        root = self._create_dynamic_xml(
            'MOD_USER', 'USER_INFO', 'write', dic)

        element = root.find('LOGIN/USER_INFO/MOD_USER')
        etree.SubElement(element, 'PASSWORD', VALUE=password)
        d = self._request_ilo(root)
        self._parse_output(d)

    def _get_virtual_boot_devices(self, result):
        virtual_list = []
        dev_desc = "HP iLO Virtual USB CD"
        try:
            for item in result:
                if dev_desc in item["DESCRIPTION"]:
                    virtual_list.append(item["value"])
        except KeyError as e:
            msg = "_get_virtual_boot_devices failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        return virtual_list

    def get_essential_properties(self):
        """Gets essential scheduling properties as required by ironic

        :returns: a dictionary of server properties like memory size,
                  disk size, number of cpus, cpu arch, port numbers
                  and mac addresses.
        :raises:IloError if iLO returns an error in command execution.

        """

        data = self.get_host_health_data()
        properties = {}
        properties['memory_mb'] = self._parse_memory_embedded_health(data)
        cpus, cpu_arch = self._parse_processor_embedded_health(data)
        properties['cpus'] = cpus
        properties['cpu_arch'] = cpu_arch
        properties['local_gb'] = self._parse_storage_embedded_health(data)
        macs = self._parse_nics_embedded_health(data)
        return_value = {'properties': properties, 'macs': macs}
        return return_value

    def _get_server_boot_modes(self):
        """Gets boot modes supported by the server

        :returns: a dictionary of supported boot modes or None.
        :raises:IloError, if iLO returns an error in command execution.
        """
        bootmode = self.get_supported_boot_mode()
        if bootmode == 'LEGACY_ONLY':
            BootMode = ['LEGACY']
        elif bootmode == 'LEGACY_UEFI':
            BootMode = ['LEGACY', 'UEFI']
        elif bootmode == 'UEFI_ONLY':
            BootMode = ['UEFI']
        else:
            BootMode = None
        return {'BootMode': BootMode}

    def get_server_capabilities(self):
        """Gets server properties which can be used for scheduling

        :returns: a dictionary of hardware properties like firmware
                  versions, server model.
        :raises: IloError, if iLO returns an error in command execution.
        """

        # Commenting out the BootMode as we dont plan to add it for Kilo.
        # BootMode = self._get_server_boot_modes()
        capabilities = {}
        data = self.get_host_health_data()
        capabilities.update(self._get_ilo_firmware_version(data))
        capabilities.update(self._get_rom_firmware_version(data))
        capabilities.update({'server_model': self.get_product_name()})
        capabilities.update(self._get_number_of_gpu_devices_connected(data))
        return capabilities

    def _parse_memory_embedded_health(self, data):
        """Parse the get_host_health_data() for essential properties

        :param data: the output returned by get_host_health_data()
        :returns: memory size in MB.
        :raises IloError, if unable to get the memory details.

        """
        memory_mb = 0
        try:
            memory = (data['GET_EMBEDDED_HEALTH_DATA']['MEMORY']
                      ['MEMORY_DETAILS_SUMMARY'])
        except KeyError as e:
            msg = "Unable to get memory data. Error: Data missing %s"
            raise exception.IloError((msg) % e)

        # here the value can be either a dictionary or a list.
        # Convert it tolist so that its uniform across servers.
        if not isinstance(memory, list):
            memory = [memory]
        total_memory_size = 0
        for item in memory:
            for val in item.values():
                memsize = val['TOTAL_MEMORY_SIZE']['VALUE']
                if memsize != 'N/A':
                    memory_bytes = (
                        strutils.string_to_bytes(
                            memsize.replace(' ', ''), return_int=True))
                    memory_mb = int(memory_bytes / (1024 * 1024))
                    total_memory_size = total_memory_size + memory_mb
        return total_memory_size

    def _parse_processor_embedded_health(self, data):
        """Parse the get_host_health_data() for essential properties

        :param data: the output returned by get_host_health_data()
        :returns: processor details like cpu arch and number of cpus.

        """
        try:
            processor = (data['GET_EMBEDDED_HEALTH_DATA']
                         ['PROCESSORS']['PROCESSOR'])
        except KeyError as e:
            msg = "Unable to get cpu data. Error: Data missing %s"
            raise exception.IloError((msg) % e)

        # here the value can be either a dictionary or a list.
        # Convert it tolist so that its uniform across servers.
        if not isinstance(processor,  list):
            processor = [processor]
        cpus = len(processor)
        cpu_arch = 'x86_64'
        return cpus, cpu_arch

    def _parse_storage_embedded_health(self, data):
        """Gets the storage data from get_embedded_health

        Parse the get_host_health_data() for essential properties

        :param data: the output returned by get_host_health_data()
        :returns: disk size in GB.

        """
        try:
            s = data['GET_EMBEDDED_HEALTH_DATA']['STORAGE']
            storage = s['CONTROLLER']['LOGICAL_DRIVE']
        except KeyError:
            # We dont raise exception because this dictionary
            # is available only when RAID is configured.
            # If we raise error here then we will always fail
            # inspection where this module is consumed. Hence
            # as a workaround just return 0.
            local_gb = 0
            return local_gb

        local_gb = 0
        minimum = local_gb

        # here the value can be either a dictionary or a list.
        # Convert it to a list so that its uniform across servers.
        if not isinstance(storage, list):
            storage = [storage]

        for item in storage:
            for key, val in item.items():
                if key == 'CAPACITY':
                    capacity = val['VALUE']
                    local_bytes = (strutils.string_to_bytes(
                                   capacity.replace(' ', ''), return_int=True))
                    local_gb = int(local_bytes / (1024 * 1024 * 1024))
                    if minimum >= local_gb or minimum == 0:
                        minimum = local_gb
        return minimum

    def _parse_nics_embedded_health(self, data):
        """Gets the NIC details from get_embedded_health data

         Parse the get_host_health_data() for essential properties

        :param data: the output returned by get_host_health_data()
        :returns: a dictionary of port numbers and their corresponding
                  mac addresses.
        :raises IloError, if unable to get NIC data.

        """
        try:
            nic_data = (data['GET_EMBEDDED_HEALTH_DATA']
                        ['NIC_INFORMATION']['NIC'])
        except KeyError as e:
            msg = "Unable to get NIC details. Data missing %s"
            raise exception.IloError((msg) % e)
        # here the value can be either a dictionary or a list.
        # Convert it tolist so that its uniform across servers.
        if not isinstance(nic_data, list):
            nic_data = [nic_data]
        nic_dict = {}
        for item in nic_data:
            try:
                port = item['NETWORK_PORT']['VALUE']
                mac = item['MAC_ADDRESS']['VALUE']
                location = item['LOCATION']['VALUE']
                if location == 'Embedded':
                    nic_dict[port] = mac
            except KeyError as e:
                msg = "Unable to get NIC details. Data missing %s"
                raise exception.IloError((msg) % e)
        return nic_dict

    def _get_firmware_embedded_health(self, data):
        """Parse the get_host_health_data() for server capabilities

        :param data: the output returned by get_host_health_data()
        :returns: a dictionary of firmware name and firmware version.

        """
        try:
            firmware = data['GET_EMBEDDED_HEALTH_DATA']['FIRMWARE_INFORMATION']
        except KeyError:
            pass

        if not isinstance(firmware, list):
            firmware = [firmware]
        return dict((y['FIRMWARE_NAME']['VALUE'],
                     y['FIRMWARE_VERSION']['VALUE'])
                    for x in firmware for y in x.values())

    def _get_rom_firmware_version(self, data):
        """Gets the rom firmware version for server capabilities

        Parse the get_host_health_data() to retreive the firmware
        details.

        :param data: the output returned by get_host_health_data()
        :returns: a dictionary of rom firmware version.

        """
        firmware_details = self._get_firmware_embedded_health(data)
        rom_firmware_version = firmware_details['HP ProLiant System ROM']
        return {'rom_firmware_version': rom_firmware_version}

    def _get_ilo_firmware_version(self, data):
        """Gets the ilo firmware version for server capabilities

        Parse the get_host_health_data() to retreive the firmware
        details.

        :param data: the output returned by get_host_health_data()
        :returns: a dictionary of iLO firmware version.

        """
        firmware_details = self._get_firmware_embedded_health(data)
        return {'ilo_firmware_version': firmware_details['iLO']}

    def _get_number_of_gpu_devices_connected(self, data):
        """Gets the number of GPU devices connected to the server

        Parse the get_host_health_data() and get the count of
        number of GPU devices connected to the server.

        :param data: the output returned by get_host_health_data()
        :returns: a dictionary of rom firmware version.

        """
        try:
            temp = data['GET_EMBEDDED_HEALTH_DATA']['TEMPERATURE']['TEMP']
        except KeyError:
            pass

        if not isinstance(temp, list):
            temp = [temp]

        count = 0
        for key in temp:
            for name, value in key.items():
                if name == 'LABEL' and 'GPU' in value['VALUE']:
                    count = count + 1

        return {'pci_gpu_devices': count}

# The below block of code is there only for backward-compatibility
# reasons (before commit 47608b6 for ris-support).
IloClient = RIBCLOperations
IloError = exception.IloError
IloClientInternalError = exception.IloClientInternalError
IloCommandNotSupportedError = exception.IloCommandNotSupportedError
IloLoginFailError = exception.IloLoginFailError
IloConnectionError = exception.IloConnectionError
IloInvalidInputError = exception.IloInvalidInputError
