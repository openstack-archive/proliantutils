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

    def test_base_configs(self):
        self.assertIsNone(self.bios_inst._base_configs)
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        default_settings = self.bios_inst.base_configs
        self.assertIsInstance(default_settings, bios.BIOSBaseConfigs)

    def test_pending_settings_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['BIOS_pending_settings_default'])
        actual_settings = self.bios_inst.pending_settings
        self.assertIsInstance(actual_settings,
                              bios.BIOSPendingSettings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_inst.refresh()
        self.assertIsNone(self.bios_inst._pending_settings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['BIOS_pending_settings_default'])

        self.assertIsInstance(actual_settings,
                              bios.BIOSPendingSettings)

    def test_boot_settings_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])
        actual_settings = self.bios_inst.boot_settings
        self.assertIsInstance(actual_settings,
                              bios.BIOSBootSettings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_inst.refresh()
        self.assertIsNone(self.bios_inst._boot_settings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.assertIsInstance(actual_settings,
                              bios.BIOSBootSettings)

    def test_base_configs_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        default_settings = self.bios_inst.base_configs
        self.assertIsInstance(default_settings, bios.BIOSBaseConfigs)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.bios_inst.refresh()
        self.assertIsNone(self.bios_inst._base_configs)

        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.assertIsInstance(default_settings, bios.BIOSBaseConfigs)


class BIOSBaseConfigsTestCase(testtools.TestCase):

    def setUp(self):
        super(BIOSBaseConfigsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.bios_base_inst = bios.BIOSBaseConfigs(
            self.conn, '/redfish/v1/Systems/1/bios/baseconfigs',
            redfish_version='1.0.2')

    def test_attributes(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            bios_default = json.loads(f.read())['BaseConfigs'][0]['default']

        self.assertEqual(bios_default, self.bios_base_inst.default_config)


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
        data['BootMode'] = 'Uefi'
        self.bios_settings_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Systems/1/bios/settings', data)

    def test_update_bios_data(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            bios_settings = json.loads(f.read())['BaseConfigs'][0]['default']
        target_uri = '/redfish/v1/systems/1/bios/settings'
        self.bios_settings_inst.update_bios_data(bios_settings)
        self.bios_settings_inst._conn.post(target_uri,
                                           data={'Attributes': bios_settings})


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

    def test_get_persistent_boot_device_boot_sources_is_none(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_json = (
                json.loads(f.read())['BIOS_boot_without_boot_sources'])
        self.bios_boot_inst.boot_sources = boot_json['BootSources']
        self.bios_boot_inst.persistent_boot_config_order = (
            boot_json['PersistentBootConfigOrder'])
        self.assertRaisesRegex(
            exception.IloError,
            'Boot sources or persistent boot config order not found',
            self.bios_boot_inst.get_persistent_boot_device)
