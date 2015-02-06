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
import urllib2
import xml.etree.ElementTree as etree

import six

from proliantutils.ilo import exception
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
            req = urllib2.Request(url=urlstr, data=xml)
            req.add_header("Content-length", len(xml))
            data = urllib2.urlopen(req).read()
        except (ValueError, urllib2.URLError, urllib2.HTTPError) as e:
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
            xml = '\r\n'.join(etree.tostringlist(root)) + '\r\n'
        else:
            xml = etree.tostring(root) + '\r\n'
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
                if 'syntax error' or 'Feature not supported' in msg:
                    for cmd in BOOT_MODE_CMDS:
                        if cmd in msg:
                            msg = "%s not supported on this platform." % cmd
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
                device_list += nic_list
            if dev == 'HDD':
                disk_list = self._get_disk_boot_devices(result)
                device_list += disk_list

        if device_list:
            self.set_persistent_boot(device_list)

    def _check_boot_mode(self, result):

        if 'DESCRIPTION' in result[0]:
            return 'uefi'
        else:
            return 'bios'

    def _get_nic_boot_devices(self, result):
        nw_identifier = "NIC"
        pxe_enabled = "PXE"
        nic_list = []
        pxe_nic_list = []
        try:
            for item in result:
                if nw_identifier in item["DESCRIPTION"]:
                    # Check if it is PXE enabled, to add it to starting of list
                    if pxe_enabled in item["DESCRIPTION"]:
                        pxe_nic_list.append(item["value"])
                    else:
                        nic_list.append(item["value"])
        except KeyError as e:
            msg = "_get_nic_boot_devices failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        all_nics = pxe_nic_list + nic_list
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
