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
from sushy import utils as sushy_utils

from proliantutils.redfish import utils

from proliantutils.redfish.resources.system.storage import constants
from proliantutils.redfish.resources.system.storage import mappings


class HPEPhysicalDrive(base.ResourceBase):
    """This class represents the HPEPhysicalDrives resource"""

    identity = base.Field('Id', required=True)

    name = base.Field('Name')

    description = base.Field('Description')

    capacity_mib = base.Field('CapacityMiB', adapter=int)

    media_type = base.MappedField('MediaType', mappings.MEDIA_TYPE_MAP)

    rotational_speed_rpm = base.Field('RotationalSpeedRpm', adapter=int)


class HPEPhysicalDriveCollection(base.ResourceCollectionBase):
    """This class represents the collection of HPEPhysicalDrives resource"""

    @property
    def _resource_type(self):
        return HPEPhysicalDrive

    @property
    @sushy_utils.cache_it
    def maximum_size_mib(self):
        """Gets the biggest physical drive

        :returns size in MiB.
        """
        return utils.max_safe([member.capacity_mib
                               for member in self.get_members()])

    @property
    @sushy_utils.cache_it
    def has_ssd(self):
        """Return true if the drive is ssd"""
        for member in self.get_members():
            if member.media_type == constants.MEDIA_TYPE_SSD:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_rotational(self):
        """Return true if the drive is HDD"""
        for member in self.get_members():
            if member.media_type == constants.MEDIA_TYPE_HDD:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def drive_rotational_speed_rpm(self):
        """Gets the set of rotational speed of the HDD drives"""
        drv_rot_speed_rpm = set()
        for member in self.get_members():
            if member.rotational_speed_rpm is not None:
                drv_rot_speed_rpm.add(member.rotational_speed_rpm)
        return drv_rot_speed_rpm
