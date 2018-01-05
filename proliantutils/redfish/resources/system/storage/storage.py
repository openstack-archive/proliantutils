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

from proliantutils.redfish.resources.system.storage import constants
from proliantutils.redfish.resources.system.storage import drive as sys_drives
from proliantutils.redfish.resources.system.storage \
    import volume as sys_volumes
from proliantutils.redfish import utils
from sushy.resources import base

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

    _volumes = None
    _drives_maximum_size_bytes = None
    _has_ssd = None
    _has_rotational = None
    _has_nvme_ssd = None
    _drive_rotational_speed_rpm = None

    @property
    def volumes(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        if self._volumes is None:
            self._volumes = sys_volumes.VolumeCollection(
                self._conn, utils.get_subresource_path_by(self, 'Volumes'),
                redfish_version=self.redfish_version)

        self._volumes.refresh(force=False)
        return self._volumes

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
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._drives_maximum_size_bytes is None:
            self._drives_maximum_size_bytes = (
                utils.max_safe([member.capacity_bytes
                               for member in self._drives_list()]))
        return self._drives_maximum_size_bytes

    @property
    def has_ssd(self):
        """Return true if any of the drive is ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self._drives_list():
                if member.media_type == constants.MEDIA_TYPE_SSD:
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if any of the drive is HDD"""

        if self._has_rotational is None:
            self._has_rotational = False
            for member in self._drives_list():
                if member.media_type == constants.MEDIA_TYPE_HDD:
                    self._has_rotational = True
                    break
        return self._has_rotational

    @property
    def has_nvme_ssd(self):
        """Return True if the drive is SSD and protocol is NVMe"""

        if self._has_nvme_ssd is None:
            self._has_nvme_ssd = False
            for member in self._drives_list():
                if (member.media_type == constants.MEDIA_TYPE_SSD and
                        member.protocol == constants.PROTOCOL_NVMe):
                    self._has_nvme_ssd = True
        return self._has_nvme_ssd

    @property
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = set()
            for member in self._drives_list():
                if member.rotation_speed_rpm is not None:
                    self._drive_rotational_speed_rpm.add(
                        member.rotation_speed_rpm)
        return self._drive_rotational_speed_rpm

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        if self._volumes is not None:
            self._volumes.invalidate(force)

        self._drives_maximum_size_bytes = None
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
    def volumes_maximum_size_bytes(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        if self._volumes_maximum_size_bytes is None:
            self._volumes_maximum_size_bytes = (
                utils.max_safe([member.volumes.maximum_size_bytes
                               for member in self.get_members()]))
        return self._volumes_maximum_size_bytes

    @property
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._drives_maximum_size_bytes is None:
            self._drives_maximum_size_bytes = (
                utils.max_safe([member.drives_maximum_size_bytes
                               for member in self.get_members()]))
        return self._drives_maximum_size_bytes

    @property
    def has_ssd(self):
        """Return true if Storage has any drive as ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self.get_members():
                if member.has_ssd:
                    self._has_ssd = True
                    break
        return self._has_ssd

    @property
    def has_rotational(self):
        """Return true if Storage has any drive as HDD"""

        if self._has_rotational is None:
            self._has_rotational = False
            for member in self.get_members():
                if member.has_rotational:
                    self._has_rotational = True
                    break
        return self._has_rotational

    @property
    def has_nvme_ssd(self):
        """Return True if Storage has SSD drive and protocol is NVMe"""

        if self._has_nvme_ssd is None:
            self._has_nvme_ssd = False
            for member in self.get_members():
                if member.has_nvme_ssd:
                    self._has_nvme_ssd = True
                    break
        return self._has_nvme_ssd

    @property
    def drive_rotational_speed_rpm(self):
        """Gets set of rotational speed of the disks"""

        if self._drive_rotational_speed_rpm is None:
            self._drive_rotational_speed_rpm = set()
            for member in self.get_members():
                self._drive_rotational_speed_rpm.update(
                    member.drive_rotational_speed_rpm)
        return self._drive_rotational_speed_rpm

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        self._volumes_maximum_size_bytes = None
        self._drives_maximum_size_bytes = None
        self._has_ssd = None
        self._has_rotational = None
        self._has_nvme_ssd = None
        self._drive_rotational_speed_rpm = None
