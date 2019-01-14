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
from sushy import utils as sushy_utils

from proliantutils.redfish import utils


class ISCSIResource(base.ResourceBase):
    """Class that represents the iSCSI resource.

    This class extends the functionality of base resource class
    from sushy.
    """
    iscsi_initiator = base.Field("iSCSIInitiatorName")

    def is_iscsi_boot_supported(self):
        """Checks whether iscsi boot is supported or not.

        To find the iscsi boot support, check whether the PATCH
        operation is allowed on the iscsi 'settings' uri.
        :returns: True if it is supported else False
        """
        return utils.is_operation_allowed(
            'PATCH', self,
            ['@Redfish.Settings', 'SettingsObject'])

    @property
    @sushy_utils.cache_it
    def iscsi_settings(self):
        """Property to provide reference to iSCSI settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        return ISCSISettings(
            self._conn, utils.get_subresource_path_by(
                self, ["@Redfish.Settings", "SettingsObject"]),
            redfish_version=self.redfish_version)


class ISCSISettings(base.ResourceBase):
    """Class that represents the iSCSI settings.

    This class extends the functionality of base resource class
    from sushy.
    """

    def update_iscsi_settings(self, iscsi_data):
        """Update iscsi data

        :param data: default iscsi config data
        """
        self._conn.patch(self.path, data=iscsi_data)
