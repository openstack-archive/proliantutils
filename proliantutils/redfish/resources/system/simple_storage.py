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

import logging

from sushy.resources import base


LOG = logging.getLogger(__name__)


class SimpleStorage(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The SimpleStorage identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    devices = base.Field('Devices')
    """The storage devices associated with this resource"""


class SimpleStorageCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return SimpleStorage

    _maximum_size = None

    @property
    def maximum_size(self):
        """Gets the maximum disk size"""
        self._maximum_size = 0
        for mem in self.get_members():
            for device in mem.devices:
                self._maximum_size = (
                    max(int(self._maximum_size),
                        int(device.get("CapacityBytes") or 0)))
        return self._maximum_size

    def refresh(self):
        super(SimpleStorageCollection, self).refresh()
        self._maximum_size = None
