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

from proliantutils import log
from proliantutils.redfish.resources.system.storage import array_controller
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)


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
    @utils.lazy_load_and_cache('_array_controllers')
    def array_controllers(self):
        """Gets the HPEArrayControllerCollection instance"""
        return array_controller.HPEArrayControllerCollection(
            self._conn, utils.get_subresource_path_by(
                self, ['Links', 'ArrayControllers']),
            redfish_version=self.redfish_version)

    @property
    @utils.lazy_load_and_cache('_logical_drives_maximum_size_mib')
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :Returns the size in MiB.
        """
        return self.array_controllers.logical_drives_maximum_size_mib

    @property
    @utils.lazy_load_and_cache('_physical_drives_maximum_size_mib')
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk drive

        :Returns the size in MiB.
        """
        return self.array_controllers.physical_drives_maximum_size_mib

    @property
    @utils.lazy_load_and_cache('_has_ssd')
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is SSD"""
        return self.array_controllers.has_ssd

    @property
    @utils.lazy_load_and_cache('_has_rotational')
    def has_rotational(self):
        """Return true if any of the drive under ArrayControllers is HDD"""
        return self.array_controllers.has_rotational

    @property
    @utils.lazy_load_and_cache('_logical_raid_levels')
    def logical_raid_levels(self):
        """Gets the raid level for each logical volume

        :returns the set of list of raid levels configured.
        """
        return self.array_controllers.logical_raid_levels

    @property
    @utils.lazy_load_and_cache('_drive_rotational_speed_rpm')
    def drive_rotational_speed_rpm(self):
        """Gets the list of rotational speed of the HDD drives"""
        return self.array_controllers.drive_rotational_speed_rpm

    def refresh(self):
        super(HPESmartStorage, self).refresh()
        self._logical_drives_maximum_size_mib = None
        self._physical_drives_maximum_size_mib = None
        self._array_controllers = None
        self._has_ssd = None
        self._has_rotational = None
        self._logical_raid_levels = None
        self._drive_rotational_speed_rpm = None
