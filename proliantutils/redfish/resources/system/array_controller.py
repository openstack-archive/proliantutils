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

from proliantutils.redfish.resources.system import disk_drives
from proliantutils.redfish.resources.system import logical_drives
from proliantutils.redfish.resources.system import unconfigured_drives
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')


class LinkField(base.CompositeField):
    logical_drives = base.Field(['LogicalDrives', '@odata.id'])
    disk_drives = base.Field(['PhysicalDrives', '@odata.id'])
    storage_enclosure = base.Field(['StorageEnclosure', '@odata.id'])
    unconfigured_drives = base.Field(['UnconfiguredDrives', '@odata.id'])


class ArrayController(base.ResourceBase):

    identity = base.Field('Id')
    """The identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    links = LinkField('Links')

    status = HealthStatusField('Status')


class ArrayControllerCollection(base.ResourceCollectionBase):

    _logical_drive_paths = None
    _logical_drive = None
    _smart_disk_drive_paths = None
    _smart_disk_drive = None
    _unconfigured_disk_drive_paths = None
    _unconfigured_disk_drive = None

    @property
    def _resource_type(self):
        return ArrayController

    @property
    def logical_drive_paths(self):
        """Prepares list of logical drive paths

        Prepares list of logical drive paths from all members
        of array controllers.
        :returns a list of logical drive paths
        """
        if self._logical_drive_paths is None:
            self._logical_drive_paths = []
            for member in self.get_members():
                self._logical_drive_paths.append(member.links.logical_drives)
        return self._logical_drive_paths

    @property
    def logical_drive(self):
        """Prepares list of logical drives

        Prepares list of logical drives from all members
        of array controllers.
        :returns a list of logical drives
        """
        if self._logical_drive is None:
            self._logical_drive = []
            paths = self.logical_drive_paths
            for path in paths:
                self._logical_drive.append(
                    logical_drives.LogicalDriveCollection(
                        self._conn, path,
                        redfish_version=self.redfish_version))
        return self._logical_drive

    @property
    def smart_disk_drive_paths(self):
        """Prepares list of disk drive paths

        Prepares list of disk drive paths from all members
        of array controllers.
        :returns a list of disk drive paths
        """
        if self._smart_disk_drive_paths is None:
            self._smart_disk_drive_paths = []
            for member in self.get_members():
                self._smart_disk_drive_paths.append(member.links.disk_drives)
        return self._smart_disk_drive_paths

    @property
    def smart_disk_drive(self):
        """Prepares list of disk drives

        Prepares list of disk drives from all members
        of array controllers.
        :returns a list of disk drives
        """
        if self._smart_disk_drive is None:
            self._smart_disk_drive = []
            paths = self.smart_disk_drive_paths
            for path in paths:
                self._smart_disk_drive.append(
                    disk_drives.DiskDriveCollection(
                        self._conn, path,
                        redfish_version=self.redfish_version))
        return self._smart_disk_drive

    @property
    def unconfigured_disk_drive_paths(self):
        """Prepares list of unconfigured disk drive paths

        Prepares list of unconfigured disk drive paths from all members
        of array controllers.
        :returns a list of unconfigured disk drive paths
        """
        if self._unconfigured_disk_drive_paths is None:
            self._unconfigured_disk_drive_paths = []
            for member in self.get_members():
                self._unconfigured_disk_drive_paths.append(
                    member.links.unconfigured_drives)
        return self._unconfigured_disk_drive_paths

    @property
    def unconfigured_disk_drive(self):
        """Prepares list of unconfigured disk drives

        Prepares list of unconfigured disk drives from all members
        of array controllers.
        :returns a list of unconfigured disk drives
        """
        if self._unconfigured_disk_drive is None:
            self._unconfigured_disk_drive = []
            paths = self.unconfigured_disk_drive_paths
            for path in paths:
                self._unconfigured_disk_drive.append(
                    unconfigured_drives.UnconfiguredDriveCollection(
                        self._conn, path,
                        redfish_version=self.redfish_version))
        return self._unconfigured_disk_drive

    def refresh(self):
        super(ArrayControllerCollection, self).refresh()
        self._logical_drive_paths = None
        self._logical_drive = None
        self._smart_disk_drive_paths = None
        self._smart_disk_drive = None
        self._unconfigured_disk_drive_paths = None
        self._unconfigured_disk_drive = None
