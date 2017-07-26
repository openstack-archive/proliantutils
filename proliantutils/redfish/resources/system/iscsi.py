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


class ISCSISettings(base.ResourceBase):
    """Class that represents the iSCSI settings resource.

    This class extends the functionality of base resource class
    from sushy.
    """

    def is_iscsi_boot_supported(self):
        """Checks whether iscsi boot is supported or not.

        To find the iscsi boot support, check whether the PATCH
        operation is allowed on the iscsi 'settings' uri.
        :returns: True if it is supported else False
        """
        return 'PATCH' in utils.get_allowed_operations(
            self, ['@Redfish.Settings', 'SettingsObject'])
