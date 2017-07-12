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


class HPELogicalDrive(base.ResourceBase):

    identity = base.Field('Id')

    name = base.Field('Name')

    description = base.Field('Description')

    capacity_mib = base.Field('CapacityMiB', adapter=int)

    raid = base.Field('Raid')


class HPELogicalDriveCollection(base.ResourceCollectionBase):

    _maximum_size_mib = None

    @property
    def _resource_type(self):
        return HPELogicalDrive

    @property
    def maximum_size_mib(self):
        """Gets the biggest logical drive

        :returns size in MiB.
        """
        if self._maximum_size_mib is None:
            self._maximum_size_mib = (
                max([member.capacity_mib for member in self.get_members()]))
        return self._maximum_size_mib

    def refresh(self):
        super(HPELogicalDriveCollection, self).refresh()
        self._maximum_size_mib = None
