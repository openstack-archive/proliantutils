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

from sushy.resources import base

from proliantutils.redfish import utils


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    def _get_smart_storage_config_url(self):
        """Get the smart storage config settings url.

        :returns: smart storage config settings url
        """
        return utils.get_subresource_path_by(self, ["@Redfish.Settings",
                                                    "SettingsObject"])

    def delete_raid(self):
        """Clears the RAID configuration from the system."""

        settings_uri = self._get_smart_storage_config_url()
        raid_data = self._conn.get(settings_uri)
        current_config = raid_data.json()
        if 'PhysicalDrives' not in current_config:
            return

        data = {
            "LogicalDrives": [],
            "DataGuard": "Disabled",
            "PhysicalDrives": current_config['PhysicalDrives'],
            "Actions": [{"Action": "FactoryReset"}]
        }
        self._conn.put(settings_uri, data=data)
