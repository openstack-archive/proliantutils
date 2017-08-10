# Copyright 2017 Hewlett Packard Enterprise Development LP
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

from proliantutils.redfish import utils


class SimpleStorage(base.ResourceBase):
    """This class represents the SimpleStorage resource"""

    identity = base.Field('Id', required=True)
    """The SimpleStorage identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    devices = base.Field('Devices')
    """The storage devices associated with this resource"""

    _maximum_size_bytes = None

    @property
    @utils.lazy_load_and_cache('_maximum_size_bytes')
    def maximum_size_bytes(self):
        """Gets the biggest disk drive

        :returns size in bytes.
        """
        return utils.max_safe(
            [device.get('CapacityBytes') for device in self.devices
             if device.get('CapacityBytes') is not None])

    def refresh(self):
        super(SimpleStorage, self).refresh()
        self._maximum_size_bytes = None


class SimpleStorageCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return SimpleStorage

    _maximum_size_bytes = None

    @property
    @utils.lazy_load_and_cache('_maximum_size_bytes')
    def maximum_size_bytes(self):
        """Gets the biggest disk drive

        :returns size in bytes.
        """
        return utils.max_safe([member.maximum_size_bytes
                               for member in self.get_members()])

    def refresh(self):
        super(SimpleStorageCollection, self).refresh()
        self._maximum_size_bytes = None
