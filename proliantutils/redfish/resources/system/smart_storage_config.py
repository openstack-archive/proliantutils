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
from proliantutils.redfish.resources.system.storage import constants as storage_constants
from proliantutils.redfish.resources.system.storage import mappings as storage_mappings


LOG = log.get_logger(__name__)


class LogicalDriveListField(base.ListField):
    volume_unique_identifier = base.Field('VolumeUniqueIdentifier',
                                          required=True)


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    controller_id = base.Field("Id")

    smart_storage_config_message = base.Field(['@Redfish.Settings',
                                               'Messages'])

    logical_drives = LogicalDriveListField("LogicalDrives", default=[])

    location = base.Field("Location")

    physical_drives = base.Field("PhysicalDrives", adapter=list, default=None)

    settings_uri = base.Field(["@Redfish.Settings",
                               "SettingsObject", "@odata.id"])

    def _generic_format(self, raid_config, controller=None):
        """Convert redfish data of current raid config to generic format.

        :param raid_config: Raid configuration dictionary
        :param controller: Array controller model in post_create read else
                           None
        :returns: current raid config.
        """
        logical_drives = raid_config["LogicalDrives"]
        logical_disks = []
        controller = controller
        for ld in logical_drives:
            prop = {'size_gb': ld['CapacityGiB'],
                    'raid_level': ld['Raid'].strip('Raid'),
                    'root_device_hint': {
                        'wwn': '0x' + ld['VolumeUniqueIdentifier']},
                    'controller': controller,
                    'physical_disks': ld['DataDrives'],
                    'volume_name': ld['LogicalDriveName']}
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

    def read_raid(self, controller=None):
        """Get the current RAID configuration from the system.

        :param controller: If controller model its post-create read else
                           post-delete
        :returns: current raid config.
        """
        if controller:
            if not self.logical_drives:
                msg = ('No logical drives found on the controller')
                LOG.debug(msg)
                raise exception.IloLogicalDriveNotFoundError(msg)
            raid_op = 'create_raid'
        else:
            raid_op = 'delete_raid'

        result, raid_message = self._check_smart_storage_message()

        if result:
            configured_raid_settings = self._conn.get(self.settings_uri)
            raid_data = {
                'logical_disks': self._generic_format(
                    configured_raid_settings.json(), controller=controller)}
            return raid_data
        else:
            if self.physical_drives is None or not raid_message:
                # This controller is not configured or controller
                # not used in raid operation
                return
            else:
                msg = ('Failed to perform the %(opr)s operation '
                       'successfully. Error - %(error)s'
                       % {'opr': raid_op, 'error': str(raid_message)})
                raise exception.IloError(msg)

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

    def disk_erase(self, disks, disk_type):
        """Perform the out of band sanitize disk erase on the hardware.

        :param disks: List of id of disk drives
        :param disk_type: Media type of disk drives
        """
        if disk_type == storage_mappings.MEDIA_TYPE_MAP_REV[storage_constant.MEDIA_TYPE_HDD]:
            data = {
                "Actions": [
                    {
                        "Action": "PhysicalDriveErase",
                        "ErasePattern": "SanitizeUnrestrictedOverwrite",
                        "PhysicalDriveList": disks
                    }
                ],
                "DataGuard": "Disabled"
            }
        else:
            data = {
                "Actions": [
                    {
                        "Action": "PhysicalDriveErase",
                        "ErasePattern": "SanitizeRestrictedBlockErase",
                        "PhysicalDriveList": disks
                    }
                ],
                "DataGuard": "Disabled"
            }
        self._conn.patch(self.settings_uri, data=data)