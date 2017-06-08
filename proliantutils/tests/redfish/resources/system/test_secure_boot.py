# Copyright 2017 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import mock
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import secure_boot


class SecureBootTestCase(testtools.TestCase):

    def setUp(self):
        super(SecureBootTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/secure_boot.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.secure_boot_inst = secure_boot.SecureBoot(
            self.conn, '/redfish/v1/Systems/1/SecureBoot',
            redfish_version='1.0.2')

    def test_field_attributes(self):
        self.assertEqual('UEFI Secure Boot', self.secure_boot_inst.name)
        self.assertEqual(sys_cons.SECUREBOOT_CURRENT_BOOT_DISABLED,
                         self.secure_boot_inst.current_boot)
        self.assertFalse(self.secure_boot_inst.enable)
        self.assertEqual('UserMode', self.secure_boot_inst.mode)

    def test__get_reset_keys_action_element(self):
        value = self.secure_boot_inst._get_reset_keys_action_element()
        self.assertEqual('/redfish/v1/Systems/1/SecureBoot/Actions/'
                         'SecureBoot.ResetKeys',
                         value.target_uri)
        self.assertEqual(['ResetAllKeysToDefault',
                          'DeleteAllKeys',
                          'DeletePK'], value.allowed_values)

    def test__get_reset_keys_action_element_missing_action(self):
        self.secure_boot_inst._actions.reset_keys = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'Actions/#SecureBoot.ResetKeys is missing',
            self.secure_boot_inst._get_reset_keys_action_element)

    def test_get_allowed_reset_keys_values(self):
        values = self.secure_boot_inst.get_allowed_reset_keys_values()
        expected = set([sys_cons.SECUREBOOT_RESET_KEYS_DEFAULT,
                        sys_cons.SECUREBOOT_RESET_KEYS_DELETE_ALL,
                        sys_cons.SECUREBOOT_RESET_KEYS_DELETE_PK])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)

    @mock.patch.object(secure_boot.LOG, 'warning', autospec=True)
    def test_get_allowed_reset_keys_values_no_values_specified(
            self, mock_log):
        self.secure_boot_inst._actions.reset_keys.allowed_values = None
        values = self.secure_boot_inst.get_allowed_reset_keys_values()
        # Assert it returns all values if it can't get the specific ones
        expected = set([sys_cons.SECUREBOOT_RESET_KEYS_DEFAULT,
                        sys_cons.SECUREBOOT_RESET_KEYS_DELETE_ALL,
                        sys_cons.SECUREBOOT_RESET_KEYS_DELETE_PK])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)
        self.assertEqual(1, mock_log.call_count)

    def test_reset_keys(self):
        self.secure_boot_inst.reset_keys(
            sys_cons.SECUREBOOT_RESET_KEYS_DEFAULT)
        self.secure_boot_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Systems/1/SecureBoot/Actions/SecureBoot.ResetKeys',
            data={'ResetKeysType': 'ResetAllKeysToDefault'})

    def test_reset_system_invalid_value(self):
        self.assertRaises(exception.InvalidInputError,
                          self.secure_boot_inst.reset_keys, 'invalid-value')
