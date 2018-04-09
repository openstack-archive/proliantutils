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
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants
from proliantutils.redfish.resources.system import ethernet_interface
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import memory
from proliantutils.redfish.resources.system import pci_device
from proliantutils.redfish.resources.system import secure_boot
from proliantutils.redfish.resources.system.storage import simple_storage
from proliantutils.redfish.resources.system.storage import \
    smart_storage as hpe_smart_storage
from proliantutils.redfish.resources.system.storage import storage

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


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """

    model = base.Field(['Model'])
    rom_version = base.Field(['Oem', 'Hpe', 'Bios', 'Current',
                             'VersionString'])
    uefi_target_override_devices = (base.Field([
        'Boot',
        'UefiTargetBootSourceOverride@Redfish.AllowableValues'],
        adapter=list))
    supported_boot_mode = base.MappedField(
        ['Oem', 'Hpe', 'Bios', 'UefiClass'], mappings.SUPPORTED_BOOT_MODE,
        default=constants.SUPPORTED_LEGACY_BIOS_ONLY)
    """System supported boot mode."""
    postState = base.MappedField(
        ['Oem', 'Hpe', 'PostState'], mappings.POST_STATE_MAP,
        default=constants.POST_STATE_NULL)
    """System POST state"""

    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)
    """Oem specific system extensibility actions"""

    _bios_settings = None  # ref to BIOSSettings instance
    _secure_boot = None  # ref to SecureBoot instance

    _smart_storage = None  # SmartStorage instance
    _simple_storages = None  # SimpleStorage instance
    _storages = None  # Storage instance
    _pci_devices = None  # PCIDevice instance

    _ethernet_interfaces = None  # EthernetInterface instance

    _memory = None  # Memory instance

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

        self._bios_settings.refresh(force=False)
        return self._bios_settings

    def update_persistent_boot(self, devices=[], persistent=False):
        """Changes the persistent boot device order in BIOS boot mode for host

        Note: It uses first boot device from the devices and ignores rest.

        :param devices: ordered list of boot devices
        :param persistent: Boolean flag to indicate if the device to be set as
                           a persistent boot device
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the given input is not valid.
        """
        device = PERSISTENT_BOOT_DEVICE_MAP.get(devices[0].upper())
        if device == sushy.BOOT_SOURCE_TARGET_UEFI_TARGET:
            try:
                uefi_devices = self.uefi_target_override_devices
                iscsi_device = None
                for uefi_device in uefi_devices:
                    if uefi_device is not None and 'iSCSI' in uefi_device:
                        iscsi_device = uefi_device
                        break

                if iscsi_device is None:
                    msg = 'No UEFI iSCSI bootable device found on system.'
                    raise exception.IloError(msg)

            except sushy.exceptions.SushyError as e:
                msg = ('Unable to get uefi target override devices. '
                       'Error %s') % (str(e))
                raise exception.IloError(msg)

            uefi_boot_settings = {
                'Boot': {'UefiTargetBootSourceOverride': iscsi_device}
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

        self._pci_devices.refresh(force=False)
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

        self._secure_boot.refresh(force=False)
        return self._secure_boot

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        super(HPESystem, self)._do_refresh(force)

        if self._bios_settings is not None:
            self._bios_settings.invalidate(force)
        if self._pci_devices is not None:
            self._pci_devices.invalidate(force)
        if self._secure_boot is not None:
            self._secure_boot.invalidate(force)
        if self._ethernet_interfaces is not None:
            self._ethernet_interfaces.invalidate(force)
        if self._smart_storage is not None:
            self._smart_storage.invalidate(force)
        if self._storages is not None:
            self._storages.invalidate(force)
        if self._simple_storages is not None:
            self._simple_storages.invalidate(force)
        if self._memory is not None:
            self._memory.invalidate(force)

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

        self._ethernet_interfaces.refresh(force=False)
        return self._ethernet_interfaces

    @property
    def smart_storage(self):
        """This property gets the object for smart storage.

        This property gets the object for smart storage.
        There is no collection for smart storages.
        :returns: an instance of smart storage
        """
        if self._smart_storage is None:
            self._smart_storage = hpe_smart_storage.HPESmartStorage(
                self._conn, utils.get_subresource_path_by(
                    self, ['Oem', 'Hpe', 'Links', 'SmartStorage']),
                redfish_version=self.redfish_version)

        self._smart_storage.refresh(force=False)
        return self._smart_storage

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

        self._storages.refresh(force=False)
        return self._storages

    @property
    def simple_storages(self):
        """This property gets the list of instances for SimpleStorages

        :returns: a list of instances of SimpleStorages
        """
        if self._simple_storages is None:
            self._simple_storages = simple_storage.SimpleStorageCollection(
                self._conn, utils.get_subresource_path_by(
                    self, 'SimpleStorage'),
                redfish_version=self.redfish_version)

        self._simple_storages.refresh(force=False)
        return self._simple_storages

    @property
    def memory(self):
        """Property to provide reference to `MemoryCollection` instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._memory is None:
            self._memory = memory.MemoryCollection(
                self._conn, utils.get_subresource_path_by(
                    self, 'Memory'),
                redfish_version=self.redfish_version)

        self._memory.refresh(force=False)
        return self._memory
