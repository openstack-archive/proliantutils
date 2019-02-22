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

from sushy import utils as sushy_utils

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

    @property
    @sushy_utils.cache_it
    def logical_drives(self):
        """Gets the resource HPELogicalDriveCollection of ArrayControllers"""

        return logical_drive.HPELogicalDriveCollection(
            self._conn, utils.get_subresource_path_by(
                self, ['Links', 'LogicalDrives']),
            redfish_version=self.redfish_version)

    @property
    @sushy_utils.cache_it
    def physical_drives(self):
        """Gets the resource HPEPhysicalDriveCollection of ArrayControllers"""
        return physical_drive.HPEPhysicalDriveCollection(
            self._conn, utils.get_subresource_path_by(
                self, ['Links', 'PhysicalDrives']),
            redfish_version=self.redfish_version)


class HPEArrayControllerCollection(base.ResourceCollectionBase):
    """This class represents the collection of HPEArrayControllers"""

    @property
    def _resource_type(self):
        return HPEArrayController

    @property
    @sushy_utils.cache_it
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        return utils.max_safe([member.logical_drives.maximum_size_mib
                               for member in self.get_members()])

    @property
    @sushy_utils.cache_it
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.physical_drives.maximum_size_mib
                               for member in self.get_members()])

    @property
    @sushy_utils.cache_it
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""
        for member in self.get_members():
            if member.physical_drives.has_ssd:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is ssd"""
        for member in self.get_members():
            if member.physical_drives.has_rotational:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured
        """
        lg_raid_lvls = set()
        for member in self.get_members():
            lg_raid_lvls.update(member.logical_drives.logical_raid_levels)
        return lg_raid_lvls

    @property
    @sushy_utils.cache_it
    def drive_rotational_speed_rpm(self):
        """Gets the set of rotational speed of the HDD drives"""

        drv_rot_speed_rpm = set()
        for member in self.get_members():
            drv_rot_speed_rpm.update(
                member.physical_drives.drive_rotational_speed_rpm)
        return drv_rot_speed_rpm

    @property
    @sushy_utils.cache_it
    def get_default_controller(self):
        """Gets default array controller

        :returns default array controller
        """
        return self.get_members()[0]

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

    def get_all_controllers_model(self):
        """Returns list of model of all array controllers

        :returns List of model of array controllers
        """
        models = []
        for member in self.get_members():
            models.append(member.model)
        return models