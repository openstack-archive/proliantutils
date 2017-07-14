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
from proliantutils.redfish.resources.system import secure_boot
from proliantutils.redfish.resources.system import system
from sushy.resources.system import system as sushy_system


class HPESystemTestCase(testtools.TestCase):

    def setUp(self):
        super(HPESystemTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = system_json['default']

        self.sys_inst = system.HPESystem(
            self.conn, '/redfish/v1/Systems/1',
            redfish_version='1.0.2')

    def test_attributes(self):
        self.assertEqual('bios and uefi',
                         self.sys_inst.supported_boot_mode)

    def test__get_hpe_push_power_button_action_element(self):
        value = self.sys_inst._get_hpe_push_power_button_action_element()
        self.assertEqual("/redfish/v1/Systems/1/Actions/Oem/Hpe/"
                         "HpeComputerSystemExt.PowerButton/",
                         value.target_uri)
        self.assertEqual(["Press", "PressAndHold"], value.allowed_values)

    def test__get_hpe_push_power_button_action_element_missing_action(self):
        self.sys_inst._hpe_actions.computer_system_ext_powerbutton = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'Oem/Hpe/Actions/#HpeComputerSystemExt.PowerButton is missing',
            self.sys_inst._get_hpe_push_power_button_action_element)

    def test_push_power_button(self):
        self.sys_inst.push_power_button(
            sys_cons.PUSH_POWER_BUTTON_PRESS)
        self.sys_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Systems/1/Actions/Oem/Hpe/'
            'HpeComputerSystemExt.PowerButton/',
            data={'PushType': 'Press'})

    def test_push_power_button_invalid_value(self):
        self.assertRaises(exception.InvalidInputError,
                          self.sys_inst.push_power_button, 'invalid-value')

    def test_bios_settings(self):
        self.assertIsNone(self.sys_inst._bios_settings)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_bios = self.sys_inst.bios_settings
        self.assertIsInstance(actual_bios,
                              bios.BIOSSettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_bios,
                      self.sys_inst.bios_settings)
        self.conn.get.return_value.json.assert_not_called()

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_persistent(self,
                                               set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['CDROM'], persistent=True)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_CD,
            enabled=sushy.BOOT_SOURCE_ENABLED_CONTINUOUS)

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_device_unknown_persistent(
            self, set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['unknown'], persistent=True)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_NONE,
            enabled=sushy.BOOT_SOURCE_ENABLED_CONTINUOUS)

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_not_persistent(
            self, set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['CDROM'], persistent=False)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_CD,
            enabled=sushy.BOOT_SOURCE_ENABLED_ONCE)

    def test_bios_settings_on_refresh(self):
        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/bios.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.bios_settings,
                              bios.BIOSSettings)

        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        self.sys_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.sys_inst._bios_settings)

        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/bios.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.bios_settings,
                              bios.BIOSSettings)

    def test_update_persistent_boot_uefi_target(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            bios_boot_mock = json.loads(f.read())
        self.conn.get.return_value.json.reset()
        self.conn.get.return_value.json.side_effect = (
            [bios_mock['Default'], bios_boot_mock['Default']])
        self.sys_inst.update_persistent_boot(['ISCSI'], persistent=True,
                                             mac='C4346BB7EF30')
        uefi_boot_settings = {
            'Boot': {'UefiTargetBootSourceOverride': 'NIC.LOM.1.1.iSCSI'}
        }

        calls = [mock.call('/redfish/v1/Systems/1', data=uefi_boot_settings),
                 mock.call('/redfish/v1/Systems/1',
                           data={'Boot':
                                 {'BootSourceOverrideTarget': 'UefiTarget',
                                  'BootSourceOverrideEnabled': 'Continuous'}})]
        self.sys_inst._conn.patch.assert_has_calls(calls)

    def test_update_persistent_boot_uefi_target_without_mac(self):
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            'Mac is needed for uefi iscsi boot',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True, None)

    def test_update_persistent_boot_uefi_target_fail(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = (
            [bios_mock['Default'], sushy.exceptions.SushyError])
        self.assertRaisesRegex(
            exception.IloError,
            'The BIOS Boot Settings was not found.',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True, '12345678')

    def test_pci_devices(self):
        pci_dev_return_value = None
        pci_dev1_return_value = None
        pci_coll_return_value = None
        self.assertIsNone(self.sys_inst._pci_devices)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device_collection.json') as f:
            pci_coll_return_value = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device.json') as f:
            pci_dev_return_value = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device1.json') as f:
            pci_dev1_return_value = json.loads(f.read())
            self.conn.get.return_value.json.side_effect = (
                [pci_coll_return_value, pci_dev_return_value,
                 pci_dev1_return_value])
        actual_pci = self.sys_inst.pci_devices
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_pci,
                      self.sys_inst.pci_devices)
        self.conn.get.return_value.json.assert_not_called()

    def test_secure_boot_with_missing_path_attr(self):
        def _get_secure_boot():
            return self.sys_inst.secure_boot

        self.sys_inst._json.pop('SecureBoot')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'attribute SecureBoot is missing',
            _get_secure_boot)

    def test_secure_boot(self):
        # check for the underneath variable value
        self.assertIsNone(self.sys_inst._secure_boot)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN |
        actual_secure_boot = self.sys_inst.secure_boot
        # | THEN |
        self.assertIsInstance(actual_secure_boot,
                              secure_boot.SecureBoot)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_secure_boot,
                      self.sys_inst.secure_boot)
        self.conn.get.return_value.json.assert_not_called()

    def test_secure_boot_on_refresh(self):
        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.secure_boot,
                              secure_boot.SecureBoot)

        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        self.sys_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.sys_inst._secure_boot)

        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.secure_boot,
                              secure_boot.SecureBoot)
