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

from proliantutils.redfish.resources.system.storage import array_controller
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HPESmartStorage(base.ResourceBase):
    """This class represents the HPE OEM SmartStorage resource"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    _array_controllers = None
    _logical_drives_maximum_size_mib = None
    _physical_drives_maximum_size_mib = None
    _has_ssd = None
    _has_rotational = None
    _logical_raid_levels = None
    _drive_rotational_speed_rpm = None

    @property
    def array_controllers(self):
        """This property gets the list of instances for array controllers

        This property gets the list of instances for array controllers
        :returns: a list of instances of array controllers.
        """
        if self._array_controllers is None:
            self._array_controllers = (
                array_controller.HPEArrayControllerCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'ArrayControllers']),
                    redfish_version=self.redfish_version))
        return self._array_controllers

    @property
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :Returns the size in MiB.
        """
        if self._logical_drives_maximum_size_mib is None:
            self._logical_drives_maximum_size_mib = (
                utils.max_safe(
                    [member.logical_drives.maximum_size_mib
                     for member in self.array_controllers.get_members()]))
        return self._logical_drives_maximum_size_mib

    @property
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk drive

        :Returns the size in MiB.
        """
        if self._physical_drives_maximum_size_mib is None:
            self._physical_drives_maximum_size_mib = (
                utils.max_safe(
                    [member.physical_drives.maximum_size_mib
                     for member in self.array_controllers.get_members()]))
        return self._physical_drives_maximum_size_mib

    @property
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self.array_controllers.get_members():
                if member.physical_drives.has_ssd:
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is HDD"""

        if self._has_rotational is None:
            self._has_rotational = False
            for member in self.array_controllers.get_members():
                if member.physical_drives.has_rotational:
                    self._has_rotational = True
                    break
        return self._has_rotational

    @property
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured.
        """
        if self._logical_raid_levels is None:
            self._logical_raid_levels = set()
            for member in self.array_controllers.get_members():
                for raid_level in member.logical_drives.logical_raid_levels:
                    self._logical_raid_levels.add(raid_level)
        return self._logical_raid_levels

    @property
    def drive_rotational_speed_rpm(self):
        """Gets the list of rotational speed of the HDD drives"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = set()
            for member in self.array_controllers.get_members():
                for speed in (
                        member.physical_drives.drive_rotational_speed_rpm):
                    self._drive_rotational_speed_rpm.add(speed)
        return self._drive_rotational_speed_rpm

    def refresh(self):
        super(HPESmartStorage, self).refresh()
        self._logical_drives_maximum_size_mib = None
        self._physical_drives_maximum_size_mib = None
        self._array_controllers = None
        self._has_ssd = None
        self._has_rotational = None
        self._logical_raid_levels = None
        self._drive_rotational_speed_rpm = None
