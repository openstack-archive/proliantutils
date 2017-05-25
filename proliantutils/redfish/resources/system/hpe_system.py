# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from proliantutils.redfish.resources.system.bios import BiosResource
from proliantutils.redfish.resources.system.bios import BiosSettings
from proliantutils.redfish.resources.system.secure_boot import SecureBootResource
from sushy import exceptions
from sushy.resources.system.system import System


class HPESystem(System):

    def _get_resource_path(self, resource_name):
        """Helper function to find the resource path"""
        resource_path = self.json.get(resource_name)
        if not resource_path:
            raise exceptions.MissingAttributeError(attribute=resource_name,
                                                   resource=self._path)
        return resource_path.get('@odata.id')

    @property
    def secure_boot_resource(self):
        secure_boot_resource = SecureBootResource(
            self._conn, self._get_resource_path('SecureBoot'),
            redfish_version=self.redfish_version)
        return secure_boot_resource

    def secure_boot_config(self, data):
        if data is not None:
            target_uri = self._get_resource_path('SecureBoot')
            self._conn.post(target_uri, data=data)

    @property
    def bios_resource(self):
        bios_resource = BiosResource(
            self._conn, self._get_resource_path('Bios'),
            redfish_version=self.redfish_version)
        return bios_resource

    @property
    def bios_settings(self):
        bios_resource = BiosResource(
            self._conn, self._get_resource_path('Bios'),
            redfish_version=self.redfish_version)
        bios_settings_uri = bios_resource.BiosSettingsURI
        bios_settings = BiosSettings(self._conn, bios_settings_uri,
                                     redfish_version=self.redfish_version)
        return bios_settings
