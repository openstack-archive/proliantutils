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

from proliantutils.redfish.resources.system import logical_drives
from proliantutils.redfish.resources.system import physical_drives
from proliantutils.redfish.resources.system import unconfigured_drives
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class ArrayController(base.ResourceBase):

    identity = base.Field('Id')
    """The identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    _logical_drive = None
    _physical_drive = None
    _unconfigured_drive = None

    @property
    def logical_drive(self):
        if self._logical_drive is None:
            self._logical_drive = (
                logical_drives.LogicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'LogicalDrives']),
                    redfish_version=self.redfish_version))
        return self._logical_drive

    @property
    def physical_drive(self):
        if self._physical_drive is None:
            self._physical_drive = (
                physical_drives.PhysicalDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'PhysicalDrives']),
                    redfish_version=self.redfish_version))
        return self._physical_drive

    @property
    def unconfigured_drive(self):
        if self._unconfigured_drive is None:
            self._unconfigured_drive = (
                unconfigured_drives.UnconfiguredDriveCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'UnconfiguredDrives']),
                    redfish_version=self.redfish_version))
        return self._unconfigured_drive

    def refresh(self):
        super(ArrayController, self).refresh()
        self._physical_drive = None
        self._logical_drive = None
        self._unconfigured_drive = None


class ArrayControllerCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return ArrayController
