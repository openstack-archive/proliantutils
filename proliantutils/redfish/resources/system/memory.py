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


class HealthStatusField(base.CompositeField):

    health = base.Field('Health')
    state = base.Field('State')


class MemoryLocationField(base.CompositeField):

    channel = base.Field('Channel')
    memorycontroller = base.Field('MemoryController')
    slot = base.Field('Slot')
    socket = base.Field('Socket')


class Memory(base.ResourceBase):

    identity = base.Field('Id')
    """The memory identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    bus_width_bits = base.Field('BusWidthBits')
    capacity_mib = base.Field('CapacityMiB')
    device_locator = base.Field('DeviceLocator')
    memory_device_type = base.Field('MemoryDeviceType')
    memory_location = MemoryLocationField('MemoryLocation')
    memory_media = base.Field('MemoryMedia')
    memory_type = base.Field('MemoryType')
    operating_speed_mhz = base.Field('OperatingSpeedMhz')
    vendor_id = base.Field('VendorID')
    status = HealthStatusField('Status')


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

        memory_types = {'persistent_memory': persistent_memory,
                        'nvdimm_n': nvdimm_n,
                        'logical_nvdimm_n': logical_nvdimm_n}
        return memory_types
