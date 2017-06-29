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

from sushy.resources import base

import collections
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import mappings

MemoryData = collections.namedtuple(
    'MemoryData', ['has_persistent_memory',
                   'has_nvdimm_n',
                   'has_logical_nvdimm_n'])


class Memory(base.ResourceBase):

    identity = base.Field('Id')
    """The memory identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    memory_device_type = base.MappedField('MemoryDeviceType',
                                          mappings.MEMORY_DEVICE_TYPE_MAP)
    memory_type = base.MappedField('MemoryType',
                                   mappings.MEMORY_TYPE_MAP)


class MemoryCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Memory

    def details(self):
        persistent_memory = False
        nvdimm_n = False
        logical_nvdimm_n = False
        for mem in self.get_members():
            if mem.memory_type == sys_cons.MEMORY_TYPE_NVDIMM_N:
                persistent_memory = True
                nvdimm_n = True
                if (mem.memory_device_type ==
                        sys_cons.MEMORY_DEVICE_TYPE_LOGICAL):
                    logical_nvdimm_n = True
                    break

        return MemoryData(has_persistent_memory=persistent_memory,
                          has_nvdimm_n=nvdimm_n,
                          has_logical_nvdimm_n=logical_nvdimm_n)
