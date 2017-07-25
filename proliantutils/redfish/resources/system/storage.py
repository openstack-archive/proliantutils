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

from proliantutils.redfish.resources.system import drives as sys_drives
from proliantutils.redfish.resources.system import volumes as sys_volumes
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

    _volume = None
    _drive = None

    @property
    def volume(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        if self._volume is None:
            self._volume = sys_volumes.VolumesCollection(
                self._conn, utils.get_subresource_path_by(self, 'Volumes'),
                redfish_version=self.redfish_version)
        return self._volume

    @property
    def drive(self):
        """This property prepares the list of drives

        :return a list of drives.
        """
        if self._drive is None:
            self._drive = []
            for member in self.drives:
                self._drive.append(sys_drives.Drives(
                    self._conn, member.get('@odata.id'),
                    self.redfish_version))
        return self._drive


class StorageCollection(base.ResourceCollectionBase):

    _maximum_volume_size = None
    _maximum_drive_size = None

    @property
    def _resource_type(self):
        return Storage

    @property
    def maximum_volume_size(self):
        """Gets the biggest volume

        :returns: size in bytes.
        """
        if self._maximum_volume_size is None:
            self._maximum_volume_size = 0
            size = []
            for member in self.get_members():
                size.append(member.volume.maximum_size)
            self._maximum_volume_size = max(size)
        return self._maximum_volume_size

    @property
    def maximum_drive_size(self):
        """Gets the biggest disk

        :returns the size in bytes.
        """
        if self._maximum_drive_size is None:
            self._maximum_drive_size = 0
            size = []
            for member in self.get_members():
                size.append(max(member.drive.capacity_bytes))
            self._maximum_drive_size = max(size)
        return self._maximum_drive_size

    def refresh(self):
        super(StorageCollection, self).refresh()
        self._maximum_drive_size = None
        self._maximum_volume_size = None
