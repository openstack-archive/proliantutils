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

from proliantutils.redfish import utils
from sushy.resources import base


class BIOS(base.ResourceBase):

    boot_mode = base.Field(["Attributes", "BootMode"])

    _settings = None

    @property
    def settings(self):
        """Property to provide reference to bios settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._settings is None:
            self._settings = BIOSSettings(
                self._conn, utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]),
                redfish_version=self.redfish_version)

        return self._settings


class BIOSSettings(base.ResourceBase):

    boot_mode = base.Field(["Attributes", "BootMode"])
