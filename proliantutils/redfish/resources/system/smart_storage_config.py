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

import json

from sushy.resources import base

from proliantutils.hpssa import manager
from proliantutils.hpssa import constants
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
        raid_data = self._conn.get(self._get_smart_storage_config_url())
        current_config = raid_data.json()
        physical_drives = json.dumps(current_config['PhysicalDrives'])
        data = {
            "LogicalDrives": [],
            "DataGuard": "Disabled",
            "PhysicalDrives": json.loads(physical_drives),
            "Actions": [{"Action": "FactoryReset"}]
        }
        settings_uri = self._get_smart_storage_config_url()
        self._conn.put(settings_uri, data=data)

    def create_raid(self, raid_config):
        """Create the RAID configuration from the system.

        :param raid_config: The dictionary containing the requested
        RAID configuration. This data structure should be as follows:
        raid_config = {'logical_disks': [{'raid_level': 1, 'size_gb': 100},
                                         <info-for-logical-disk-2>
                                        ]}

        ---------Minimal redfish data required---------
        {
            "DataGuard": "Disabled",
            "LogicalDrives": [
               {
                  "CapacityGiB": xxx,
                  "Raid": "xxxxx",
                  "PhysicalDrives": [],
                  "DataDrives": {
                     "DataDriveCount": x
                  }
               }
            ]
        }
        """
        manager.validate(raid_config)
        logical_drives = raid_config['logical_disks']
        redfish_logical_disk = []
        for ld in logical_drives:
            ld_attr = {}
            if ld["size_gb"] == "MAX":
                ld_attr["CapacityGiB"] = -1
            else:
                ld_attr["CapacityGiB"] = int(ld["size_gb"])
            ld_attr["Raid"] = "Raid" + ld["raid_level"]
            if 'physical_disks' in ld:
                ld_attr["DataDrives"] = ld["physical_disks"]
            else:
                datadrives = {}
                if 'number_of_physical_disks' in ld:
                    datadrives["DataDriveCount"] = (
                        ld["number_of_physical_disks"])
                else:
                    datadrives["DataDriveCount"] = (constants.
                                                    RAID_LEVEL_MIN_DISKS
                                                    [ld["raid_level"]])
                if 'disk_type' in ld:
                    datadrives["DataDriveMediaType"] = ld["disk_type"]
                if 'interface_type' in ld:
                    datadrives["DataDriveInterfaceType"] = ld["interface_type"]
                ld_attr["DataDrives"] = datadrives
            if 'volume_name' in ld:
                ld_attr["LogicalDriveName"] = ld["volume_name"]

            redfish_logical_disk.append(ld_attr)
        data = {
            "DataGuard": "Disabled",
            "PhysicalDrives": [],
            "LogicalDrives": redfish_logical_disk
        }
        settings_uri = self._get_smart_storage_config_url()
        self._conn.put(settings_uri, data=data)
