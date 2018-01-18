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

from proliantutils import exception
from proliantutils.redfish import utils


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    smart_storage_config_message = base.Field(['@Redfish.Settings',
                                               'Messages'])

    def _get_smart_storage_config_url(self):
        """Get the smart storage config settings url.

        :returns: smart storage config settings url
        """
        return utils.get_subresource_path_by(self, ["@Redfish.Settings",
                                                    "SettingsObject"])

    def _generic_format(self, raid_config):
        """Convert redfish data of current raid config to generic format.

        :returns: current raid config.
        """
        logical_drives = raid_config["LogicalDrives"]
        logical_disks = []
        for ld in logical_drives:
            prop = {}
            prop['size_gb'] = ld['CapacityGiB']
            prop['raid_level'] = ld['Raid'].strip('Raid')
            prop['root_device_hint'] = {'wwn': '0x' +
                                        ld['VolumeUniqueIdentifier']}
            prop['controller'] = ("Smart Storage Controller in " +
                                  raid_config["Location"])
            prop['physical_disks'] = ld['DataDrives']
            prop['volume_name'] = ld['LogicalDriveName']
            logical_disks.append(prop)
        return logical_disks

    def _check_smart_storage_message(self):
        """Check for smart storage message.

        :returns: result, raid_message
        """
        ssc_mesg = self.smart_storage_config_message
        result = True
        raid_message = ""
        for element in ssc_mesg:
            if "Success" not in element['MessageId']:
                result = False
                raid_message = element['MessageId']
        return result, raid_message

    def read_raid(self):
        """Get the current RAID configuration from the system.

        :returns: current raid config.
        """
        result, raid_message = self._check_smart_storage_message()
        if result:
            raid_data = {}
            raid_config = self._conn.get(self._get_smart_storage_config_url())
            raid_data['logical_disks'] = (self.
                                          _generic_format(raid_config.json()))
            return raid_data
        else:
            msg = ('Failed to perform the raid operation successfully.'
                   'Response from controller Error - %(error)s'
                   % {'error': str(raid_message)})
            raise exception.IloError(msg)

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
