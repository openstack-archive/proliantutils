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
from proliantutils.redfish.resources.system import ethernet_interface
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import pci_device
from proliantutils.redfish.resources.system import secure_boot
from proliantutils.redfish.resources.system import simple_storage
from proliantutils.redfish.resources.system import smart_storage
from proliantutils.redfish.resources.system import storage
from proliantutils.redfish import utils


LOG = log.get_logger(__name__)

PERSISTENT_BOOT_DEVICE_MAP = {
    'CDROM': sushy.BOOT_SOURCE_TARGET_CD,
    'NETWORK': sushy.BOOT_SOURCE_TARGET_PXE,
    'ISCSI': sushy.BOOT_SOURCE_TARGET_UEFI_TARGET,
    'HDD': sushy.BOOT_SOURCE_TARGET_HDD
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

    model = base.Field(['Model'])
    rom_version = base.Field(['Oem', 'Hpe', 'Bios', 'Current',
                             'VersionString'])
    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)
    """Oem specific system extensibility actions"""

    _bios_settings = None  # ref to BIOSSettings instance
    _secure_boot = None  # ref to SecureBoot instance

    _local_gb = None
    _simple_storages = None
    _storages = None
    _smart_storages = None
    _array_controllers = None

    _pci_devices = None
    _ethernet_interfaces = None

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
        """Property to provide reference to `BIOSSettings` instance

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
        device = PERSISTENT_BOOT_DEVICE_MAP.get(devices[0].upper())

        if device == sushy.BOOT_SOURCE_TARGET_UEFI_TARGET:
            if not mac:
                msg = ('Mac is needed for uefi iscsi boot')
                raise exception.IloInvalidInputError(msg)

            try:
                uefi_boot_string = (self.bios_settings.boot_settings.
                                    get_uefi_boot_string(mac))
            except sushy.exceptions.SushyError:
                msg = ('The BIOS Boot Settings was not found.')
                raise exception.IloError(msg)

            uefi_boot_settings = {
                'Boot': {'UefiTargetBootSourceOverride': uefi_boot_string}
            }
            self._conn.patch(self.path, data=uefi_boot_settings)
        elif device is None:
            device = sushy.BOOT_SOURCE_TARGET_NONE

        tenure = (sushy.BOOT_SOURCE_ENABLED_CONTINUOUS
                  if persistent else sushy.BOOT_SOURCE_ENABLED_ONCE)
        self.set_system_boot_source(device, enabled=tenure)

    @property
    def pci_devices(self):
        """Provides the collection of PCI devices

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._pci_devices is None:
            self._pci_devices = pci_device.PCIDeviceCollection(
                self._conn, utils.get_subresource_path_by(
                    self, ['Oem', 'Hpe', 'Links', 'PCIDevices']))
        return self._pci_devices

    @property
    def secure_boot(self):
        """Property to provide reference to `SecureBoot` instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._secure_boot is None:
            self._secure_boot = secure_boot.SecureBoot(
                self._conn, utils.get_subresource_path_by(self, 'SecureBoot'),
                redfish_version=self.redfish_version)

        return self._secure_boot

    def refresh(self):
        super(HPESystem, self).refresh()
        self._bios_settings = None
        self._pci_devices = None
        self._secure_boot = None
        self._ethernet_interfaces = None
        self._storages = None
        self._smart_storages = None
        self._simple_storages = None
        self._array_controllers = None

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
        if self._ethernet_interfaces is None:
            sub_res = 'EthernetInterfaces'
            self._ethernet_interfaces = (
                ethernet_interface.EthernetInterfaceCollection(
                    self._conn,
                    self._get_hpe_sub_resource_collection_path(sub_res),
                    redfish_version=self.redfish_version))
        return self._ethernet_interfaces

    @property
    def simple_storages(self):
        """This property gets the list of instances for SimpleStorages

        This property gets the list of instances for SimpleStorages
        :returns: a list of instances of SimpleStorages
        """

        if self._simple_storages is None:
            self._simple_storages = simple_storage.SimpleStorageCollection(
                self._conn, utils.get_subresource_path_by(
                    self, 'SimpleStorage'),
                redfish_version=self.redfish_version)
        return self._simple_storages

    @property
    def storages(self):
        """This property gets the list of instances for Storages

        This property gets the list of instances for Storages
        :returns: a list of instances of Storages
        """
        if self._storages is None:
            self._storages = storage.StorageCollection(
                self._conn, utils.get_subresource_path_by(self, 'Storage'),
                redfish_version=self.redfish_version)
        return self._storages

    @property
    def smart_storages(self):
        """This property gets the object for smart storage.

        This property gets the object for smart storage.
        There is no collection for smart storages.
        :returns: an instance of smart storage
        """
        if self._smart_storages is None:
            self._smart_storages = smart_storage.SmartStorage(
                self._conn, utils.get_subresource_path_by(
                    self, ['Oem', 'Hpe', 'Links', 'SmartStorage']),
                redfish_version=self.redfish_version)
        return self._smart_storages

    @property
    def array_controllers(self):
        """This property gets the list of instances for array controllers

        This property gets the list of instances for array controllers
        :returns: a list of instances of array controllers.
        """
        if self._array_controllers is None:
            path = self.smart_storages.links.array_controllers
            self._array_controllers = (
                array_controller.ArrayControllerCollection(
                    self._conn, path,
                    redfish_version=self.redfish_version))
        return self._array_controllers

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

        :returns the greatest size in GB.
        """
        size = 0
        disk_size = []
        log_size = []
        try:
            if self.array_controllers is not None:
                log_size.append(
                    self.array_controllers.maximum_logical_drive_size)
                disk_size.append(self.array_controllers.maximum_disk_size)
            if self.storages is not None:
                log_size.append(self.storages.maximum_volume_size)
                disk_size.append(self.storages.maximum_disk_size)
            if self.simple_storages is not None:
                disk_size.append(self.storages.maximum_disk_size)
        except exception.MissingAttributeError:
            pass

        if len(log_size) > 0:
            for val in log_size:
                if size < val:
                    size = val
        if size == 0:
            if len(disk_size) > 0:
                for val in disk_size:
                    if size < val:
                        size = val
        self._local_gb = size / (1024 * 1024 * 1024)
        return self._local_gb
