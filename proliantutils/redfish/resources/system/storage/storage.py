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

from proliantutils.redfish.resources.system.storage import constants
from proliantutils.redfish.resources.system.storage import drive as sys_drives
from proliantutils.redfish.resources.system.storage \
    import volume as sys_volumes
from proliantutils.redfish import utils

LOG = logging.getLogger(__name__)


class Storage(base.ResourceBase):
    """This class represents the Storage resource"""

    identity = base.Field('Id', required=True)
    """The Storage identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    drives = base.Field('Drives')
    """The set of drives attached to the storage controllers"""

    @property
    @sushy_utils.cache_it
    def volumes(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        return sys_volumes.VolumeCollection(
            self._conn, utils.get_subresource_path_by(self, 'Volumes'),
            redfish_version=self.redfish_version)

    def _drives_list(self):
        """Gets the list of drives

        :return a list of drives.
        """
        drives_list = []
        for member in self.drives:
            drives_list.append(sys_drives.Drive(
                self._conn, member.get('@odata.id'), self.redfish_version))
        return drives_list

    @property
    @sushy_utils.cache_it
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.capacity_bytes
                               for member in self._drives_list()])

    @property
    @sushy_utils.cache_it
    def has_ssd(self):
        """Return true if any of the drive is ssd"""
        for member in self._drives_list():
            if member.media_type == constants.MEDIA_TYPE_SSD:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_rotational(self):
        """Return true if any of the drive is HDD"""
        for member in self._drives_list():
            if member.media_type == constants.MEDIA_TYPE_HDD:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_nvme_ssd(self):
        """Return True if the drive is SSD and protocol is NVMe"""
        for member in self._drives_list():
            if (member.media_type == constants.MEDIA_TYPE_SSD and
                    member.protocol == constants.PROTOCOL_NVMe):
                return True
        return False

    @property
    @sushy_utils.cache_it
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""

        drv_rot_speed_rpm = set()
        for member in self._drives_list():
            if member.rotation_speed_rpm is not None:
                drv_rot_speed_rpm.add(member.rotation_speed_rpm)
        return drv_rot_speed_rpm


class StorageCollection(base.ResourceCollectionBase):
    """This class represents the collection of Storage resource"""

    @property
    def _resource_type(self):
        return Storage

    @property
    @sushy_utils.cache_it
    def volumes_maximum_size_bytes(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        return utils.max_safe([member.volumes.maximum_size_bytes
                               for member in self.get_members()])

    @property
    @sushy_utils.cache_it
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.drives_maximum_size_bytes
                               for member in self.get_members()])

    @property
    @sushy_utils.cache_it
    def has_ssd(self):
        """Return true if Storage has any drive as ssd"""
        for member in self.get_members():
            if member.has_ssd:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_rotational(self):
        """Return true if Storage has any drive as HDD"""
        for member in self.get_members():
            if member.has_rotational:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def has_nvme_ssd(self):
        """Return True if Storage has SSD drive and protocol is NVMe"""
        for member in self.get_members():
            if member.has_nvme_ssd:
                return True
        return False

    @property
    @sushy_utils.cache_it
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""
        drv_rot_speed_rpm = set()
        for member in self.get_members():
            drv_rot_speed_rpm.update(member.drive_rotational_speed_rpm)
        return drv_rot_speed_rpm
