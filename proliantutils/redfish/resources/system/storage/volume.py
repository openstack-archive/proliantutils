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


class Volume(base.ResourceBase):
    """This class represents the Volume resource"""

    identity = base.Field('Id', required=True)
    """The processor identity string"""

    capacity_bytes = base.Field('CapacityBytes', adapter=int)
    """The size in bytes of this Volume"""


class VolumeCollection(base.ResourceCollectionBase):
    """This class represents the collection of Volume resource"""

    _maximum_size_bytes = None

    @property
    def _resource_type(self):
        return Volume

    @property
    def maximum_size_bytes(self):
        """Gets the biggest volume

        :returns size in bytes.
        """
        if self._maximum_size_bytes is None:
            self._maximum_size_bytes = (
                utils.max_safe([member.capacity_bytes
                               for member in self.get_members()]))
        return self._maximum_size_bytes

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        self._maximum_size_bytes = None
