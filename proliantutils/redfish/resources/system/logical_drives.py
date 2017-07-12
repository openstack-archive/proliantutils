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


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')


class LogicalDrive(base.ResourceBase):

    identity = base.Field('Id')

    name = base.Field('Name')

    description = base.Field('Description')

    status = HealthStatusField('Status')

    capacity_mib = base.Field('CapacityMiB')

    raid = base.Field('Raid')


class LogicalDriveCollection(base.ResourceCollectionBase):

    _maximum_size = None

    @property
    def _resource_type(self):
        return LogicalDrive

    @property
    def maximum_size(self):
        """Gets the biggest logical drive

        :returns size in bytes.
        """
        if self._maximum_size is None:
            self._maximum_size = 0
            for mem in self.get_members():
                if self._maximum_size < mem.capacity_mib:
                    self._maximum_size = mem.capacity_mib
        return (self._maximum_size * 1024 * 1024)

    def refresh(self):
        super(LogicalDriveCollection, self).refresh()
        self._maximum_size = None
