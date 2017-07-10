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
import sushy
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons


class BIOSSettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSSettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_inst = bios.BIOSSettings(
            self.conn, '/redfish/v1/Systems/1/bios',
            redfish_version='1.0.2')

    def test_attributes(self):
        self.assertEqual(sys_cons.BIOS_BOOT_MODE_UEFI,
                         self.bios_inst.boot_mode)

    def test_pending_settings(self):
        self.assertIsNone(self.bios_inst._pending_settings)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['BIOS_pending_settings_default'])
        actual_settings = self.bios_inst.pending_settings
        self.assertIsInstance(actual_settings,
                              bios.BIOSPendingSettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_settings,
                      self.bios_inst.pending_settings)
        self.conn.get.return_value.json.assert_not_called()

    def test_boot_settings(self):
        self.assertIsNone(self.bios_inst._boot_settings)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])
        actual_settings = self.bios_inst.boot_settings
        self.assertIsInstance(actual_settings,
                              bios.BIOSBootSettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_settings,
                      self.bios_inst.boot_settings)
        self.conn.get.return_value.json.assert_not_called()


class BIOSPendingSettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSPendingSettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['BIOS_pending_settings_default'])

        self.bios_settings_inst = bios.BIOSPendingSettings(
            self.conn, '/redfish/v1/Systems/1/bios/settings',
            redfish_version='1.0.2')

    def test_attributes(self):
        self.assertEqual(sys_cons.BIOS_BOOT_MODE_UEFI,
                         self.bios_settings_inst.boot_mode)

    def test_set_pending_boot_mode_bios(self):
        self.bios_settings_inst.set_pending_boot_mode(
            sys_cons.BIOS_BOOT_MODE_LEGACY_BIOS)
        data = {}
        data['BootMode'] = 'LegacyBios'
        self.bios_settings_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Systems/1/bios/settings', data)

    def test_set_pending_boot_mode_uefi(self):
        self.bios_settings_inst.set_pending_boot_mode(
            sys_cons.BIOS_BOOT_MODE_UEFI)
        data = {}
        data['UefiOptimizedBoot'] = 'Enabled'
        self.bios_settings_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Systems/1/bios/settings', data)


class BIOSBootSettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSBootSettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_boot_inst = bios.BIOSBootSettings(
            self.conn, '/redfish/v1/Systems/1/bios/boot',
            redfish_version='1.0.2')

    def test__attributes(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_json = (json.loads(f.read())['Default'])
        self.assertEqual(boot_json['BootSources'],
                         self.bios_boot_inst.boot_sources)
        self.assertEqual(boot_json['PersistentBootConfigOrder'],
                         self.bios_boot_inst.persistent_boot_config_order)

    def test_get_persistent_boot_device(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_json = (json.loads(f.read())['Default'])
        self.bios_boot_inst.persistent_boot_config_order = (
            boot_json['PersistentBootConfigOrder'])
        self.bios_boot_inst.boot_sources = boot_json['BootSources']
        result = self.bios_boot_inst.get_persistent_boot_device()
        self.assertEqual(result, sushy.BOOT_SOURCE_TARGET_HDD)

    def test_get_persistent_boot_device_without_boot(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_json = (json.loads(f.read())['BIOS_boot_without_boot'])
        self.bios_boot_inst.boot_sources = boot_json['BootSources']
        self.bios_boot_inst.persistent_boot_config_order = (
            boot_json['PersistentBootConfigOrder'])
        self.assertRaisesRegex(
            exception.IloError,
            'Persistent boot device failed, as no matched boot sources '
            'found for device:',
            self.bios_boot_inst.get_persistent_boot_device)

    def test_get_persistent_boot_device_none(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_json = (
                json.loads(f.read())['BIOS_persistent_boot_device_none'])
        self.bios_boot_inst.boot_sources = boot_json['BootSources']
        self.bios_boot_inst.persistent_boot_config_order = (
            boot_json['PersistentBootConfigOrder'])
        result = self.bios_boot_inst.get_persistent_boot_device()
        self.assertEqual(result, sushy.BOOT_SOURCE_TARGET_NONE)
