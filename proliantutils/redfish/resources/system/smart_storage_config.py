# Copyright 2018 Hewlett Packard Enterprise Development LP
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

from proliantutils import log
from sushy.resources import base


LOG = log.get_logger(__name__)


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    controller_id = base.Field("Id")

    physical_drives = base.Field("PhysicalDrives", adapter=list)

    settings_uri = base.Field(["@Redfish.Settings",
                               "SettingsObject", "@odata.id"])

    def delete_raid(self):
        """Clears the RAID configuration from the system."""
        if self.physical_drives is None:
            msg = ('Delete raid was not attempted for controller: '
                   '%(controller)s as no physical drive found.'
                   % {'controller': self.controller_id})
            LOG.debug(msg)
            return

        data = {
            "LogicalDrives": [],
            "DataGuard": "Disabled",
            "PhysicalDrives": self.physical_drives,
            "Actions": [{"Action": "FactoryReset"}]
        }
        self._conn.put(self.settings_uri, data=data)
