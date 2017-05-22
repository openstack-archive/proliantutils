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

from proliantutils.redfish.resources.system import bios


class BIOSTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_inst = bios.BIOS(
            self.conn, '/redfish/v1/Systems/1/bios',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.bios_inst._parse_attributes()
        self.assertEqual('/redfish/v1/systems/1/bios/settings/',
                         self.bios_inst._settings_object_path)
        self.assertEqual('Uefi', self.bios_inst.boot_mode)

    def test_settings(self):
        self.assertIsNone(self.bios_inst._settings)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_settings = self.bios_inst.settings
        self.assertIsInstance(actual_settings,
                              bios.BIOSSettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_settings,
                      self.bios_inst.settings)
        self.conn.get.return_value.json.assert_not_called()


class BIOSSettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSSettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Bios_settings_default'])

        self.bios_settings_inst = bios.BIOSSettings(
            self.conn, '/redfish/v1/Systems/1/bios/settings',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.bios_settings_inst._parse_attributes()
        self.assertEqual('Uefi', self.bios_settings_inst.boot_mode)
