# Copyright 2017 Hewlett Packard Enterprise Development LP
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

from proliantutils.redfish.resources.system.storage import array_controller


class HPEArrayControllerTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEArrayControllerTestCase, self).setUp()
        self.conn = mock.Mock()
        array_controller_file = ('proliantutils/tests/redfish/json_samples/'
                                 'array_controller.json')

        with open(array_controller_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        path = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers")
        self.sys_stor = array_controller.HPEArrayController(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)

    def test_logical_drives(self):
        log_coll = None
        log_dr = None
        self.assertIsNone(self.sys_stor._logical_drives)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_drive_collection.json') as f:
            log_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_drive.json') as f:
            log_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [log_coll, log_dr]
        actual_log_dr = self.sys_stor.logical_drives
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor.logical_drives)
        self.conn.get.return_value.json.assert_not_called()

    def test_physical_drives(self):
        disk_coll = None
        disk_dr = None
        self.assertIsNone(self.sys_stor._physical_drives)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/disk_drive_collection.json') as f:
            disk_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/disk_drive.json') as f:
            disk_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [disk_coll, disk_dr]
        actual_log_dr = self.sys_stor.physical_drives
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor.physical_drives)
        self.conn.get.return_value.json.assert_not_called()


class HPEArrayControllerCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEArrayControllerCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'array_controller_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_stor_col = array_controller.HPEArrayControllerCollection(
            self.conn, '/redfish/v1/Systems/1/SmartStorage/ArrayControllers',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor_col.redfish_version)
        self.assertEqual('HpeSmartStorageArrayControllers',
                         self.sys_stor_col.name)
        path = ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0',)
        self.assertEqual(path, self.sys_stor_col.members_identities)

    @mock.patch.object(array_controller, 'HPEArrayController', autospec=True)
    def test_get_member(self, mock_eth):
        self.sys_stor_col.get_member(
            '/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0')
        mock_eth.assert_called_once_with(
            self.sys_stor_col._conn,
            '/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0',
            redfish_version=self.sys_stor_col.redfish_version)

    @mock.patch.object(array_controller, 'HPEArrayController', autospec=True)
    def test_get_members(self, mock_eth):
        members = self.sys_stor_col.get_members()
        path = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0")
        calls = [
            mock.call(self.sys_stor_col._conn, path,
                      redfish_version=self.sys_stor_col.redfish_version),
        ]
        mock_eth.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test_logical_drives_maximum_size_mib(self):
        self.assertIsNone(self.sys_stor_col._logical_drives_maximum_size_mib)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'logical_drive_collection.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'logical_drive.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 953837
        actual = self.sys_stor_col.logical_drives_maximum_size_mib
        self.assertEqual(expected, actual)

    def test_physical_drives_maximum_size_mib(self):
        self.assertIsNone(self.sys_stor_col._physical_drives_maximum_size_mib)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive_collection.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 572325
        actual = self.sys_stor_col.physical_drives_maximum_size_mib
        self.assertEqual(expected, actual)

    def test_has_ssd(self):
        self.assertIsNone(self.sys_stor_col._has_ssd)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive_collection.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        self.assertFalse(self.sys_stor_col.has_ssd)
