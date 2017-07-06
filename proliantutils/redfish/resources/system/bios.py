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

from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish import utils
from sushy.resources import base


class BIOSSettings(base.ResourceBase):

    _pending_settings = None

    @property
    def pending_settings(self):
        """Property to provide reference to bios settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._pending_settings is None:
            self._pending_settings = BIOSPendingSettings(
                self._conn, utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]),
                redfish_version=self.redfish_version)

        return self._pending_settings


class BIOSPendingSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)
