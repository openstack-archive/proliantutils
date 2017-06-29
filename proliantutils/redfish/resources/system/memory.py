# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sushy.resources import base


class Memory(base.ResourceBase):

    identity = base.Field('Id')
    """The memory identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    memory_device_type = base.Field('MemoryDeviceType')
    memory_type = base.Field('MemoryType')


class MemoryCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Memory

    def memory_data(self):
        persistent_memory = False
        nvdimm_n = False
        logical_nvdimm_n = False
        members = self.get_members()
        for mem in members:
            if mem.memory_type == 'NVDIMM_N':
                persistent_memory = True
                nvdimm_n = True
            if mem.memory_device_type == 'Logical':
                logical_nvdimm_n = True
                break

        memory_types = {'persistent_memory': persistent_memory,
                        'nvdimm_n': nvdimm_n,
                        'logical_nvdimm_n': logical_nvdimm_n}
        return memory_types
