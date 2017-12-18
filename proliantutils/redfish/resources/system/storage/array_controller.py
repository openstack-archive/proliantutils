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

from proliantutils.redfish.resources.system.storage import logical_drive
from proliantutils.redfish.resources.system.storage import physical_drive
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HPEArrayController(base.ResourceBase):
    """This class represents the HPEArrayControllers resource"""

    identity = base.Field('Id')
    """The identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    model = base.Field('Model')
    """Controller model"""

    location = base.Field('Location')
    """Controller slot location"""

    _logical_drives = None
    _physical_drives = None

    @property
    def logical_drives(self):
        """Gets the resource HPELogicalDriveCollection of ArrayControllers"""

        if self._logical_drives is None:
            self._logical_drives = (
                logical_drive.HPELogicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'LogicalDrives']),
                    redfish_version=self.redfish_version))

        self._logical_drives.refresh(force=False)
        return self._logical_drives

    @property
    def physical_drives(self):
        """Gets the resource HPEPhysicalDriveCollection of ArrayControllers"""

        if self._physical_drives is None:
            self._physical_drives = (
                physical_drive.HPEPhysicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'PhysicalDrives']),
                    redfish_version=self.redfish_version))

        self._physical_drives.refresh(force=False)
        return self._physical_drives

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        super(HPEArrayController, self)._do_refresh(force)

        if self._physical_drives is not None:
            self._physical_drives.invalidate(force)
        if self._logical_drives is not None:
            self._logical_drives.invalidate(force)


class HPEArrayControllerCollection(base.ResourceCollectionBase):
    """This class represents the collection of HPEArrayControllers"""

    _logical_drives_maximum_size_mib = None
    _physical_drives_maximum_size_mib = None
    _has_ssd = None
    _has_rotational = None
    _logical_raid_levels = None
    _drive_rotational_speed_rpm = None
    _get_models = None
    _get_default_controller = None

    @property
    def _resource_type(self):
        return HPEArrayController

    @property
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        if self._logical_drives_maximum_size_mib is None:
            self._logical_drives_maximum_size_mib = (
                utils.max_safe([member.logical_drives.maximum_size_mib
                               for member in self.get_members()]))
        return self._logical_drives_maximum_size_mib

    @property
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._physical_drives_maximum_size_mib is None:
            self._physical_drives_maximum_size_mib = (
                utils.max_safe([member.physical_drives.maximum_size_mib
                               for member in self.get_members()]))
        return self._physical_drives_maximum_size_mib

    @property
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self.get_members():
                if member.physical_drives.has_ssd:
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        if self._has_rotational is None:
            self._has_rotational = False
            for member in self.get_members():
                if member.physical_drives.has_rotational:
                    self._has_rotational = True
                    break
        return self._has_rotational

    @property
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured
        """
        if self._logical_raid_levels is None:
            self._logical_raid_levels = set()
            for member in self.get_members():
                self._logical_raid_levels.update(
                    member.logical_drives.logical_raid_levels)
        return self._logical_raid_levels

    @property
    def drive_rotational_speed_rpm(self):
        """Gets the set of rotational speed of the HDD drives"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = set()
            for member in self.get_members():
                self._drive_rotational_speed_rpm.update(
                    member.physical_drives.drive_rotational_speed_rpm)
        return self._drive_rotational_speed_rpm

    @property
    def get_default_controller(self):
        """Gets default array controller

        :returns default array controller
        """
        if self._get_default_controller is None:
            self._get_default_controller = self.get_members()[0]
        return self._get_default_controller

    def array_controller_by_location(self, location):
        """Returns array controller instance by location

        :returns Instance of array controller
        """
        for member in self.get_members():
            if member.location == location:
                return member

    def array_controller_by_model(self, model):
        """Returns array controller instance by model

        :returns Instance of array controller
        """
        for member in self.get_members():
            if member.model == model:
                return member

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        self._logical_drives_maximum_size_mib = None
        self._physical_drives_maximum_size_mib = None
        self._has_ssd = None
        self._has_rotational = None
        self._logical_raid_levels = None
        self._drive_rotational_speed_rpm = None
        self._get_models = None
        self._get_default_controller = None
