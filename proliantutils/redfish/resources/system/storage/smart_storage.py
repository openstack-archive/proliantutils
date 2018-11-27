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
from sushy import utils as sushy_utils

from proliantutils.redfish.resources.system.storage import array_controller
from proliantutils.redfish import utils

LOG = logging.getLogger(__name__)


class HPESmartStorage(base.ResourceBase):
    """This class represents the HPE OEM SmartStorage resource"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    @property
    @sushy_utils.cache_it
    def array_controllers(self):
        """This property gets the list of instances for array controllers

        This property gets the list of instances for array controllers
        :returns: a list of instances of array controllers.
        """
        return array_controller.HPEArrayControllerCollection(
            self._conn, utils.get_subresource_path_by(
                self, ['Links', 'ArrayControllers']),
            redfish_version=self.redfish_version)

    @property
    @sushy_utils.cache_it
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :Returns the size in MiB.
        """
        return self.array_controllers.logical_drives_maximum_size_mib

    @property
    @sushy_utils.cache_it
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk drive

        :Returns the size in MiB.
        """
        return self.array_controllers.physical_drives_maximum_size_mib

    @property
    @sushy_utils.cache_it
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""
        return self.array_controllers.has_ssd

    @property
    @sushy_utils.cache_it
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is HDD"""
        return self.array_controllers.has_rotational

    @property
    @sushy_utils.cache_it
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured.
        """
        return self.array_controllers.logical_raid_levels

    @property
    @sushy_utils.cache_it
    def drive_rotational_speed_rpm(self):
        """Gets the list of rotational speed of the HDD drives"""
        return self.array_controllers.drive_rotational_speed_rpm
