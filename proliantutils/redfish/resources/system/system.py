# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import sushy
from sushy.resources import base
from sushy.resources.system import system

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import array_controller
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import disk_drives
from proliantutils.redfish.resources.system import drives
from proliantutils.redfish.resources.system import ethernet_interface
from proliantutils.redfish.resources.system import logical_drives
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import simple_storage
from proliantutils.redfish.resources.system import smart_storage
from proliantutils.redfish.resources.system import storage
from proliantutils.redfish.resources.system import unconfigured_drives
from proliantutils.redfish.resources.system import volumes
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)

PERSISTENT_BOOT_DEVICE_MAP = {
    'CDROM': sys_cons.BOOT_SOURCE_TARGET_CD,
    'NETWORK': sys_cons.BOOT_SOURCE_TARGET_PXE,
    'ISCSI': sys_cons.BOOT_SOURCE_TARGET_UEFI_TARGET,
    'HDD': sys_cons.BOOT_SOURCE_TARGET_HDD
}


class PowerButtonActionField(base.CompositeField):
    allowed_values = base.Field('PushType@Redfish.AllowableValues',
                                adapter=list)

    target_uri = base.Field('target', required=True)


class HpeActionsField(base.CompositeField):
    computer_system_ext_powerbutton = (
        PowerButtonActionField('#HpeComputerSystemExt.PowerButton'))


class HpeEthernetInterface(base.CompositeField):
    eth_interface_path = base.Field(['EthernetInterface', '@odata.id'])


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """

    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)

    """Oem specific system extensibility actions"""

    _bios_settings = None
    _simple_storage_path = base.Field(['SimpleStorage', '@odata.id'])
    _storage_path = base.Field(['Storage', '@odata.id'])
    _smart_storage_path = base.Field(['Oem', 'Hpe', 'Links',
                                      'SmartStorage', '@odata.id'])

    _local_gb = None
    _simple_storages = None
    _storages = None
    _volume = None
    _smart_storages = None
    _array_controllers = None
    _logical_drive = None
    _smart_disk_drive = None
    _smart_unconfigured_disk_drive = None

    _connected_mac_addresses = None
    _hpe_eth_interface = HpeEthernetInterface(['Oem', 'Hpe',
                                               'EthernetInterfaces'])

    def _get_hpe_push_power_button_action_element(self):
        push_action = self._hpe_actions.computer_system_ext_powerbutton
        if not push_action:
            raise exception.MissingAttributeError(
                attribute='Oem/Hpe/Actions/#HpeComputerSystemExt.PowerButton',
                resource=self.path)

        return push_action

    def push_power_button(self, target_value):
        """Reset the system in hpe exclusive manner.

        :param target_value: The target value to be set.
        :raises: InvalidInputError, if the target value is not
            allowed.
        :raises: SushyError, on an error from iLO.
        """
        if target_value not in mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV:
            msg = ('The parameter "%(parameter)s" value "%(target_value)s" is '
                   'invalid. Valid values are: %(valid_power_values)s' %
                   {'parameter': 'target_value', 'target_value': target_value,
                    'valid_power_values': (
                        mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV.keys())})
            raise exception.InvalidInputError(msg)

        value = mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV[target_value]
        target_uri = (
            self._get_hpe_push_power_button_action_element().target_uri)

        self._conn.post(target_uri, data={'PushType': value})

    @property
    def bios_settings(self):
        """Property to provide reference to bios_settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._bios_settings is None:
            self._bios_settings = bios.BIOSSettings(
                self._conn, utils.get_subresource_path_by(self, 'Bios'),
                redfish_version=self.redfish_version)

        return self._bios_settings

    def update_persistent_boot(self, devices=[], persistent=False,
                               mac=None):
        """Changes the persistent boot device order in BIOS boot mode for host

        Note: It uses first boot device from the devices and ignores rest.

        :param devices: ordered list of boot devices
        :param persistent: Boolean flag to indicate if the device to be set as
                           a persistent boot device
        :param mac: intiator mac address, mandotory for iSCSI uefi boot
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the given input is not valid.
        """
        new_device = devices[0]
        tenure = 'Continuous' if persistent else 'Once'

        try:
            boot_sources = self.bios_settings.boot_settings.boot_sources
        except sushy.exceptions.SushyError:
            msg = ('The BIOS Boot Settings was not found.')
            raise exception.IloError(msg)

        if devices[0].upper() in PERSISTENT_BOOT_DEVICE_MAP:
            new_device = PERSISTENT_BOOT_DEVICE_MAP[devices[0].upper()]

        new_boot_settings = {}
        if new_device is 'UefiTarget':
            if not mac:
                msg = ('Mac is needed for iscsi uefi boot')
                raise exception.IloInvalidInputError(msg)

            boot_string = None
            for boot_source in boot_sources:
                if(mac.upper() in boot_source['UEFIDevicePath'] and
                   'iSCSI' in boot_source['UEFIDevicePath']):
                    boot_string = boot_source['StructuredBootString']
                    break

            if not boot_string:
                msg = ('MAC provided "%s" is Invalid' % mac)
                raise exception.IloInvalidInputError(msg)

            uefi_boot_settings = {}
            uefi_boot_settings['Boot'] = (
                {'UefiTargetBootSourceOverride': boot_string})
            self._conn.patch(self._path, uefi_boot_settings)

        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': tenure,
                                     'BootSourceOverrideTarget': new_device}
        self._conn.patch(self._path, new_boot_settings)

    def _get_hpe_sub_resource_collection_path(self, sub_res):
        path = None
        try:
            path = utils.get_subresource_path_by(self, sub_res)
        except exception.MissingAttributeError:
                path = utils.get_subresource_path_by(
                    self, ['Oem', 'Hpe', 'Links', sub_res])
        return path

    @property
    def ethernet_interfaces(self):
        """Provide reference to EthernetInterfacesCollection instance"""
        if self._connected_mac_addresses is None:
            sub_res = 'EthernetInterfaces'
            self._connected_mac_addresses = (
                ethernet_interface.EthernetInterfaceCollection(
                    self._conn,
                    self._get_hpe_sub_resource_collection_path(sub_res),
                    redfish_version=self.redfish_version))

        return self._connected_mac_addresses

    @property
    def simple_storages(self):
        path = self._simple_storage_path
        if path:
            self._simple_storages = simple_storage.SimpleStorageCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._simple_storages

    @property
    def storages(self):
        path = self._storage_path
        if path:
            self._storages = storage.StorageCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._storages

    @property
    def volume(self):
        self._volume = []
        volume_paths = self.storages.volume_paths
        if volume_paths is not None or len(volume_paths) > 0:
            for path in volume_paths:
                vol = volumes.VolumesCollection(
                    self._conn, path, redfish_version=self.redfish_version)
                self._volume.append(vol)
        return self._volume

    @property
    def diskdrive(self):
        members = self.storages.get_members()
        for member in members:
            path = self._storage.drives.get('@odata.id')
            self._diskdrive.append(path)
        return self._diskdrive

    @property
    def smart_storages(self):
        path = self._smart_storage_path
        if path:
            self._smart_storages = smart_storage.SmartStorageCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._smart_storages

    @property
    def array_controllers(self):
        members = self.smart_storages.get_members()
        for member in members:
            self._array_controller_path = member.array_controller
        path = self._array_controller_path
        if path:
            self._array_controllers = (
                array_controller.ArrayControllerCollection(
                    self._conn, path,
                    redfish_version=self.redfish_version))
        return self._array_controller

    @property
    def logical_drive(self):
        members = self.array_controllers.get_members()
        for member in members:
            self._logical_drive_path = member.logical_drives
        path = self._logical_drive_path
        if path:
            self._logical_drive = logical_drives.LogicalDriveCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._logical_drive

    @property
    def smart_disk_drive(self):
        members = self.array_controller.get_members()
        for member in members:
            self._smart_disk_drive_path = member.disk_drive
        path = self._smart_disk_drive_path
        if path:
            self._smart_disk_drive = disk_drives.DiskDriveCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._smart_disk_drive

    @property
    def smart_unconfigured_disk_drive(self):
        members = self.array_controller.get_members()
        for member in members:
            self._smart_disk_drive_path = member.disk_drive
        path = self._smart_unconfigured_disk_drive_path
        if path:
            self._smart_unconfigured_disk_drive = (
                unconfigured_drives.DiskDriveCollection(
                    self._conn, path, redfish_version=self.redfish_version))
        return self._smart_unconfigured_disk_drive

    @property
    def storage_summary(self):
        """Gets the storage size.

        Redfish standards supports the disk data in following possible ways:
        1. /redfish/v1/Systems/<System_id>/SimpleStorage - simple collection
        2. /redfish/v1/Systems/<System_id>/Storage - Storage collection
        3. /redfish/v1/Systems/<System_id>/Storage/<storage_id>/Volumes -
           Volume collection.
        4. /redfish/v1/Systems/<System_id>/Storage/<storage_id>/<Drive_id>
           - Drive URIs.
           or
          /redfish/v1/Chassis/<Chassis_id>/<Drive_id> - drive URIs

        The algorithm followed is:
        1. Get the biggest size from SimpleStorage if SimpleStorage is present.
        2. If the volume is present, get the biggest volume size else get the
           biggest disk size(DAS).
        3. Compares the disk size returned in 1 and 2 above.

        There is a possibility that the system does not have "SimpleStorage"
        and "Storage" URIs both and has the vendor specific storage URI.
        """
        size = 0
        if self._storage_path:
            size = self._get_disk_size_from_storage_uri()
        if self._simple_storage_path and not self._volume:
            if size < self.simple_storage.size:
                size = self.simple_storage.size
        if self._smart_storage_path:
            smart_size = self._get_size_by_smart_storage()
            if size < smart_size:
                size = smart_size
        self._local_gb = size / (1024 * 1024 * 1024)
        return self._local_gb

    def get_disk_size_from_storage_uri(self):
        """Gets volume/disk size.

        The pseudo algo followed is:
            1. Get members from Storage collection.
            2. Check if ['Volumes'] is present in each of the Storage member.
            3. If present, get Volumes collection given in the Storage member
               data.
            4. parse through each volume member and get the max volume size.
            5. If ['Volumes'] is not present in any of the Storage, then
               check if the ['Drives'] is present.(DAS case)
            6. if '5' is yes, then traverse through each drive URI and get the
               disk with greatest size.(drive URI may or may not be part of
               Storage collection).
            7. Follow steps 2 to 6 for each member of Storage collection.
        """
        size = 0
        volume_members = self.volume
        if volume_members:
            size = self.volume.size
        else:
            drives_list = self.diskdrives
            if drives_list is not None:
                dr_size = self._get_size_by_drives(drives_list)
                if size < dr_size:
                    size = dr_size
        return size

    def _get_size_by_drives(self, drives_list):
        """Gets the disk of greatest size.

        :param: drives_list: A list of drives as
            [{'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'},
            {'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'},
            {'@odata.id':
                '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_id>'},
            {'@odata.id':
                '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_id>'},
            {'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'}]
        Note: There is no collection as "Drives", hence if tried to get
        data for '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives'
        or '</redfish/v1/Chassis/<chassis_id>/Drives' will lead to no data or
        invalid URI. The links can be even as follows:
        '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_type>/<drive_id>'
        or
        '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_type>/<Dr_id>'.
        In these cases the URIs,
        '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_type>/'
        or
        '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_type>/'
        gives no data and is invalid URI.

        """

        size = 0
        for drive_mem in drives_list:
            drive_uri = drive_mem.get('@odata.id')
            dr_obj = drives.Drives(self._conn, drive_uri,
                                   self.redfish_version)
            if size < dr_obj.capacity_bytes:
                size = dr_obj.capacity_bytes
        return size

    def _get_size_by_smart_storage(self):
        """Traverse through SmartStorgae URI

        Traverse through SmartStorage URI and gets the greatest volume size
        if volume is configured else gets the greatest disk size.
        """
        size = 0
        logical_drive_members = self.logical_drives
        if logical_drive_members:
            size = self.logical_drives.size
        else:
            smart_disk_drive_members = self.smart_disk_drive
            if smart_disk_drive_members:
                size = self.smart_disk_drive.size
            unconfigured_disk_drive_mem = self.smart_unconfigured_disk_drive
            if unconfigured_disk_drive_mem:
                unconfigured_size = self.smart_unconfigured_disk_drive.size
                if size < unconfigured_size:
                    size = unconfigured_size
        return size

    @property
    def has_ssd(self):
        """This property gets the media type of the disk as ssd"""
        drives_list = self.diskdrive
        if drives_list is not None:
            for drive_mem in drives_list:
                drive_uri = drive_mem.get('@odata.id')
                dr_obj = drives.Drives(self._conn, drive_uri,
                                       self.redfish_version)
                if dr_obj.media_type == sys_cons.MEDIA_TYPE_SSD:
                    self._has_ssd = True
        smart_disk_drive_members = self.smart_disk_drive
        if smart_disk_drive_members:
            ssd = self.smart_disk_drive.has_ssd
            if ssd:
                self._has_ssd = True
        unconfigured_disk_drive_mem = self.smart_unconfigured_disk_drive
        if unconfigured_disk_drive_mem:
            ssd = self.smart_unconfigured_disk_drive.has_ssd
            if ssd:
                self._has_ssd = True
        return self._has_ssd

    @property
    def has_rotational(self):
        """This property gets the media type of the disk as HDD"""
        drives_list = self.diskdrive
        if drives_list is not None:
            for drive_mem in drives_list:
                drive_uri = drive_mem.get('@odata.id')
                dr_obj = drives.Drives(self._conn, drive_uri,
                                       self.redfish_version)
                if dr_obj.media_type == sys_cons.MEDIA_TYPE_HDD:
                    self._has_rotational = True
        smart_disk_drive_members = self.smart_disk_drive
        if smart_disk_drive_members:
            hdd = self.smart_disk_drive.has_rotational
            if hdd:
                self._has_rotational = True
        unconfigured_disk_drive_mem = self.smart_unconfigured_disk_drive
        if unconfigured_disk_drive_mem:
            hdd = self.smart_unconfigured_disk_drive.has_rotational
            if hdd:
                self._has_rotational = True
        return self._has_rotational

    @property
    def has_nvme_ssd(self):
        """It is set to True if disk is SSD and protocol is NVMe"""
        drives_list = self.diskdrive
        if drives_list is not None:
            for drive_mem in drives_list:
                drive_uri = drive_mem.get('@odata.id')
                dr_obj = drives.Drives(self._conn, drive_uri,
                                       self.redfish_version)
                if dr_obj.media_type == sys_cons.MEDIA_TYPE_SSD:
                    if dr_obj.protocol == sys_cons.DRIVE_PROTOCOL_NVME:
                        self._has_nvme_ssd = True

    @property
    def logical_raid_level(self):
        self._logical_raid_level = []
        volume_members = self.volume
        if volume_members:
            self._logical_raid_level.append(self.volume.raid_levels)
        logical_drive_members = self.logical_drives
        if logical_drive_members:
            self._logical_raid_level.append(self.logical_drives.raid_levels)
            
