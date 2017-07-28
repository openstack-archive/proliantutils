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

from proliantutils.redfish.resources.system.storage import drive as sys_drives
from proliantutils.redfish.resources.system.storage \
    import volume as sys_volumes
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class Storage(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The Storage identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    storage_controllers = base.Field('StorageControllers')
    """The set of storage controllers"""

    drives = base.Field('Drives')
    """The set of drives attached to the storage controllers"""

    _volumes = None
    _drives_list = None
    _drives_maximum_size_bytes = None
    _nvme_storage_controller = None
    _has_ssd = None
    _has_nvme_ssd = None
    _drive_rotational_speed_rpm = None
    _has_rotational = None    

    @property
    def volumes(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        if self._volumes is None:
            self._volumes = sys_volumes.VolumeCollection(
                self._conn, utils.get_subresource_path_by(self, 'Volumes'),
                redfish_version=self.redfish_version)
        return self._volumes

    @property
    def drives_list(self):
        """This property prepares the list of drives

        :return a list of drives.
        """
        if self._drives_list is None:
            self._drives_list = []
            for member in self.drives:
                self._drives_list.append(sys_drives.Drive(
                    self._conn, member.get('@odata.id'),
                    self.redfish_version))
        return self._drives_list

    @property
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._drives_maximum_size_bytes is None:
            self._drives_maximum_size_bytes = (
                max([member.capacity_bytes
                    for member in self.drives_list]))
        return self._drives_maximum_size_bytes

    @property
    def has_ssd(self):
        """Return true if the drive is ssd"""

        if self._has_ssd is None:
            for member in self.drive:
                if member.media_type == 'SSD':
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if the drive is ssd"""

        if self._has_rotational is None:
            for member in self.drive:
                if member.media_type == 'HDD':
                    self._has_rotational = True
        return self._has_rotational

    @property
    def drive_rotational_speed_rpm(self):
        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = {}
            for member in self.drive:
                var = ('drive_rotational' +
                       str(member.rotational_speed_rpm) + 'rpm')
                self._drive_rotational_speed_rpm.update({var: 'true'})
        return self._drive_rotational_speed_rpm

    @property
    def nvme_storage_controller(self):
        if self._nvme_storage_controller is None:
            for member in self.storage_controllers:
                if 'NVMe' in member.get('SupportedDeviceProtocols'):
                    self._nvme_storage_controller = True
                    break
        return self._nvme_storage_controller 

    @property
    def has_nvme_ssd(self):
        """Return true if the drive is ssd"""

        if self._has_nvme_ssd is None:
            for member in self.drive:
                if (member.media_type == 'SSD' and
                        member.nvme_storage_controller):
                    self._has_nvme_ssd = True
        return self._has_nvme_ssd


class StorageCollection(base.ResourceCollectionBase):

    _volumes_maximum_size_bytes = None
    _drives_maximum_size_bytes = None
    _drive_rotational_speed_rpm = None
    _has_rotational = None
    _has_ssd = None
    _has_nvme_ssd = None
    _logical_raid_level = None

    @property
    def _resource_type(self):
        return Storage

    @property
    def volumes_maximum_size_bytes(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        if self._volumes_maximum_size_bytes is None:
            self._volumes_maximum_size_bytes = (
                max([member.volumes.maximum_size_bytes
                    for member in self.get_members()]))
        return self._volumes_maximum_size_bytes

    @property
    def logical_raid_level(self):
        """Gets the Raid level for all logical volumes

        :returns the dictionary of such logical raid levels.
        """
        if self._logical_raid_level is None:
            self._logical_raid_level = {}
            for member in self.get_members():
                self._logical_raid_level.update(
                    member.volumes.logical_raid_level)
        return self._logical_raid_level

    @property
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._drives_maximum_size_bytes is None:
            self._drives_maximum_size_bytes = (
                max([member.drives_maximum_size_bytes
                    for member in self.get_members()]))
        return self._drives_maximum_size_bytes

    @property
    def has_ssd(self):
        """Return true if the drive is ssd"""

        if self._has_ssd is None:
            self._has_ssd = (
                member.has_ssd is not None
                for member in self.get_members())
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if the drive is HDD"""

        if self._has_rotational is None:
            self._has_rotational = (
                member.has_rotational is not None
                for member in self.get_members())
        return self._has_rotational

    @property
    def drive_rotational_speed_rpm(self):
        """Gets dictionary of rotational speed of the disks"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = (
                member.drive_rotational_speed_rpm
                for member in self.get_members())
        return self._drive_rotational_speed_rpm

    @property
    def has_nvme_ssd(self):
        """Return true if the drive is ssd"""

        if self._has_nvme_ssd is None:
            self._has_nvme_ssd = (
                member.has_nvme_ssd is not None
                for member in self.get_members())
        return self._has_nvme_ssd

    def refresh(self):
        super(StorageCollection, self).refresh()
        self._volumes_maximum_size_bytes = None
        self._drives_maximum_size_bytes = None
        self._drive_rotational_speed_rpm = None
        self._has_rotational = None
        self._has_ssd = None
        self._has_nvme_ssd = None
        self._logical_raid_level = None
