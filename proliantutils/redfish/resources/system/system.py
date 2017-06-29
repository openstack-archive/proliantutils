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
from proliantutils.redfish.resources.system import mappings

LOG = log.get_logger(__name__)


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

     def _get_memory_collection_path(self):
          """Helper function to find the MemoryCollection path"""
        memory_col = self.json.get('Memory')
        if not memory_col:
            raise exceptions.MissingAttributeError(
                attribute='Memory', resource=self._path)
        return memory_col.get('@odata.id')

    @property
    def memory_data(self):
        persistent_memory = False
        nvdimm_n = False
        logical_nvdimm_n = False 
        mem_collection = Memory.MemoryCollection(
            self._conn, self._get_memory_collection_path(),
            redfish_version=self.redfish_version)
        members = mem_collection.get_members()
        for mem in members:
            if mem.MemoryType == 'NVDIMM-N':
                persistent_memory = True
                nvdimm_n = True
            if mem.MemoryDeviceType == 'Logical':
                logical_nvdimm_n = True
        memory_types = {'persistent_memory': persistent_memory,
                        'nvdimm_n': nvdimm_n,
                        'logical_nvdimm_n': logical_nvdimm_n}
        return memory_types
