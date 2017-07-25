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

    _volume = None
    _drive = None
    _drives_maximum_size_bytes = None

    @property
    def volume(self):
        """This property prepares the list of volumes

        :return a list of volumes.
        """
        if self._volume is None:
            self._volume = sys_volumes.VolumeCollection(
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
                self._drive.append(sys_drives.Drive(
                    self._conn, member.get('@odata.id'),
                    self.redfish_version))
        return self._drive

    @property
    def drives_maximum_size_bytes(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._drives_maximum_size_bytes is None:
            self._drives_maximum_size_bytes = (
                max([member.capacity_bytes
                    for member in self.drive]))
        return self._drives_maximum_size_bytes


class StorageCollection(base.ResourceCollectionBase):

    _volumes_maximum_size_bytes = None
    _drives_maximum_size_bytes = None

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
                max([member.volume.maximum_size_bytes
                    for member in self.get_members()]))
        return self._volumes_maximum_size_bytes

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

    def refresh(self):
        super(StorageCollection, self).refresh()
        self._volumes_maximum_size_bytes = None
        self._drives_maximum_size_bytes = None
