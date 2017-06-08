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

__author__ = 'HPE'

from sushy.resources import base

from proliantutils.redfish.resources.system import mappings


class SecureBoot(base.ResourceBase):

    current_boot = base.MappedField(
        'SecureBootCurrentBoot', mappings.SECUREBOOT_CURRENT_BOOT_MAP)
    """current secure boot"""

    enable = base.Field('SecureBootEnable', required=True)
    """secure boot enable"""

    # Note(deray): May need mapping if this gets used.
    mode = base.Field('SecureBootMode')
    """secure boot mode"""

    _actions_reset_keys_target_uri = base.Field(
        ['Actions', '#SecureBoot.ResetKeys', 'target'], required=True)
    """secure boot reset keys target path"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing SecureBoot

        :param connector: A Connector instance
        :param identity: The canonical path identity of SecureBoot
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(SecureBoot, self).__init__(connector, identity,
                                         redfish_version=redfish_version)

    def change_settings(self, target_data):
        """Change secure boot settings on the server.

        :param data: The data to be set.
        :raises: InvalidParameterValueError, if the target value is not
            allowed.
        """
        # TODO(deray): Need to test. No way to test it now.
        # Probably the caller should reset the server after issuing
        # this command.
        self._conn.post(self.path, data=target_data)
