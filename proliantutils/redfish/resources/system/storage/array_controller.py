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

import functools

from sushy.resources import base

from proliantutils import log
from proliantutils.redfish.resources.system.storage import logical_drive
from proliantutils.redfish.resources.system.storage import physical_drive
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)


class HPEArrayController(base.ResourceBase):
    """This class represents the HPEArrayControllers resource"""

    identity = base.Field('Id')
    """The identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    _logical_drives = None
    _physical_drives = None

    @property
    @utils.init_and_set_resource_if_not_already(
        logical_drive.HPELogicalDriveCollection,
        functools.partial(utils.get_subresource_path_by,
                          subresource_path=['Links', 'LogicalDrives']))
    def logical_drives(self):
        """Gets the resource HPELogicalDriveCollection of ArrayControllers"""
        return '_logical_drives'

    @property
    @utils.init_and_set_resource_if_not_already(
        physical_drive.HPEPhysicalDriveCollection,
        functools.partial(utils.get_subresource_path_by,
                          subresource_path=['Links', 'PhysicalDrives']))
    def physical_drives(self):
        """Gets the resource HPEPhysicalDriveCollection of ArrayControllers"""
        return '_physical_drives'

    def refresh(self):
        super(HPEArrayController, self).refresh()
        self._physical_drives = None
        self._logical_drives = None


class HPEArrayControllerCollection(base.ResourceCollectionBase):
    """This class represents the collection of HPEArrayControllers"""

    _logical_drives_maximum_size_mib = None
    _physical_drives_maximum_size_mib = None
    _has_ssd = None
    _has_rotational = None
    _logical_raid_levels = None
    _drive_rotational_speed_rpm = None

    @property
    def _resource_type(self):
        return HPEArrayController

    @property
    @utils.lazy_evaluate_for_attribute(
        '_logical_drives_maximum_size_mib', set_attribute_value=True)
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        return utils.max_safe([member.logical_drives.maximum_size_mib
                               for member in self.get_members()])

    @property
    @utils.lazy_evaluate_for_attribute(
        '_physical_drives_maximum_size_mib', set_attribute_value=True)
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.physical_drives.maximum_size_mib
                               for member in self.get_members()])

    @property
    @utils.lazy_evaluate_for_attribute('_has_ssd')
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        self._has_ssd = False
        for member in self.get_members():
            if member.physical_drives.has_ssd:
                self._has_ssd = True
                break

    @property
    @utils.lazy_evaluate_for_attribute('_has_rotational')
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        self._has_rotational = False
        for member in self.get_members():
            if member.physical_drives.has_rotational:
                self._has_rotational = True
                break

    @property
    @utils.lazy_evaluate_for_attribute('_logical_raid_levels')
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured
        """
        self._logical_raid_levels = set()
        for member in self.get_members():
            self._logical_raid_levels.update(
                member.logical_drives.logical_raid_levels)

    @property
    @utils.lazy_evaluate_for_attribute('_drive_rotational_speed_rpm')
    def drive_rotational_speed_rpm(self):
        """Gets the set of rotational speed of the HDD drives"""

        self._drive_rotational_speed_rpm = set()
        for member in self.get_members():
            self._drive_rotational_speed_rpm.update(
                member.physical_drives.drive_rotational_speed_rpm)

    def refresh(self):
        super(HPEArrayControllerCollection, self).refresh()
        self._logical_drives_maximum_size_mib = None
        self._physical_drives_maximum_size_mib = None
        self._has_ssd = None
        self._has_rotational = None
        self._logical_raid_levels = None
        self._drive_rotational_speed_rpm = None
