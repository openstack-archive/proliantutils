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
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import ethernetinterface
from proliantutils.redfish.resources.system import system


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

    def test_ethernet_interfaces(self):
        self.conn.get.return_value.json.reset_mock()
        eth_coll_return_value = None
        eth_return_value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'ethernetinterfaces_collection.json')
        with open(path, 'r') as f:
            eth_coll_return_value = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'ethernetinterfaces.json', 'r') as f:
            eth_return_value = (json.loads(f.read()))

        self.conn.get.return_value.json.side_effect = [eth_coll_return_value,
                                                       eth_return_value]

        self.assertIsNone(self.sys_inst._connected_mac_addresses)
        actual_macs = self.sys_inst.ethernet_interfaces.eth_summary
        self.assertEqual({'12:44:6A:3B:04:11': 'Enabled'},
                         actual_macs)
        self.assertIsInstance(self.sys_inst._connected_mac_addresses,
                              ethernetinterface.EthernetInterfaceCollection)
