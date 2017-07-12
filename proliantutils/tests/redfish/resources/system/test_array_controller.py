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

from proliantutils.redfish.resources.system import array_controller


class ArrayControllerTestCase(testtools.TestCase):

    def setUp(self):
        super(ArrayControllerTestCase, self).setUp()
        self.conn = mock.Mock()
        array_controller_file = ('proliantutils/tests/redfish/json_samples/'
                                 'array_controller.json')

        with open(array_controller_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        path = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers")
        self.sys_stor = array_controller.ArrayController(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)


class ArrayControllerCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(ArrayControllerCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'array_controller_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_stor_col = array_controller.ArrayControllerCollection(
            self.conn, '/redfish/v1/Systems/1/SmartStorage/ArrayControllers',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor_col.redfish_version)
        self.assertEqual('HpeSmartStorageArrayControllers',
                         self.sys_stor_col.name)
        path = ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0',)
        self.assertEqual(path, self.sys_stor_col.members_identities)

    @mock.patch.object(array_controller, 'ArrayController', autospec=True)
    def test_get_member(self, mock_eth):
        self.sys_stor_col.get_member(
            '/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0')
        mock_eth.assert_called_once_with(
            self.sys_stor_col._conn,
            '/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0',
            redfish_version=self.sys_stor_col.redfish_version)

    @mock.patch.object(array_controller, 'ArrayController', autospec=True)
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

    def test_logical_drive_paths(self):
        self.assertIsNone(self.sys_stor_col._logical_drive_paths)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
                    "/LogicalDrives/"]
        actual = self.sys_stor_col.logical_drive_paths
        self.assertEqual(expected, actual)

    def test_logical_drive(self):
        log_coll = None
        log_dr = None
        self.sys_stor_col._logical_drive_paths = (
            ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
             "/LogicalDrives/"])
        self.assertIsNone(self.sys_stor_col._logical_drive)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_drive_collection.json') as f:
            log_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_drive.json') as f:
            log_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [log_coll, log_dr]
        actual_log_dr = self.sys_stor_col.logical_drive
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor_col.logical_drive)
        self.conn.get.return_value.json.assert_not_called()

    def test_smart_disk_drive_paths(self):
        self.assertIsNone(self.sys_stor_col._smart_disk_drive_paths)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
                    "/DiskDrives/"]
        actual = self.sys_stor_col.smart_disk_drive_paths
        self.assertEqual(expected, actual)

    def test_smart_disk_drive(self):
        disk_coll = None
        disk_dr = None
        self.sys_stor_col._smart_disk_drive_paths = (
            ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
             "/DiskDrives/"])
        self.assertIsNone(self.sys_stor_col._smart_disk_drive)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/disk_drive_collection.json') as f:
            disk_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/disk_drive.json') as f:
            disk_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [disk_coll, disk_dr]
        actual_log_dr = self.sys_stor_col.smart_disk_drive
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor_col.smart_disk_drive)
        self.conn.get.return_value.json.assert_not_called()

    def test_unconfigured_disk_drive_paths(self):
        self.assertIsNone(self.sys_stor_col._unconfigured_disk_drive_paths)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
                    "/UnconfiguredDrives/"]
        actual = self.sys_stor_col.unconfigured_disk_drive_paths
        self.assertEqual(expected, actual)

    def test_unconfigured_disk_drive(self):
        disk_coll = None
        disk_dr = None
        self.sys_stor_col._unconfigured_disk_drive_paths = (
            ["/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0"
             "/UnconfiguredDrives/"])
        self.assertIsNone(self.sys_stor_col._unconfigured_disk_drive)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/unconfigured_drive_collection.json') as f:
            disk_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/unconfigured_drive.json') as f:
            disk_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [disk_coll, disk_dr]
        actual_log_dr = self.sys_stor_col.unconfigured_disk_drive
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor_col.unconfigured_disk_drive)
        self.conn.get.return_value.json.assert_not_called()
