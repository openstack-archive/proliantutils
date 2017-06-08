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

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import mappings

LOG = log.get_logger(__name__)


class ResetKeysActionField(base.CompositeField):
    allowed_values = base.Field('ResetKeysType@Redfish.AllowableValues',
                                adapter=list)

    target_uri = base.Field('target', required=True)


class ActionsField(base.CompositeField):
    reset_keys = ResetKeysActionField('#SecureBoot.ResetKeys')


class SecureBoot(base.ResourceBase):

    name = base.Field('Name')
    """secure boot resource name"""

    current_boot = base.MappedField(
        'SecureBootCurrentBoot', mappings.SECUREBOOT_CURRENT_BOOT_MAP)
    """current secure boot"""

    enable = base.Field('SecureBootEnable', required=True)
    """secure boot enable"""

    # Note(deray): May need mapping if this gets used.
    mode = base.Field('SecureBootMode')
    """secure boot mode"""

    _actions = ActionsField('Actions', required=True)

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

    def _get_reset_keys_action_element(self):
        reset_keys_action = self._actions.reset_keys
        if not reset_keys_action:
            raise exception.MissingAttributeError(
                attribute='Actions/#SecureBoot.ResetKeys',
                resource=self.path)
        return reset_keys_action

    def get_allowed_reset_keys_values(self):
        """Get the allowed values for resetting the system.

        :returns: A set with the allowed values.
        """
        reset_keys_action = self._get_reset_keys_action_element()

        if not reset_keys_action.allowed_values:
            LOG.warning('Could not figure out the allowed values for the '
                        'reset keys in secure boot %s', self.path)
            return set(mappings.SECUREBOOT_RESET_KEYS_MAP_REV)

        return set([mappings.SECUREBOOT_RESET_KEYS_MAP[v] for v in
                    set(mappings.SECUREBOOT_RESET_KEYS_MAP).
                    intersection(reset_keys_action.allowed_values)])

    def reset_keys(self, target_value):
        """Resets the secure boot keys.

        :param target_value: The target value to be set.
        :raises: InvalidInputError, if the target value is not
            allowed.
        :raises: SushyError, on an error from iLO.
        """
        valid_keys_resets = self.get_allowed_reset_keys_values()
        if target_value not in valid_keys_resets:
            msg = ('The parameter "%(parameter)s" value "%(target_value)s" is '
                   'invalid. Valid values are: %(valid_keys_reset_values)s' %
                   {'parameter': 'target_value', 'target_value': target_value,
                    'valid_keys_reset_values': valid_keys_resets})
            raise exception.InvalidInputError(msg)

        value = mappings.SECUREBOOT_RESET_KEYS_MAP_REV[target_value]
        target_uri = (
            self._get_reset_keys_action_element().target_uri)

        self._conn.post(target_uri, data={'ResetKeysType': value})
