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
from proliantutils.redfish.resources.system.storage import constants
from proliantutils.redfish.resources.system.storage import drive as sys_drives
from proliantutils.redfish.resources.system.storage \
    import volume as sys_volumes
from proliantutils.redfish import utils


LOG = log.get_logger(__name__)


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

    _volumes = None
    _drives_maximum_size_bytes = None
    _has_ssd = None
    _has_rotational = None
    _has_nvme_ssd = None
    _drive_rotational_speed_rpm = None

    @property
    @utils.lazy_load_and_cache('_volumes')
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
    @utils.lazy_load_and_cache('_drives_maximum_size_bytes')
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.capacity_bytes
                               for member in self._drives_list()])

    @property
    @utils.lazy_load_and_cache('_has_ssd', should_set_attribute=False)
    def has_ssd(self):
        """Return true if any of the drive is SSD"""
        self._has_ssd = False
        for member in self._drives_list():
            if member.media_type == constants.MEDIA_TYPE_SSD:
                self._has_ssd = True
                break

    @property
    @utils.lazy_load_and_cache('_has_rotational', should_set_attribute=False)
    def has_rotational(self):
        """Return true if any of the drive is HDD"""
        self._has_rotational = False
        for member in self._drives_list():
            if member.media_type == constants.MEDIA_TYPE_HDD:
                self._has_rotational = True
                break

    @property
    @utils.lazy_load_and_cache('_has_nvme_ssd', should_set_attribute=False)
    def has_nvme_ssd(self):
        """Return True if the drive is SSD and protocol is NVMe"""
        self._has_nvme_ssd = False
        for member in self._drives_list():
            if (member.media_type == constants.MEDIA_TYPE_SSD and
                    member.protocol == constants.PROTOCOL_NVMe):
                self._has_nvme_ssd = True

    @property
    @utils.lazy_load_and_cache(
        '_drive_rotational_speed_rpm', should_set_attribute=False)
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""
        self._drive_rotational_speed_rpm = set()
        for member in self._drives_list():
            if member.rotation_speed_rpm is not None:
                self._drive_rotational_speed_rpm.add(
                    member.rotation_speed_rpm)

    def refresh(self):
        super(Storage, self).refresh()
        self._drives_maximum_size_bytes = None
        self._volumes = None
        self._has_ssd = None
        self._has_rotational = None
        self._has_nvme_ssd = None
        self._drive_rotational_speed_rpm = None


class StorageCollection(base.ResourceCollectionBase):
    """This class represents the collection of Storage resource"""

    _volumes_maximum_size_bytes = None
    _drives_maximum_size_bytes = None
    _has_ssd = None
    _has_rotational = None
    _has_nvme_ssd = None
    _drive_rotational_speed_rpm = None

    @property
    def _resource_type(self):
        return Storage

    @property
    @utils.lazy_load_and_cache('_volumes_maximum_size_bytes')
    def volumes_maximum_size_bytes(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        return utils.max_safe([member.volumes.maximum_size_bytes
                               for member in self.get_members()])

    @property
    @utils.lazy_load_and_cache('_drives_maximum_size_bytes')
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        return utils.max_safe([member.drives_maximum_size_bytes
                               for member in self.get_members()])

    @property
    @utils.lazy_load_and_cache('_has_ssd', should_set_attribute=False)
    def has_ssd(self):
        """Return true if Storage has any drive as SSD"""
        self._has_ssd = False
        for member in self.get_members():
            if member.has_ssd:
                self._has_ssd = True
                break

    @property
    @utils.lazy_load_and_cache('_has_rotational', should_set_attribute=False)
    def has_rotational(self):
        """Return true if Storage has any drive as HDD"""
        self._has_rotational = False
        for member in self.get_members():
            if member.has_rotational:
                self._has_rotational = True
                break

    @property
    @utils.lazy_load_and_cache('_has_nvme_ssd', should_set_attribute=False)
    def has_nvme_ssd(self):
        """Return True if Storage has SSD drive and protocol is NVMe"""
        self._has_nvme_ssd = False
        for member in self.get_members():
            if member.has_nvme_ssd:
                self._has_nvme_ssd = True
                break

    @property
    @utils.lazy_load_and_cache(
        '_drive_rotational_speed_rpm', should_set_attribute=False)
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""
        self._drive_rotational_speed_rpm = set()
        for member in self.get_members():
            self._drive_rotational_speed_rpm.update(
                member.drive_rotational_speed_rpm)

    def refresh(self):
        super(StorageCollection, self).refresh()
        self._volumes_maximum_size_bytes = None
        self._drives_maximum_size_bytes = None
        self._has_ssd = None
        self._has_rotational = None
        self._has_nvme_ssd = None
        self._drive_rotational_speed_rpm = None
