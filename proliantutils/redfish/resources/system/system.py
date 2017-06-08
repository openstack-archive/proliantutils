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
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import secure_boot
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


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """

    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)
    """Oem specific system extensibility actions"""

    _bios_settings = None  # ref to BIOSSettings instance
    _secure_boot = None  # ref to SecureBoot instance

    def refresh(self):
        super(HPESystem, self).refresh()
        self._bios_settings = None
        self._secure_boot = None

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
