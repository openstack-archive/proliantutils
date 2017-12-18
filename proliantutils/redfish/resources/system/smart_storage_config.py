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

from proliantutils import exception
from proliantutils import log
from sushy.resources import base

from proliantutils.hpssa import constants
from proliantutils.hpssa import manager


LOG = log.get_logger(__name__)


class LogicalDriveListField(base.ListField):
    volume_unique_identifier = base.Field('VolumeUniqueIdentifier',
                                          required=True)


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    controller_id = base.Field("Id")

    logical_drives = LogicalDriveListField("LogicalDrives", default=[])

    location = base.Field("Location")

    settings_uri = base.Field(["@Redfish.Settings",
                               "SettingsObject", "@odata.id"])

    def delete_raid(self):
        """Clears the RAID configuration from the system.

        """
        if not self.logical_drives:
            msg = ('No logical drives found on the controller '
                   '%(controller)s' % {'controller': str(self.controller_id)})
            LOG.debug(msg)
            raise exception.IloLogicalDriveNotFoundError(msg)

        lds = [{
               'Actions': [{"Action": "LogicalDriveDelete"}],
               'VolumeUniqueIdentifier':
               logical_drive.volume_unique_identifier}
               for logical_drive in self.logical_drives]

        data = {'LogicalDrives': lds, 'DataGuard': 'Permissive'}
        self._conn.put(self.settings_uri, data=data)

    def create_raid(self, raid_config):
        """Create the raid configuration on the hardware.

        :param raid_config: A dictionary containing target raid configuration
                            data. This data stucture should be as follows:
                            raid_config = {'logical_disks': [{'raid_level': 1,
                            'size_gb': 100, 'physical_disks': ['6I:1:5'],
                            'controller': 'HPE Smart Array P408i-a SR Gen10'},
                            <info-for-logical-disk-2>]}
        """
        manager.validate(raid_config)
        logical_drives = raid_config['logical_disks']
        redfish_logical_disk = []
        for ld in logical_drives:
            ld_attr = {"Raid": "Raid" + ld["raid_level"]}
            ld_attr[
                "CapacityGiB"] = -1 if ld[
                    "size_gb"] == "MAX" else int(ld["size_gb"])
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
            "LogicalDrives": redfish_logical_disk
        }
        self._conn.put(self.settings_uri, data=data)
