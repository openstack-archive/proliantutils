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

from proliantutils.redfish.resources.system import pci_device


class PCIDeviceTestCase(testtools.TestCase):

    def setUp(self):
        super(PCIDeviceTestCase, self).setUp()
        self.conn = mock.Mock()
        pci_file = 'proliantutils/tests/redfish/json_samples/pci_device.json'
        with open(pci_file, 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        pci_path = "/redfish/v1/Systems/1/PCIDevices/1"
        self.sys_pci = pci_device.PCIDevice(
            self.conn, pci_path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_pci._parse_attributes()
        self.assertEqual('1.0.2', self.sys_pci.redfish_version)
        self.assertEqual('1', self.sys_pci.identity)


class PCIDeviceCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(PCIDeviceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'pci_device_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_pci_col = pci_device.PCIDeviceCollection(
            self.conn, '/redfish/v1/Systems/1/PCIDevices',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_pci_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_pci_col.redfish_version)
        self.assertEqual('PciDevices', self.sys_pci_col.name)
        pci_path = ('/redfish/v1/Systems/1/PCIDevices/1',
                    '/redfish/v1/Systems/1/PCIDevices/6')
        self.assertEqual(pci_path, self.sys_pci_col.members_identities)

    @mock.patch.object(pci_device, 'PCIDevice', autospec=True)
    def test_get_member(self, mock_pci):
        self.sys_pci_col.get_member(
            '/redfish/v1/Systems/1/PCIDevices/1')
        mock_pci.assert_called_once_with(
            self.sys_pci_col._conn,
            ('/redfish/v1/Systems/1/PCIDevices/1'),
            redfish_version=self.sys_pci_col.redfish_version)

    @mock.patch.object(pci_device, 'PCIDevice', autospec=True)
    def test_get_members(self, mock_pci):
        members = self.sys_pci_col.get_members()
        path_list = ["/redfish/v1/Systems/1/PCIDevices/1",
                     "/redfish/v1/Systems/1/PCIDevices/6"]
        calls = [
            mock.call(self.sys_pci_col._conn, path_list[0],
                      redfish_version=self.sys_pci_col.redfish_version),
            mock.call(self.sys_pci_col._conn, path_list[1],
                      redfish_version=self.sys_pci_col.redfish_version)
        ]
        mock_pci.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))

    def test_gpu_devices(self):
        self.assertIsNone(self.sys_pci_col._gpu_devices)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'pci_device.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'pci_device1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = val
        actual = self.sys_pci_col.gpu_devices
        self.assertEqual(1, len(self.sys_pci_col._gpu_devices))

    def test_gpu_devices_count(self):
        self.assertIsNone(self.sys_pci_col._gpu_devices_count)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'pci_device.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'pci_device1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))    
        self.conn.get.return_value.json.side_effect = val
        actual_count = self.sys_pci_col.gpu_devices_count
        expected_count = 1
        self.assertEqual(expected_count, actual_count) 
