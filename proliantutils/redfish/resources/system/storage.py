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

from proliantutils.redfish.resources.system import drives
from proliantutils.redfish.resources.system import volumes as sys_volumes
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')


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

    volumes = base.Field('Volumes')
    """The set of volumes produced by the storage controllers."""

    status = HealthStatusField('Status')


class StorageCollection(base.ResourceCollectionBase):

    _volume_paths = None
    _volume = None
    _disk_drive_paths = None
    _disk_drive = None

    @property
    def _resource_type(self):
        return Storage

    @property
    def volume_paths(self):
        """This property prepares the list of volume collection paths

        Prepares the list of volume collection paths from all members
        of Storage.
        :return a list of volume paths.
        """
        if self._volume_paths is None:
            self._volume_paths = []
            for mem in self.get_members():
                if mem.volumes is not None:
                    path = mem.volumes.get('@odata.id')
                    if path is not None:
                        self._volume_paths.append(path)
        return self._volume_paths

    @property
    def volume(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        if self._volume is None:
            self._volume = []
            volume_paths = self.volume_paths
            for path in volume_paths:
                self._volume.append(sys_volumes.VolumesCollection(
                    self._conn, path, redfish_version=self.redfish_version))
        return self._volume

    @property
    def disk_drive_paths(self):
        """This property prepares the list of drives paths

        :return a list of drives paths.
        """
        if self._disk_drive_paths is None:
            self._disk_drive_paths = []
            for member in self.get_members():
                path_list = member.drives
                for mem in path_list:
                    path = mem.get('@odata.id')
                    self._disk_drive_paths.append(path)
        return self._disk_drive_paths

    @property
    def disk_drive(self):
        """This property prepares the list of drives

        :return a list of drives.
        """
        if self._disk_drive is None:
            self._disk_drive = []
            drive_paths = self.disk_drive_paths
            for path in drive_paths:
                self._disk_drive.append(drives.Drives(self._conn,
                                                      path,
                                                      self.redfish_version))
        return self._disk_drive

    @property
    def maximum_volume_size(self):
        """Gets the biggest volume

        :returns the size in bytes.
        """
        if self._maximum_volume_size is None:
            self._maximum_volume_size = 0
            volume_members = self.volume
            if len(volume_members) > 0:
                for mem in volume_members:
                    size = mem.maximum_size
                    if self._maximum_volume_size < size:
                        self._maximum_volume_size = size
        return self._maximum_volume_size

    @property
    def maximum_disk_size(self):
        """Gets the biggest disk

        :returns the size in bytes.
        """
        if self._maximum_disk_size is None:
            self._maximum_disk_size = 0
            disk_members = self.disk_drive
            if len(disk_members) > 0:
                for mem in disk_members:
                    disk_size = mem.capacity_bytes
                    if self._maximum_disk_size < disk_size:
                        self._maximum_disk_size = disk_size
        return self._maximum_disk_size

    def refresh(self):
        super(StorageCollection, self).refresh()
        self._volume_paths = None
        self._volume = None
        self._disk_drive_paths = None
        self._disk_drive = None
        self._maximum_volume_size = None
        self._maximum_disk_size = None
