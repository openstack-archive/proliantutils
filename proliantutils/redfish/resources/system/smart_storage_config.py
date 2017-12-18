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

from proliantutils.hpssa import constants
from proliantutils.hpssa import manager


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    physical_drives = base.Field("PhysicalDrives", adapter=list)

    settings_uri = base.Field(["@Redfish.Settings",
                               "SettingsObject", "@odata.id"])

    def delete_raid(self):
        """Clears the RAID configuration from the system."""
        if self.physical_drives is None:
            return

        data = {
            "LogicalDrives": [],
            "DataGuard": "Disabled",
            "PhysicalDrives": self.physical_drives,
            "Actions": [{"Action": "FactoryReset"}]
        }
        self._conn.put(self.settings_uri, data=data)

    def create_raid(self, raid_config):
        """Create the RAID configuration from the system.

        :param raid_config: The dictionary containing the requested RAID
                            configuration. This data structure should be
        as follows: raid_config = {'raid_level': 1, 'size_gb': 100}
        """
        manager.validate(raid_config)
        ld = raid_config['logical_disks'][0]
        redfish_logical_disk = []
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
        self._conn.put(self.settings_uri, data=data)
