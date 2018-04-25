# Copyright 2017 Hewlett Packard Enterprise Development Company, L.P.
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

__author__ = 'HPE'

import hashlib
import retrying

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import firmware_controller
from proliantutils.ilo import mappings
from proliantutils.ilo import operations
from proliantutils import log
from proliantutils import rest

""" Currently this class supports only secure boot and firmware settings
related API's .

TODO : Add rest of the API's that exists in RIBCL. """

DEVICE_COMMON_TO_RIS = {'NETWORK': 'Pxe',
                        'CDROM': 'Cd',
                        'HDD': 'Hdd',
                        'ISCSI': 'UefiTarget'}
DEVICE_RIS_TO_COMMON = dict(
    (v, k) for (k, v) in DEVICE_COMMON_TO_RIS.items())

POWER_STATE = {
    'ON': 'On',
    'OFF': 'ForceOff',
}

# The PCI standards mention following categories of PCI devices as
# GPU devices.
# Base Class Code 03 indicate VGA devices
# Sub Class Code
#     00h: VGA-compatible controller
#     01h:  XGA controller
#     02h:  3D controller
#     80h:  Other display controller
# RIS data reports the SubclassCode in integer rather than in hexadecimal form.

CLASSCODE_FOR_GPU_DEVICES = [3]
SUBCLASSCODE_FOR_GPU_DEVICES = [0, 1, 2, 128]

MAX_RETRY_ATTEMPTS = 3  # Maximum number of attempts to be retried
MAX_TIME_BEFORE_RETRY = 7 * 1000  # wait time in milliseconds before retry

LOG = log.get_logger(__name__)


class RISOperations(rest.RestConnectorBase, operations.IloOperations):
    """iLO class for RIS interface of iLO.

    Implements the class used for REST based RIS services to talk to the iLO.
    """
    def __init__(self, host, login, password, bios_password=None,
                 cacert=None):
        super(RISOperations, self).__init__(host, login, password,
                                            bios_password=bios_password,
                                            cacert=cacert)

    def _get_collection(self, collection_uri, request_headers=None):
        """Generator function that returns collection members."""

        # get the collection
        status, headers, thecollection = self._rest_get(collection_uri)

        if status != 200:
            msg = self._get_extended_error(thecollection)
            raise exception.IloError(msg)

        while status < 300:
            # verify expected type
            # Don't limit to version 0 here as we will rev to 1.0 at some
            # point hopefully with minimal changes
            ctype = self._get_type(thecollection)
            if (ctype not in ['Collection.0', 'Collection.1']):
                raise exception.IloError("collection not found")

            # if this collection has inline items, return those
            # NOTE:  Collections are very flexible in how the represent
            # members.  They can be inline in the collection as members
            # of the 'Items' array, or they may be href links in the
            # links/Members array.  The could actually be both. Typically,
            # iLO implements the inline (Items) for only when the collection
            # is read only.  We have to render it with the href links when an
            # array contains PATCHable items because its complex to PATCH
            # inline collection members.

            if 'Items' in thecollection:
                # iterate items
                for item in thecollection['Items']:
                    # if the item has a self uri pointer,
                    # supply that for convenience.
                    memberuri = None
                    if 'links' in item and 'self' in item['links']:
                        memberuri = item['links']['self']['href']
                    yield 200, None, item, memberuri

            # else walk the member links
            elif ('links' in thecollection and
                  'Member' in thecollection['links']):
                # iterate members
                for memberuri in thecollection['links']['Member']:
                    # for each member return the resource indicated by the
                    # member link
                    status, headers, member = self._rest_get(memberuri['href'])
                    yield status, headers, member, memberuri['href']

            # page forward if there are more pages in the collection
            if ('links' in thecollection and
                    'NextPage' in thecollection['links']):
                next_link_uri = (collection_uri + '?page=' + str(
                                 thecollection['links']['NextPage']['page']))
                status, headers, thecollection = self._rest_get(next_link_uri)

            # else we are finished iterating the collection
            else:
                break

    def _get_type(self, obj):
        """Return the type of an object."""
        typever = obj['Type']
        typesplit = typever.split('.')
        return typesplit[0] + '.' + typesplit[1]

    def _operation_allowed(self, headers_dict, operation):
        """Checks if specified operation is allowed on the resource."""

        if 'allow' in headers_dict:
            if operation in headers_dict['allow']:
                return True
        return False

    def _render_extended_error_message_list(self, extended_error):
        """Parse the ExtendedError object and retruns the message.

        Build a list of decoded messages from the extended_error using the
        message registries. An ExtendedError JSON object is a response from
        the with its own schema.  This function knows how to parse the
        ExtendedError object and, using any loaded message registries,
        render an array of plain language strings that represent
        the response.
        """
        messages = []
        if isinstance(extended_error, dict):
            if ('Type' in extended_error and
                    extended_error['Type'].startswith('ExtendedError.')):
                for msg in extended_error['Messages']:
                    message_id = msg['MessageID']
                    x = message_id.split('.')
                    registry = x[0]
                    msgkey = x[len(x) - 1]

                    # if the correct message registry is loaded,
                    # do string resolution
                    if (registry in self.message_registries and msgkey in
                            self.message_registries[registry]['Messages']):
                        rmsgs = self.message_registries[registry]['Messages']
                        msg_dict = rmsgs[msgkey]
                        msg_str = message_id + ':  ' + msg_dict['Message']

                        for argn in range(0, msg_dict['NumberOfArgs']):
                            subst = '%' + str(argn+1)
                            m = str(msg['MessageArgs'][argn])
                            msg_str = msg_str.replace(subst, m)

                        if ('Resolution' in msg_dict and
                                msg_dict['Resolution'] != 'None'):
                            msg_str += '  ' + msg_dict['Resolution']

                        messages.append(msg_str)
                    else:
                        # no message registry, simply return the msg object
                        # in string form
                        messages.append(str(message_id))

        return messages

    def _get_extended_error(self, extended_error):
        """Gets the list of decoded messages from the extended_error."""
        return self._render_extended_error_message_list(extended_error)

    def _get_host_details(self):
        """Get the system details."""
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        status, headers, system = self._rest_get('/rest/v1/Systems/1')
        if status < 300:
            stype = self._get_type(system)
            if stype not in ['ComputerSystem.0', 'ComputerSystem.1']:
                msg = "%s is not a valid system type " % stype
                raise exception.IloError(msg)
        else:
            msg = self._get_extended_error(system)
            raise exception.IloError(msg)

        return system

    def _check_bios_resource(self, properties=[]):
        """Check if the bios resource exists."""

        system = self._get_host_details()
        if ('links' in system['Oem']['Hp'] and
                'BIOS' in system['Oem']['Hp']['links']):
            # Get the BIOS URI and Settings
            bios_uri = system['Oem']['Hp']['links']['BIOS']['href']
            status, headers, bios_settings = self._rest_get(bios_uri)

            if status >= 300:
                msg = self._get_extended_error(bios_settings)
                raise exception.IloError(msg)

            # If property is not None, check if the bios_property is supported
            for property in properties:
                if property not in bios_settings:
                    # not supported on this platform
                    msg = ('BIOS Property "' + property + '" is not'
                           ' supported on this system.')
                    raise exception.IloCommandNotSupportedError(msg)

            return headers, bios_uri, bios_settings

        else:
            msg = ('"links/BIOS" section in ComputerSystem/Oem/Hp'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _get_pci_devices(self):
        """Gets the PCI devices.

        :returns: PCI devices list if the pci resource exist.
        :raises: IloCommandNotSupportedError if the PCI resource
            doesn't exist.
        :raises: IloError, on an error from iLO.
        """

        system = self._get_host_details()
        if ('links' in system['Oem']['Hp'] and
                'PCIDevices' in system['Oem']['Hp']['links']):
            # Get the PCI URI and Settings
            pci_uri = system['Oem']['Hp']['links']['PCIDevices']['href']
            status, headers, pci_device_list = self._rest_get(pci_uri)

            if status >= 300:
                msg = self._get_extended_error(pci_device_list)
                raise exception.IloError(msg)

            return pci_device_list

        else:
            msg = ('links/PCIDevices section in ComputerSystem/Oem/Hp'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _get_gpu_pci_devices(self):
        """Returns the list of gpu devices."""
        pci_device_list = self._get_pci_devices()

        gpu_list = []
        items = pci_device_list['Items']
        for item in items:
            if item['ClassCode'] in CLASSCODE_FOR_GPU_DEVICES:
                if item['SubclassCode'] in SUBCLASSCODE_FOR_GPU_DEVICES:
                    gpu_list.append(item)
        return gpu_list

    def _get_storage_resource(self):
        """Gets the SmartStorage resource if exists.

        :raises: IloCommandNotSupportedError if the resource SmartStorage
            doesn't exist.
        :returns the tuple of SmartStorage URI, Headers and settings.
        """
        system = self._get_host_details()
        if ('links' in system['Oem']['Hp'] and
                'SmartStorage' in system['Oem']['Hp']['links']):
            # Get the SmartStorage URI and Settings
            storage_uri = system['Oem']['Hp']['links']['SmartStorage']['href']
            status, headers, storage_settings = self._rest_get(storage_uri)

            if status >= 300:
                msg = self._get_extended_error(storage_settings)
                raise exception.IloError(msg)

            return headers, storage_uri, storage_settings
        else:
            msg = ('"links/SmartStorage" section in ComputerSystem/Oem/Hp'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _get_array_controller_resource(self):
        """Gets the ArrayController resource if exists.

        :raises: IloCommandNotSupportedError if the resource ArrayController
            doesn't exist.
        :returns the tuple of SmartStorage URI, Headers and settings.
        """
        headers, storage_uri, storage_settings = self._get_storage_resource()
        if ('links' in storage_settings and
                'ArrayControllers' in storage_settings['links']):
            # Get the ArrayCOntrollers URI and Settings
            array_uri = storage_settings['links']['ArrayControllers']['href']
            status, headers, array_settings = self._rest_get(array_uri)

            if status >= 300:
                msg = self._get_extended_error(array_settings)
                raise exception.IloError(msg)

            return headers, array_uri, array_settings
        else:
            msg = ('"links/ArrayControllers" section in SmartStorage'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _create_list_of_array_controllers(self):
        """Creates the list of Array Controller URIs.

        :raises: IloCommandNotSupportedError if the ArrayControllers
            doesnt have member "Member".
        :returns list of ArrayControllers.
        """
        headers, array_uri, array_settings = (
            self._get_array_controller_resource())
        array_uri_links = []
        if ('links' in array_settings and
                'Member' in array_settings['links']):
            array_uri_links = array_settings['links']['Member']
        else:
            msg = ('"links/Member" section in ArrayControllers'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)
        return array_uri_links

    def _get_drive_type_and_speed(self):
        """Gets the disk drive type.

        :returns: A dictionary with the following keys:
            - has_rotational: True/False. It is True if atleast one
            rotational disk is attached.
            - has_ssd: True/False. It is True if at least one SSD disk is
            attached.
            - drive_rotational_<speed>_rpm: These are set to true as
              per the speed of the rotational disks.
        :raises: IloCommandNotSupportedError if the PhysicalDrives resource
            doesn't exist.
        :raises: IloError, on an error from iLO.
        """
        disk_details = self._get_physical_drive_resource()
        drive_hdd = False
        drive_ssd = False
        drive_details = {}
        speed_const_list = [4800, 5400, 7200, 10000, 15000]
        if disk_details:
            for item in disk_details:
                value = item['MediaType']
                if value == "HDD":
                    drive_hdd = True
                    speed = item['RotationalSpeedRpm']
                    if speed in speed_const_list:
                        var = 'rotational_drive_' + str(speed) + '_rpm'
                        drive_details.update({var: 'true'})
                # Note: RIS returns value as 'SDD' for SSD drives.
                else:
                    drive_ssd = True
        if drive_hdd:
            drive_details.update({'has_rotational': 'true'})
        if drive_ssd:
            drive_details.update({'has_ssd': 'true'})
        return drive_details if len(drive_details.keys()) > 0 else None

    def _get_drive_resource(self, drive_name):
        """Gets the DiskDrive resource if exists.

        :param drive_name: can be either "PhysicalDrives" or
             "LogicalDrives".
        :returns the list of drives.
        :raises: IloCommandNotSupportedError if the given drive resource
            doesn't exist.
        :raises: IloError, on an error from iLO.
        """
        disk_details_list = []
        array_uri_links = self._create_list_of_array_controllers()
        for array_link in array_uri_links:
            _, _, member_settings = (
                self._rest_get(array_link['href']))

            if ('links' in member_settings and
                    drive_name in member_settings['links']):
                disk_uri = member_settings['links'][drive_name]['href']
                headers, disk_member_uri, disk_mem = (
                    self._rest_get(disk_uri))
                if ('links' in disk_mem and
                        'Member' in disk_mem['links']):
                    for disk_link in disk_mem['links']['Member']:
                        diskdrive_uri = disk_link['href']
                        _, _, disk_details = (
                            self._rest_get(diskdrive_uri))
                        disk_details_list.append(disk_details)
                else:
                    msg = ('"links/Member" section in %s'
                           ' does not exist', drive_name)
                    raise exception.IloCommandNotSupportedError(msg)
            else:
                msg = ('"links/%s" section in '
                       ' ArrayController/links/Member does not exist',
                       drive_name)
                raise exception.IloCommandNotSupportedError(msg)
        if disk_details_list:
            return disk_details_list

    def _get_logical_drive_resource(self):
        """Returns the LogicalDrives data."""
        return self._get_drive_resource('LogicalDrives')

    def _get_physical_drive_resource(self):
        """Returns the PhysicalDrives data."""
        return self._get_drive_resource('PhysicalDrives')

    def _get_logical_raid_levels(self):
        """Gets the different raid levels configured on a server.

        :returns a dictionary of logical_raid_levels set to true.
            Example if raid level 1+0 and 6 are configured, it returns
            {'logical_raid_level_10': 'true',
             'logical_raid_level_6': 'true'}
        """
        logical_drive_details = self._get_logical_drive_resource()
        raid_level = {}
        if logical_drive_details:
            for item in logical_drive_details:
                if 'Raid' in item:
                    raid_level_var = "logical_raid_level_" + item['Raid']
                    raid_level.update({raid_level_var: 'true'})
        return raid_level if len(raid_level.keys()) > 0 else None

    def _is_raid_supported(self):
        """Get the RAID support on the server.

        This method returns the raid support on the physical server. It
        checks for the list of array controllers configured to the Smart
        Storage. If one or more array controllers available then raid
        is supported by the server. If none, raid is not supported.

        :return: Raid support as a dictionary with true/false as its value.
        """
        header, uri, array_resource = self._get_array_controller_resource()

        return True if array_resource['Total'] > 0 else False

    def _get_bios_settings_resource(self, data):
        """Get the BIOS settings resource."""
        try:
            bios_settings_uri = data['links']['Settings']['href']
        except KeyError:
            msg = ('BIOS Settings resource not found.')
            raise exception.IloError(msg)

        status, headers, bios_settings = self._rest_get(bios_settings_uri)
        if status != 200:
            msg = self._get_extended_error(bios_settings)
            raise exception.IloError(msg)

        return headers, bios_settings_uri, bios_settings

    def _validate_if_patch_supported(self, headers, uri):
        """Check if the PATCH Operation is allowed on the resource."""
        if not self._operation_allowed(headers, 'PATCH'):
                msg = ('PATCH Operation not supported on the resource '
                       '"%s"' % uri)
                raise exception.IloError(msg)

    def _get_bios_setting(self, bios_property):
        """Retrieves bios settings of the server."""
        headers, bios_uri, bios_settings = self._check_bios_resource([
            bios_property])
        return bios_settings[bios_property]

    def _get_bios_hash_password(self, bios_password):
        """Get the hashed BIOS password."""
        request_headers = {}
        if bios_password:
            bios_password_hash = hashlib.sha256((bios_password.encode()).
                                                hexdigest().upper())
            request_headers['X-HPRESTFULAPI-AuthToken'] = bios_password_hash
        return request_headers

    def _change_bios_setting(self, properties):
        """Change the bios settings to specified values."""
        keys = properties.keys()
        # Check if the BIOS resource/property exists.
        headers, bios_uri, settings = self._check_bios_resource(keys)
        if not self._operation_allowed(headers, 'PATCH'):
            headers, bios_uri, _ = self._get_bios_settings_resource(settings)
            self._validate_if_patch_supported(headers, bios_uri)

        request_headers = self._get_bios_hash_password(self.bios_password)
        status, headers, response = self._rest_patch(bios_uri, request_headers,
                                                     properties)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_iscsi_settings_resource(self, data):
        """Get the iscsi settings resoure.

        :param data: Existing iscsi settings of the server.
        :returns: headers, iscsi_settings url and
                 iscsi settings as a dictionary.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            iscsi_settings_uri = data['links']['Settings']['href']
        except KeyError:
            msg = ('iscsi settings resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, iscsi_settings = self._rest_get(iscsi_settings_uri)

        if status != 200:
            msg = self._get_extended_error(iscsi_settings)
            raise exception.IloError(msg)

        return headers, iscsi_settings_uri, iscsi_settings

    def _get_bios_boot_resource(self, data):
        """Get the Boot resource like BootSources.

        :param data: Existing Bios settings of the server.
        :returns: boot settings.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            boot_uri = data['links']['Boot']['href']
        except KeyError:
            msg = ('Boot resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, boot_settings = self._rest_get(boot_uri)

        if status != 200:
            msg = self._get_extended_error(boot_settings)
            raise exception.IloError(msg)

        return boot_settings

    def _get_bios_mappings_resource(self, data):
        """Get the Mappings resource.

        :param data: Existing Bios settings of the server.
        :returns: mappings settings.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            map_uri = data['links']['Mappings']['href']
        except KeyError:
            msg = ('Mappings resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, map_settings = self._rest_get(map_uri)
        if status != 200:
            msg = self._get_extended_error(map_settings)
            raise exception.IloError(msg)

        return map_settings

    def _check_iscsi_rest_patch_allowed(self):
        """Checks if patch is supported on iscsi.

        :returns: iscsi url.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """

        headers, bios_uri, bios_settings = self._check_bios_resource()
        # Check if the bios resource exists.

        if('links' in bios_settings and 'iScsi' in bios_settings['links']):
            iscsi_uri = bios_settings['links']['iScsi']['href']
            status, headers, settings = self._rest_get(iscsi_uri)

            if status != 200:
                msg = self._get_extended_error(settings)
                raise exception.IloError(msg)

            if not self._operation_allowed(headers, 'PATCH'):
                headers, iscsi_uri, settings = (
                    self._get_iscsi_settings_resource(settings))
                self._validate_if_patch_supported(headers, iscsi_uri)

            return iscsi_uri

        else:
            msg = ('"links/iScsi" section in bios'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _change_iscsi_settings(self, iscsi_info):
        """Change iSCSI settings.

        :param iscsi_info: A dictionary that contains information of iSCSI
                           target like target_name, lun, ip_address, port etc.
        :raises: IloError, on an error from iLO.
        """
        headers, bios_uri, bios_settings = self._check_bios_resource()
        # Get the Mappings resource.
        map_settings = self._get_bios_mappings_resource(bios_settings)
        nics = []
        for mapping in map_settings['BiosPciSettingsMappings']:
            for subinstance in mapping['Subinstances']:
                for association in subinstance['Associations']:
                    if 'NicBoot' in association:
                        nics.append(association)

        if not nics:
            msg = ('No nics found')
            raise exception.IloError(msg)

        iscsi_uri = self._check_iscsi_rest_patch_allowed()
        # Set iSCSI info to all nics
        iscsi_infos = []
        for nic in nics:
            data = iscsi_info.copy()
            data['iSCSIBootAttemptName'] = nic
            data['iSCSINicSource'] = nic
            data['iSCSIBootAttemptInstance'] = nics.index(nic) + 1
            iscsi_infos.append(data)

        patch_data = {'iSCSIBootSources': iscsi_infos}
        status, headers, response = self._rest_patch(iscsi_uri,
                                                     None, patch_data)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _change_secure_boot_settings(self, property, value):
        """Change secure boot settings on the server."""
        system = self._get_host_details()
        # find the BIOS URI
        if ('links' not in system['Oem']['Hp'] or
           'SecureBoot' not in system['Oem']['Hp']['links']):
            msg = (' "SecureBoot" resource or feature is not '
                   'supported on this system')
            raise exception.IloCommandNotSupportedError(msg)

        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']

        # Change the property required
        new_secure_boot_settings = {}
        new_secure_boot_settings[property] = value

        # perform the patch
        status, headers, response = self._rest_patch(
            secure_boot_uri, None, new_secure_boot_settings)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        # Change the bios setting as a workaround to enable secure boot
        # Can be removed when fixed for Gen9 snap2
        val = self._get_bios_setting('CustomPostMessage')
        val = val.rstrip() if val.endswith(" ") else val+" "
        self._change_bios_setting({'CustomPostMessage': val})

    def _is_boot_mode_uefi(self):
        """Checks if the system is in uefi boot mode.

        :return: 'True' if the boot mode is uefi else 'False'
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        boot_mode = self.get_current_boot_mode()
        if boot_mode == 'UEFI':
            return True
        else:
            return False

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        """
        system = self._get_host_details()
        return system['Model']

    def get_secure_boot_mode(self):
        """Get the status of secure boot.

        :returns: True, if enabled, else False
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        system = self._get_host_details()

        if ('links' not in system['Oem']['Hp'] or
           'SecureBoot' not in system['Oem']['Hp']['links']):
            msg = ('"SecureBoot" resource or feature is not supported'
                   ' on this system')
            raise exception.IloCommandNotSupportedError(msg)

        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']

        # get the Secure Boot object
        status, headers, secure_boot_settings = self._rest_get(secure_boot_uri)

        if status >= 300:
            msg = self._get_extended_error(secure_boot_settings)
            raise exception.IloError(msg)

        return secure_boot_settings['SecureBootCurrentState']

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server.

        :param secure_boot_enable: True, if secure boot needs to be
               enabled for next boot, else False.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            self._change_secure_boot_settings('SecureBootEnable',
                                              secure_boot_enable)
        else:
            msg = ('System is not in UEFI boot mode. "SecureBoot" related '
                   'resources cannot be changed.')
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def reset_secure_boot_keys(self):
        """Reset secure boot keys to manufacturing defaults.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            self._change_secure_boot_settings('ResetToDefaultKeys', True)
        else:
            msg = ('System is not in UEFI boot mode. "SecureBoot" related '
                   'resources cannot be changed.')
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def clear_secure_boot_keys(self):
        """Reset all keys.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            self._change_secure_boot_settings('ResetAllKeys', True)
        else:
            msg = ('System is not in UEFI boot mode. "SecureBoot" related '
                   'resources cannot be changed.')
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """

        data = self._get_host_details()
        return data['Power'].upper()

    def _perform_power_op(self, oper):
        """Perform requested power operation.

        :param oper: Type of power button press to simulate.
                     Supported values: 'ON', 'ForceOff' and 'ForceRestart'
        :raises: IloError, on an error from iLO.
        """

        power_settings = {"Action": "Reset",
                          "ResetType": oper}
        systems_uri = "/rest/v1/Systems/1"

        status, headers, response = self._rest_post(systems_uri, None,
                                                    power_settings)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def reset_server(self):
        """Resets the server.

        :raises: IloError, on an error from iLO.
        """

        self._perform_power_op("ForceRestart")

    def _press_pwr_btn(self, pushType="Press"):
        """Simulates a physical press of the server power button.

        :param pushType: Type of power button press to simulate
                         Supported values are: 'Press' and 'PressAndHold'
        :raises: IloError, on an error from iLO.
        """
        power_settings = {"Action": "PowerButton",
                          "Target": "/Oem/Hp",
                          "PushType": pushType}

        systems_uri = "/rest/v1/Systems/1"

        status, headers, response = self._rest_post(systems_uri, None,
                                                    power_settings)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button.

        :raises: IloError, on an error from iLO.
        """
        self._press_pwr_btn()

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button.

        :raises: IloError, on an error from iLO.
        """
        self._press_pwr_btn(pushType="PressAndHold")

    @retrying.retry(
        stop_max_attempt_number=MAX_RETRY_ATTEMPTS,
        retry_on_result=lambda state: state != 'ON',
        wait_fixed=MAX_TIME_BEFORE_RETRY
    )
    def _retry_until_powered_on(self, power):
        """This method retries power on operation.

        :param: power : target power state
        """
        # If the system is in the same power state as
        # requested by the user, it gives the error
        # InvalidOperationForSystemState. To avoid this error
        # the power state is checked before power on
        # operation is performed.
        status = self.get_host_power_status()
        if (status != power):
            self._perform_power_op(POWER_STATE[power])
            return self.get_host_power_status()
        else:
            return status

    def set_host_power(self, power):
        """Toggle the power button of server.

        :param power: 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """
        power = power.upper()
        if (power is not None) and (power not in POWER_STATE):
            msg = ("Invalid input '%(pow)s'. "
                   "The expected input is ON or OFF." %
                   {'pow': power})
            raise exception.IloInvalidInputError(msg)

        # Check current power status, do not act if it's in requested state.
        cur_status = self.get_host_power_status()

        if cur_status == power:
            LOG.debug(self._("Node is already in '%(power)s' power state."),
                      {'power': power})
            return
        if power == 'ON' and 'PROLIANT BL' in self.get_product_name().upper():
            self._retry_until_powered_on(power)
        else:
            self._perform_power_op(POWER_STATE[power])

    def get_http_boot_url(self):
        """Request the http boot url from system in uefi boot mode.

        :returns: URL for http boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            return self._get_bios_setting('UefiShellStartupUrl')
        else:
            msg = 'get_http_boot_url is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def set_http_boot_url(self, url):
        """Set url to the UefiShellStartupUrl to the system in uefi boot mode.

        :param url: URL for http boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            self._change_bios_setting({'UefiShellStartupUrl': url})
        else:
            msg = 'set_http_boot_url is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def set_iscsi_info(self, target_name, lun, ip_address,
                       port='3260', auth_method=None, username=None,
                       password=None):
        """Set iSCSI details of the system in UEFI boot mode.

        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param target_name: Target Name for iscsi.
        :param lun: logical unit number.
        :param ip_address: IP address of the target.
        :param port: port of the target.
        :param auth_method : either None or CHAP.
        :param username: CHAP Username for authentication.
        :param password: CHAP secret.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the BIOS boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            iscsi_info = {}
            iscsi_info['iSCSITargetName'] = target_name
            iscsi_info['iSCSIBootLUN'] = lun
            iscsi_info['iSCSITargetIpAddress'] = ip_address
            iscsi_info['iSCSITargetTcpPort'] = int(port)
            iscsi_info['iSCSITargetInfoViaDHCP'] = False
            iscsi_info['iSCSIBootEnable'] = 'Enabled'
            if (auth_method == 'CHAP'):
                iscsi_info['iSCSIAuthenticationMethod'] = 'Chap'
                iscsi_info['iSCSIChapUsername'] = username
                iscsi_info['iSCSIChapSecret'] = password
            self._change_iscsi_settings(iscsi_info)
        else:
            msg = 'iSCSI boot is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def unset_iscsi_info(self):
        """Disable iSCSI boot option in UEFI boot mode.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the BIOS boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            iscsi_info = {'iSCSIBootEnable': 'Disabled'}
            self._change_iscsi_settings(iscsi_info)
        else:
            msg = 'iSCSI boot is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def get_iscsi_initiator_info(self):
        """Give iSCSI initiator information of iLO.

        :returns: iSCSI initiator information.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the system is
                 in the bios boot mode.
        """
        headers, bios_uri, bios_settings = self._check_bios_resource()
        if('links' in bios_settings and 'iScsi' in bios_settings['links']):
            iscsi_uri = bios_settings['links']['iScsi']['href']
            status, headers, iscsi_settings = self._rest_get(iscsi_uri)

            if status != 200:
                msg = self._get_extended_error(iscsi_settings)
                raise exception.IloError(msg)
            return iscsi_settings['iSCSIInitiatorName']
        else:
            msg = ('"links/iScsi" section in bios '
                   'does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def set_iscsi_initiator_info(self, initiator_iqn):
        """Set iSCSI initiator information in iLO.

        :param initiator_iqn: Initiator iqn for iLO.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the system is
                 in the bios boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            iscsi_uri = self._check_iscsi_rest_patch_allowed()
            initiator_info = {'iSCSIInitiatorName': initiator_iqn}
            status, headers, response = self._rest_patch(iscsi_uri,
                                                         None, initiator_info)
            if status >= 300:
                msg = self._get_extended_error(response)
                raise exception.IloError(msg)
        else:
            msg = 'iSCSI initiator cannot be set in the BIOS boot mode'
            raise exception.IloCommandNotSupportedError(msg)

    def get_current_boot_mode(self):
        """Retrieves the current boot mode of the server.

        :returns: Current boot mode, LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        boot_mode = self._get_bios_setting('BootMode')
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'

        return boot_mode.upper()

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode of the server.

        Gets the boot mode to be set on next reset.
        :returns: either LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        headers, uri, bios_settings = self._check_bios_resource(['BootMode'])
        _, _, settings = self._get_bios_settings_resource(bios_settings)
        boot_mode = settings.get('BootMode')
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        return boot_mode.upper()

    def set_pending_boot_mode(self, boot_mode):
        """Sets the boot mode of the system for next boot.

        :param boot_mode: either 'uefi' or 'legacy'.
        :raises: IloInvalidInputError, on an invalid input.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        boot_mode = boot_mode.lower()
        if boot_mode not in ['uefi', 'legacy']:
            msg = 'Invalid Boot mode specified'
            raise exception.IloInvalidInputError(msg)

        boot_properties = {'BootMode': boot_mode}

        if boot_mode == 'legacy':
            boot_properties['BootMode'] = 'LegacyBios'
        else:
            # If Boot Mode is 'Uefi' set the UEFIOptimizedBoot first.
            boot_properties['UefiOptimizedBoot'] = "Enabled"

        # Change the Boot Mode
        self._change_bios_setting(boot_properties)

    def get_supported_boot_mode(self):
        """Retrieves the supported boot mode.

        :returns: any one of the following proliantutils.ilo.constants:

            SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY,
            SUPPORTED_BOOT_MODE_UEFI_ONLY,
            SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI

        """
        system = self._get_host_details()
        bios_uefi_class_val = 0  # value for bios_only boot mode
        if ('Bios' in system['Oem']['Hp'] and
                'UefiClass' in system['Oem']['Hp']['Bios']):
            bios_uefi_class_val = (system['Oem']['Hp']
                                         ['Bios']['UefiClass'])
        return mappings.GET_SUPPORTED_BOOT_MODE_RIS_MAP.get(
            bios_uefi_class_val)

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        acc_uri = '/rest/v1/AccountService/Accounts'

        for status, hds, account, memberuri in self._get_collection(acc_uri):
            if account['UserName'] == self.login:
                mod_user = {}
                mod_user['Password'] = password
                status, headers, response = self._rest_patch(memberuri,
                                                             None, mod_user)
                if status != 200:
                    msg = self._get_extended_error(response)
                    raise exception.IloError(msg)
                return

        msg = "iLO Account with specified username is not found."
        raise exception.IloError(msg)

    def _get_ilo_details(self):
        """Gets iLO details

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        manager_uri = '/rest/v1/Managers/1'
        status, headers, manager = self._rest_get(manager_uri)

        if status != 200:
            msg = self._get_extended_error(manager)
            raise exception.IloError(msg)

        # verify expected type
        mtype = self._get_type(manager)
        if (mtype not in ['Manager.0', 'Manager.1']):
            msg = "%s is not a valid Manager type " % mtype
            raise exception.IloError(msg)

        return manager, manager_uri

    def reset_ilo(self):
        """Resets the iLO.

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        manager, reset_uri = self._get_ilo_details()
        action = {'Action': 'Reset'}

        # perform the POST
        status, headers, response = self._rest_post(reset_uri, None, action)

        if(status != 200):
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        # Check if the iLO is up again.
        common.wait_for_ilo_after_reset(self)

    def reset_bios_to_default(self):
        """Resets the BIOS settings to default values.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        # Check if the BIOS resource if exists.
        headers_bios, bios_uri, bios_settings = self._check_bios_resource()
        # Get the BaseConfig resource.
        try:
            base_config_uri = bios_settings['links']['BaseConfigs']['href']
        except KeyError:
            msg = ("BaseConfigs resource not found. Couldn't apply the BIOS "
                   "Settings.")
            raise exception.IloCommandNotSupportedError(msg)

        # Check if BIOS resource supports patch, else get the settings
        if not self._operation_allowed(headers_bios, 'PATCH'):
            headers, bios_uri, _ = self._get_bios_settings_resource(
                bios_settings)
            self._validate_if_patch_supported(headers, bios_uri)

        status, headers, config = self._rest_get(base_config_uri)
        if status != 200:
            msg = self._get_extended_error(config)
            raise exception.IloError(msg)

        new_bios_settings = {}
        for cfg in config['BaseConfigs']:
            default_settings = cfg.get('default', None)
            if default_settings is not None:
                new_bios_settings = default_settings
                break
        else:
            msg = ("Default Settings not found in 'BaseConfigs' resource.")
            raise exception.IloCommandNotSupportedError(msg)
        request_headers = self._get_bios_hash_password(self.bios_password)
        status, headers, response = self._rest_patch(bios_uri, request_headers,
                                                     new_bios_settings)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_ilo_firmware_version(self):
        """Gets the ilo firmware version for server capabilities

        :returns: a dictionary of iLO firmware version.

        """

        manager, reset_uri = self._get_ilo_details()
        ilo_firmware_version = manager['Firmware']['Current']['VersionString']
        return {'ilo_firmware_version': ilo_firmware_version}

    def get_ilo_firmware_version_as_major_minor(self):
        """Gets the ilo firmware version for server capabilities

        :returns: String with the format "<major>.<minor>" or None.

        """
        try:
            manager, reset_uri = self._get_ilo_details()
            ilo_fw_ver_str = (
                manager['Oem']['Hp']['Firmware']['Current']['VersionString']
            )
            return common.get_major_minor(ilo_fw_ver_str)
        except Exception:
            return None

    def _is_sriov_enabled(self):
        """Return sriov enabled or not"""
        return (self._get_bios_setting('Sriov') == 'Enabled')

    def get_server_capabilities(self):
        """Gets server properties which can be used for scheduling

        :returns: a dictionary of hardware properties like firmware
                  versions, server model.
        :raises: IloError, if iLO returns an error in command execution.

        """
        capabilities = {}
        system = self._get_host_details()
        capabilities['server_model'] = system['Model']
        rom_firmware_version = (
            system['Oem']['Hp']['Bios']['Current']['VersionString'])
        capabilities['rom_firmware_version'] = rom_firmware_version
        capabilities.update(self._get_ilo_firmware_version())
        capabilities.update(self._get_number_of_gpu_devices_connected())
        drive_details = self._get_drive_type_and_speed()
        if drive_details is not None:
            capabilities.update(drive_details)
        raid_details = self._get_logical_raid_levels()
        if raid_details is not None:
            capabilities.update(raid_details)
        if self._is_raid_supported():
            capabilities['hardware_supports_raid'] = 'true'
        boot_modes = common.get_supported_boot_modes(
            self.get_supported_boot_mode())
        capabilities.update({
            'boot_mode_bios': boot_modes.boot_mode_bios,
            'boot_mode_uefi': boot_modes.boot_mode_uefi})
        if self._get_tpm_capability():
            capabilities['trusted_boot'] = 'true'
        if self._get_cpu_virtualization():
            capabilities['cpu_vt'] = 'true'
        if self._get_nvdimm_n_status():
            capabilities['nvdimm_n'] = 'true'
        try:
            self._check_iscsi_rest_patch_allowed()
            capabilities['iscsi_boot'] = 'true'
        except exception.IloError:
            # If an error is raised dont populate the capability
            # iscsi_boot
            pass
        try:
            self.get_secure_boot_mode()
            capabilities['secure_boot'] = 'true'
        except exception.IloCommandNotSupportedError:
            # If an error is raised dont populate the capability
            # secure_boot
            pass
        if self._is_sriov_enabled():
            capabilities['sriov_enabled'] = 'true'
        return capabilities

    def activate_license(self, key):
        """Activates iLO license.

        :param key: iLO license key.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        manager, uri = self._get_ilo_details()
        try:
            lic_uri = manager['Oem']['Hp']['links']['LicenseService']['href']
        except KeyError:
            msg = ('"LicenseService" section in Manager/Oem/Hp does not exist')
            raise exception.IloCommandNotSupportedError(msg)

        lic_key = {}
        lic_key['LicenseKey'] = key

        # Perform POST to activate license
        status, headers, response = self._rest_post(lic_uri, None, lic_key)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_vm_device_status(self,  device='FLOPPY'):
        """Returns the given virtual media device status and device URI

        :param  device: virtual media device to be queried
        :returns json format virtual media device status and its URI
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        valid_devices = {'FLOPPY': 'floppy',
                         'CDROM': 'cd'}

        # Check if the input is valid
        if device not in valid_devices:
                raise exception.IloInvalidInputError(
                    "Invalid device. Valid devices: FLOPPY or CDROM.")

        manager, uri = self._get_ilo_details()
        try:
            vmedia_uri = manager['links']['VirtualMedia']['href']
        except KeyError:
            msg = ('"VirtualMedia" section in Manager/links does not exist')
            raise exception.IloCommandNotSupportedError(msg)

        for status, hds, vmed, memberuri in self._get_collection(vmedia_uri):
            status, headers, response = self._rest_get(memberuri)
            if status != 200:
                msg = self._get_extended_error(response)
                raise exception.IloError(msg)

            if (valid_devices[device] in
               [item.lower() for item in response['MediaTypes']]):
                vm_device_uri = response['links']['self']['href']
                return response, vm_device_uri

        # Requested device not found
        msg = ('Virtualmedia device "' + device + '" is not'
               ' found on this system.')
        raise exception.IloError(msg)

    def get_vm_status(self, device='FLOPPY'):
        """Returns the virtual media drive status.

        :param  device: virtual media device to be queried
        :returns device status in dictionary form
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        response, vm_device_uri = self._get_vm_device_status(device)

        # Create RIBCL equivalent response
        # RIBCL provides this data in VM status
        # VM_APPLET = CONNECTED | DISCONNECTED
        # DEVICE = FLOPPY | CDROM
        # BOOT_OPTION = BOOT_ALWAYS | BOOT_ONCE | NO_BOOT
        # WRITE_PROTECT = YES | NO
        # IMAGE_INSERTED = YES | NO
        response_data = {}

        if response.get('WriteProtected', False):
            response_data['WRITE_PROTECT'] = 'YES'
        else:
            response_data['WRITE_PROTECT'] = 'NO'

        if response.get('BootOnNextServerReset', False):
            response_data['BOOT_OPTION'] = 'BOOT_ONCE'
        else:
            response_data['BOOT_OPTION'] = 'BOOT_ALWAYS'

        if response.get('Inserted', False):
            response_data['IMAGE_INSERTED'] = 'YES'
        else:
            response_data['IMAGE_INSERTED'] = 'NO'

        if response.get('ConnectedVia') == 'NotConnected':
            response_data['VM_APPLET'] = 'DISCONNECTED'
            # When media is not connected, it's NO_BOOT
            response_data['BOOT_OPTION'] = 'NO_BOOT'
        else:
            response_data['VM_APPLET'] = 'CONNECTED'

        response_data['IMAGE_URL'] = response['Image']
        response_data['DEVICE'] = device

        # FLOPPY cannot be a boot device
        if ((response_data['BOOT_OPTION'] == 'BOOT_ONCE') and
           (response_data['DEVICE'] == 'FLOPPY')):
            response_data['BOOT_OPTION'] = 'NO_BOOT'

        return response_data

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status

        It sets the boot option for virtual media device.
        Note: boot option can be set only for CD device.

        :param device: virual media device
        :param boot_option: boot option to set on the virtual media device
        :param write_protect: set the write protect flag on the vmedia device
                              Note: It's ignored. In RIS it is read-only.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        # CONNECT is a RIBCL call. There is no such property to set in RIS.
        if boot_option == 'CONNECT':
            return

        boot_option_map = {'BOOT_ONCE': True,
                           'BOOT_ALWAYS': False,
                           'NO_BOOT': False
                           }

        if boot_option not in boot_option_map:
            msg = ('Virtualmedia boot option "' + boot_option + '" is '
                   'invalid.')
            raise exception.IloInvalidInputError(msg)

        response, vm_device_uri = self._get_vm_device_status(device)

        # Update required property
        vm_settings = {}
        vm_settings['Oem'] = (
            {'Hp': {'BootOnNextServerReset': boot_option_map[boot_option]}})

        # perform the patch operation
        status, headers, response = self._rest_patch(
            vm_device_uri, None, vm_settings)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image.

        :param url: URL to image
        :param device: virual media device
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        response, vm_device_uri = self._get_vm_device_status(device)

        # Eject media if there is one. RIBCL was tolerant enough to overwrite
        # existing media, RIS is not. This check is to take care of that
        # assumption.
        if response.get('Inserted', False):
            self.eject_virtual_media(device)

        # Update required property
        vm_settings = {}
        vm_settings['Image'] = url

        # Perform the patch operation
        status, headers, response = self._rest_patch(
            vm_device_uri, None, vm_settings)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted.

        :param device: virual media device
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        response, vm_device_uri = self._get_vm_device_status(device)

        # Check if virtual media is connected.
        if response.get('Inserted') is False:
            return

        # Update required property
        vm_settings = {}
        vm_settings['Image'] = None

        # perform the patch operation
        status, headers, response = self._rest_patch(
            vm_device_uri, None, vm_settings)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_persistent_boot_devices(self):
        """Get details of persistent boot devices, its order

        :returns: List of dictionary of boot sources and
                  list of boot device order
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        # Check if the BIOS resource if exists.
        headers_bios, bios_uri, bios_settings = self._check_bios_resource()

        # Get the Boot resource.
        boot_settings = self._get_bios_boot_resource(bios_settings)

        # Get the BootSources resource
        try:
            boot_sources = boot_settings['BootSources']
        except KeyError:
            msg = ("BootSources resource not found.")
            raise exception.IloError(msg)

        try:
            boot_order = boot_settings['PersistentBootConfigOrder']
        except KeyError:
            msg = ("PersistentBootConfigOrder resource not found.")
            raise exception.IloCommandNotSupportedError(msg)

        return boot_sources, boot_order

    def get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        system = self._get_host_details()
        try:
            # Return boot device if it is persistent.
            if system['Boot']['BootSourceOverrideEnabled'] == 'Continuous':
                device = system['Boot']['BootSourceOverrideTarget']
                if device in DEVICE_RIS_TO_COMMON:
                    return DEVICE_RIS_TO_COMMON[device]
                return device
        except KeyError as e:
            msg = "get_persistent_boot_device failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        # Check if we are in BIOS boot mode.
        # There is no resource to fetch boot device order for BIOS boot mode
        if not self._is_boot_mode_uefi():
            return None

        # Get persistent boot device order for UEFI
        boot_sources, boot_devices = self._get_persistent_boot_devices()

        boot_string = ""
        try:
            for source in boot_sources:
                if (source["StructuredBootString"] == boot_devices[0]):
                    boot_string = source["BootString"]
                    break
        except KeyError as e:
            msg = "get_persistent_boot_device failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        if 'HP iLO Virtual USB CD' in boot_string:
            return 'CDROM'

        elif ('NIC' in boot_string or
              'PXE' in boot_string or
              "iSCSI" in boot_string):
            return 'NETWORK'

        elif common.isDisk(boot_string):
            return 'HDD'

        else:
            return None

    def _update_persistent_boot(self, device_type=[], persistent=False):
        """Changes the persistent boot device order in BIOS boot mode for host

        Note: It uses first boot device from the device_type and ignores rest.

        :param device_type: ordered list of boot devices
        :param persistent: Boolean flag to indicate if the device to be set as
                           a persistent boot device
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        tenure = 'Once'
        new_device = device_type[0]
        # If it is a standard device, we need to convert in RIS convention
        if device_type[0].upper() in DEVICE_COMMON_TO_RIS:
            new_device = DEVICE_COMMON_TO_RIS[device_type[0].upper()]

        if persistent:
            tenure = 'Continuous'

        systems_uri = "/rest/v1/Systems/1"
        # Need to set this option first if device is 'UefiTarget'
        if new_device is 'UefiTarget':
            system = self._get_host_details()
            uefi_devices = (
                system['Boot']['UefiTargetBootSourceOverrideSupported'])
            iscsi_device = None
            for device in uefi_devices:
                if device is not None and 'iSCSI' in device:
                    iscsi_device = device
                    break

            if iscsi_device is None:
                msg = 'No UEFI iSCSI bootable device found'
                raise exception.IloError(msg)

            new_boot_settings = {}
            new_boot_settings['Boot'] = {'UefiTargetBootSourceOverride':
                                         iscsi_device}

            status, headers, response = self._rest_patch(systems_uri, None,
                                                         new_boot_settings)
            if status >= 300:
                msg = self._get_extended_error(response)
                raise exception.IloError(msg)

        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': tenure,
                                     'BootSourceOverrideTarget': new_device}
        status, headers, response = self._rest_patch(systems_uri, None,
                                                     new_boot_settings)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def update_persistent_boot(self, device_type=[]):
        """Changes the persistent boot device order for the host

        :param device_type: ordered list of boot devices
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        # Check if the input is valid
        for item in device_type:
            if item.upper() not in DEVICE_COMMON_TO_RIS:
                raise exception.IloInvalidInputError("Invalid input. Valid "
                                                     "devices: NETWORK, HDD,"
                                                     " ISCSI or CDROM.")

        self._update_persistent_boot(device_type, persistent=True)

    def set_one_time_boot(self, device):
        """Configures a single boot from a specific device.

        :param device: Device to be set as a one time boot device
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        self._update_persistent_boot([device], persistent=False)

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot.

        :returns: Returns the first boot device that would be used in next
                 boot. Returns 'Normal' is no device is set.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        system = self._get_host_details()
        try:
            if system['Boot']['BootSourceOverrideEnabled'] == 'Once':
                device = system['Boot']['BootSourceOverrideTarget']
                if device in DEVICE_RIS_TO_COMMON:
                    return DEVICE_RIS_TO_COMMON[device]
                return device
            else:
                # value returned by RIBCL if one-time boot setting are absent
                return 'Normal'

        except KeyError as e:
            msg = "get_one_time_boot failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

    def _get_firmware_update_service_resource(self):
        """Gets the firmware update service uri.

        :returns: firmware update service uri
        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if not able to reach iLO.
        :raises: IloCommandNotSupportedError, for not finding the uri
        """
        manager, uri = self._get_ilo_details()
        try:
            fw_uri = manager['Oem']['Hp']['links']['UpdateService']['href']
        except KeyError:
            msg = ("Firmware Update Service resource not found.")
            raise exception.IloCommandNotSupportedError(msg)
        return fw_uri

    @firmware_controller.check_firmware_update_component
    def update_firmware(self, file_url, component_type):
        """Updates the given firmware on the server for the given component.

        :param file_url: location of the raw firmware file. Extraction of the
                         firmware file (if in compact format) is expected to
                         happen prior to this invocation.
        :param component_type: Type of component to be applied to.
        :raises: InvalidInputError, if the validation of the input fails
        :raises: IloError, on an error from iLO
        :raises: IloConnectionError, if not able to reach iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        fw_update_uri = self._get_firmware_update_service_resource()
        action_data = {
            'Action': 'InstallFromURI',
            'FirmwareURI': file_url,
        }

        # perform the POST
        LOG.debug(self._('Flashing firmware file: %s ...'), file_url)
        status, headers, response = self._rest_post(
            fw_update_uri, None, action_data)
        if status != 200:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        # wait till the firmware update completes.
        common.wait_for_ris_firmware_update_to_complete(self)

        try:
            state, percent = self.get_firmware_update_progress()
        except exception.IloError:
            msg = 'Status of firmware update not known'
            LOG.debug(self._(msg))  # noqa
            return

        if state == "ERROR":
            msg = 'Unable to update firmware'
            LOG.debug(self._(msg))  # noqa
            raise exception.IloError(msg)
        elif state == "UNKNOWN":
            msg = 'Status of firmware update not known'
            LOG.debug(self._(msg))  # noqa
        else:  # "COMPLETED" | "IDLE"
            LOG.info(self._('Flashing firmware file: %s ... done'), file_url)

    def get_firmware_update_progress(self):
        """Get the progress of the firmware update.

        :returns: firmware update state, one of the following values:
                  "IDLE", "UPLOADING", "PROGRESSING", "COMPLETED", "ERROR".
                  If the update resource is not found, then "UNKNOWN".
        :returns: firmware update progress percent
        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if not able to reach iLO.
        """
        try:
            fw_update_uri = self._get_firmware_update_service_resource()
        except exception.IloError as e:
            LOG.debug(self._('Progress of firmware update not known: %s'),
                      str(e))
            return "UNKNOWN", "UNKNOWN"

        # perform the GET
        status, headers, response = self._rest_get(fw_update_uri)
        if status != 200:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        fw_update_state = response.get('State')
        fw_update_progress_percent = response.get('ProgressPercent')
        LOG.debug(self._('Flashing firmware file ... in progress %d%%'),
                  fw_update_progress_percent)
        return fw_update_state, fw_update_progress_percent

    def _get_number_of_gpu_devices_connected(self):
        """get the number of GPU devices connected."""
        gpu_devices = self._get_gpu_pci_devices()
        gpu_devices_count = len(gpu_devices)
        return {'pci_gpu_devices': gpu_devices_count}

    def _get_tpm_capability(self):
        """Retrieves if server is TPM capable or not.

        :returns True if TPM is Present else False
        """
        tpm_values = {"NotPresent": False,
                      "PresentDisabled": True,
                      "PresentEnabled": True}
        try:
            tpm_state = self._get_bios_setting('TpmState')
        except exception.IloCommandNotSupportedError:
            tpm_state = "NotPresent"
        tpm_result = tpm_values[tpm_state]
        return tpm_result

    def _get_cpu_virtualization(self):
        """get cpu virtualization status."""
        try:
            cpu_vt = self._get_bios_setting('ProcVirtualization')
        except exception.IloCommandNotSupportedError:
            return False
        if cpu_vt == 'Enabled':
            vt_status = True
        else:
            vt_status = False
        return vt_status

    def _get_nvdimm_n_status(self):
        """Get status of NVDIMM_N.

        :returns: True if NVDIMM_N is present and enabled, False otherwise.
        """
        try:
            nvdimm_n_status = self._get_bios_setting('NvDimmNMemFunctionality')
            if nvdimm_n_status == 'Enabled':
                nvn_status = True
            else:
                nvn_status = False
        except exception.IloCommandNotSupportedError:
            nvn_status = False
        return nvn_status
