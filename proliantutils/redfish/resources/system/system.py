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

from sushy.resources import base
from sushy.resources.system import system

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import pci_device
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)


class PowerButtonActionField(base.CompositeField):
    allowed_values = base.Field('PushType@Redfish.AllowableValues',
                                adapter=list)

    target_uri = base.Field('target', required=True)


class HpeActionsField(base.CompositeField):
    computer_system_ext_powerbutton = (
        PowerButtonActionField('#HpeComputerSystemExt.PowerButton'))


class HpeOemUriField(base.CompositeField):
    pci_device_path = base.Field(['PCIDevices', '@odata.id'])


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """

    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)

    """Oem specific system extensibility actions"""

    _bios_settings = None

    _oem_path = HpeOemUriField(['Oem', 'Hpe', 'Links'])
    _pci_devices = None

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

    @property
    def pci_devices(self):
        """Provides PCI device

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._pci_devices is None:
            self._pci_devices = pci_device.PCIDeviceCollection(
                self._conn, self._oem_path.pci_device_path,
                redfish_version=self.redfish_version)

        return self._pci_devices
