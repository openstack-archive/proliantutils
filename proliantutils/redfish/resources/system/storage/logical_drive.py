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

from proliantutils.redfish.resources.system.storage import mappings


class HPELogicalDrive(base.ResourceBase):
    """This class represents the LogicalDrives resource"""

    identity = base.Field('Id')

    name = base.Field('Name')

    description = base.Field('Description')

    capacity_mib = base.Field('CapacityMiB', adapter=int)

    raid = base.MappedField('Raid', mappings.RAID_LEVEL_MAP)


class HPELogicalDriveCollection(base.ResourceCollectionBase):
    """This class represents the collection of LogicalDrives resource"""

    _maximum_size_mib = None
    _logical_raid_levels = None

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
                utils.max_safe([member.capacity_mib
                               for member in self.get_members()]))
        return self._maximum_size_mib

    @property
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured.
        """
        if self._logical_raid_levels is None:
            self._logical_raid_levels = set()
            for member in self.get_members():
                self._logical_raid_levels.add(
                    mappings.RAID_LEVEL_MAP_REV.get(member.raid))
        return self._logical_raid_levels

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        self._maximum_size_mib = None
        self._logical_raid_levels = None
