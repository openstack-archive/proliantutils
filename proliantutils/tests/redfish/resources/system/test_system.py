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
from proliantutils.redfish.resources.system import ethernet_interface
from proliantutils.redfish.resources.system import system
from proliantutils.redfish import utils


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

    def test_update_persistent_boot_persistent(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as g:
            boot_mock = json.loads(g.read())
        self.conn.get.return_value.json.side_effect = [bios_mock['Default'],
                                                       boot_mock['Default']]
        self.sys_inst.update_persistent_boot(['CDROM'], True)
        data = {}
        data['Boot'] = {'BootSourceOverrideEnabled': 'Continuous',
                        'BootSourceOverrideTarget': 'Cd'}
        self.sys_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Systems/1', data)

    def test_update_persistent_boot_not_persistent(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [bios_mock['Default'],
                                                       boot_mock['Default']]
        self.sys_inst.update_persistent_boot(['CDROM'], False)
        data = {}
        data['Boot'] = {'BootSourceOverrideEnabled': 'Once',
                        'BootSourceOverrideTarget': 'Cd'}
        self.sys_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Systems/1', data)

    def test_update_persistent_boot_uefi_target(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [bios_mock['Default'],
                                                       boot_mock['Default']]
        self.sys_inst.update_persistent_boot(['ISCSI'], persistent=True,
                                             mac='C4346BB7EF30')
        data = {}
        data['Boot'] = {'UefiTargetBootSourceOverride': 'NIC.LOM.1.1.iSCSI'}
        new_data = {}
        new_data['Boot'] = {'BootSourceOverrideEnabled': 'Continuous',
                            'BootSourceOverrideTarget': 'UefiTarget'}
        calls = [mock.call('/redfish/v1/Systems/1', data),
                 mock.call('/redfish/v1/Systems/1', new_data)]
        self.sys_inst._conn.patch.assert_has_calls(calls)

    def test_update_persistent_boot_uefi_target_without_mac(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [bios_mock['Default'],
                                                       boot_mock['Default']]
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            'Mac is needed for iscsi uefi boot',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True, None)

    def test_update_persistent_boot_uefi_target_invalid_mac(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_boot.json', 'r') as f:
            boot_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [bios_mock['Default'],
                                                       boot_mock['Default']]
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            'MAC provided "12345678" is Invalid',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True, '12345678')

    def test_update_persistent_boot_fail(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_mock = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = (
            [bios_mock['Default'], sushy.exceptions.SushyError])
        self.assertRaisesRegex(
            exception.IloError,
            'The BIOS Boot Settings was not found.',
            self.sys_inst.update_persistent_boot, ['CDROM'], True, None)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path(self, res_mock):
        res = 'EthernetInterfaces'
        res_mock.return_value = '/redfish/v1/Systems/1/EthernetInterfaces'
        path = self.sys_inst._get_hpe_sub_resource_collection_path(res)
        self.assertTrue(res_mock.called)
        self.assertEqual(path, res_mock.return_value)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path_oem_path(self, res_mock):
        res = 'EthernetInterfaces'
        error_val = exception.MissingAttributeError
        oem_path = '/redfish/v1/Systems/1/EthernetInterfaces'
        res_mock.side_effect = [error_val, oem_path]
        path = self.sys_inst._get_hpe_sub_resource_collection_path(res)
        self.assertTrue(res_mock.called)
        self.assertEqual(path, oem_path)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path_fail(self, res_mock):
        error_val = exception.MissingAttributeError
        res_mock.side_effect = [error_val, error_val]
        self.assertRaises(
            exception.MissingAttributeError,
            self.sys_inst._get_hpe_sub_resource_collection_path,
            'EthernetInterfaces')
        self.assertTrue(res_mock.called)

    @mock.patch.object(system.HPESystem,
                       '_get_hpe_sub_resource_collection_path')
    def test_ethernet_interfaces(self, path_mock):
        self.conn.get.return_value.json.reset_mock()
        eth_coll = None
        eth_value = None
        path_mock.return_value = '/redfish/v1/Systems/1/EthernetInterfaces'
        path = ('proliantutils/tests/redfish/json_samples/'
                'ethernet_interfaces_collection.json')
        with open(path, 'r') as f:
            eth_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'ethernet_interfaces.json', 'r') as f:
            eth_value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [eth_coll,
                                                       eth_value]
        self.assertIsNone(self.sys_inst._connected_mac_addresses)
        actual_macs = self.sys_inst.ethernet_interfaces.summary
        self.assertEqual({'12:44:6A:3B:04:11': sys_cons.HEALTH_STATE_ENABLED},
                         actual_macs)
        self.assertIsInstance(self.sys_inst._connected_mac_addresses,
                              ethernet_interface.EthernetInterfaceCollection)
