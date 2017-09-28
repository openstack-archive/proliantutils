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


LOG = log.get_logger(__name__)


class LogicalDriveListField(base.ListField):
    volume_unique_identifier = base.Field('VolumeUniqueIdentifier',
                                          required=True)


class HPESmartStorageConfig(base.ResourceBase):
    """Class that defines the functionality for SmartSorageConfig Resources."""

    controller_id = base.Field("Id")

    logical_drives = LogicalDriveListField("LogicalDrives", default=[])

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
