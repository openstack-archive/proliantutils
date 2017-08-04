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

    _maximum_size_mib = None
    _has_ssd = None
    _has_rotational = None
    _drive_rotational_speed_rpm = None

    @property
    def _resource_type(self):
        return HPEPhysicalDrive

    @property
    def maximum_size_mib(self):
        """Gets the biggest physical drive

        :returns size in MiB.
        """
        if self._maximum_size_mib is None:
            self._maximum_size_mib = (
                utils.max_safe([member.capacity_mib
                               for member in self.get_members()]))
        return self._maximum_size_mib

    @property
    def has_ssd(self):
        """Return true if the drive is ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self.get_members():
                if member.media_type == constants.MEDIA_TYPE_SSD:
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if the drive is HDD"""

        if self._has_rotational is None:
            self._has_rotational = False
            for member in self.get_members():
                if member.media_type == constants.MEDIA_TYPE_HDD:
                    self._has_rotational = True
                    break
        return self._has_rotational

    @property
    def drive_rotational_speed_rpm(self):
        """Gets the list of rotational speed of the HDD drives"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = []
            for member in self.get_members():
                if member.rotational_speed_rpm is not None:
                    self._drive_rotational_speed_rpm.append(
                        member.rotational_speed_rpm)
            self._drive_rotational_speed_rpm = list(set(
                self._drive_rotational_speed_rpm))
        return self._drive_rotational_speed_rpm

    def refresh(self):
        super(HPEPhysicalDriveCollection, self).refresh()
        self._maximum_size_mib = None
        self._has_ssd = None
        self._has_rotational = None
        self._drive_rotational_speed_rpm = None
