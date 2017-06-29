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

import logging

from sushy.resources import base

LOG = logging.getLogger(__name__)
class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')

class MemoryLocationField(base.CompositeField):
    channel = base.Field('Channel')
    memorycontroller = base.Field('MemoryController')
    slot = base.Field('Slot')
    socket = base.Field('Socket')

class Memory(base.ResourceBase):

    identity = base.Field('Id', required = True)
    """The memory identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    BusWidthBits = base.Field('BusWidthBits')
    capacity_mib = base.Field('CapacityMiB')
    device_locator = base.Field('DeviceLocator')
    memory_device_type = base.Field('MemoryDeviceType')
    memory_location = MemoryLocationField('MemoryLocation')
    memory_media = base.Field('MemoryMedia')
    memory_type = base.Field('MemoryType')
    operating_speed_mhz = base.Field('OperatingSpeedMhz')
    vendor_id = base.Field('VendorID')
    status = HealthStatusField('Status')
 
    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Memory

        :param connector: A Connector instance
        :param identity: The identity of the Memory resource.
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Memory, self).__init__(connector, identity,
                                                 redfish_version)


class MemoryCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Memory

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a Memoryollection

        :param connector: A Connector instance
        :param path: The canonical path to the Memory
            collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(MemoryCollection, self).__init__(connector, path,
                                               redfish_version)
