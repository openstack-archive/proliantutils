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

from proliantutils.redfish.resources.system.storage import logical_drive
from proliantutils.redfish.resources.system.storage import physical_drive
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HPEArrayController(base.ResourceBase):
    """This class represents the ArrayControllers resource from SmartStorage"""

    identity = base.Field('Id')
    """The identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    _logical_drives = None
    _physical_drives = None

    @property
    def logical_drives(self):
        """Gets the resource LogicalDrives of the ArrayControllers"""

        if self._logical_drives is None:
            self._logical_drives = (
                logical_drive.HPELogicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'LogicalDrives']),
                    redfish_version=self.redfish_version))
        return self._logical_drives

    @property
    def physical_drives(self):
        """Gets the resource PhysicalDrives of the ArrayControllers"""

        if self._physical_drives is None:
            self._physical_drives = (
                physical_drive.HPEPhysicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'PhysicalDrives']),
                    redfish_version=self.redfish_version))
        return self._physical_drives

    def refresh(self):
        super(HPEArrayController, self).refresh()
        self._physical_drives = None
        self._logical_drives = None


class HPEArrayControllerCollection(base.ResourceCollectionBase):
    """This class represents the collection of ArrayControllers resource"""

    _logical_drives_maximum_size_mib = None
    _physical_drives_maximum_size_mib = None
    _has_ssd = None

    @property
    def _resource_type(self):
        return HPEArrayController

    @property
    def logical_drives_maximum_size_mib(self):
        """Gets the biggest logical drive

        :returns the size in MiB.
        """
        if self._logical_drives_maximum_size_mib is None:
            self._logical_drives_maximum_size_mib = (
                utils.max_safe([member.logical_drives.maximum_size_mib
                               for member in self.get_members()]))
        return self._logical_drives_maximum_size_mib

    @property
    def physical_drives_maximum_size_mib(self):
        """Gets the biggest disk

        :returns the size in MiB.
        """
        if self._physical_drives_maximum_size_mib is None:
            self._physical_drives_maximum_size_mib = (
                utils.max_safe([member.physical_drives.maximum_size_mib
                               for member in self.get_members()]))
        return self._physical_drives_maximum_size_mib

    @property
    def has_ssd(self):
        """Return true if any of the drive under ArrayControllers is ssd"""

        if self._has_ssd is None:
            self._has_ssd = False
            for member in self.get_members():
                if member.physical_drives.has_ssd:
                    self._has_ssd = True
                    break
        return self._has_ssd

    def refresh(self):
        super(HPEArrayControllerCollection, self).refresh()
        self._logical_drives_maximum_size_mib = None
        self._physical_drives_maximum_size_mib = None
        self._has_ssd = None
