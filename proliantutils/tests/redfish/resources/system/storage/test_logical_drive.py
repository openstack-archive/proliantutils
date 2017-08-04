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

from proliantutils.redfish.resources.system.storage import logical_drive


class HPELogicalDriveTestCase(testtools.TestCase):

    def setUp(self):
        super(HPELogicalDriveTestCase, self).setUp()
        self.conn = mock.Mock()
        logical_file = ('proliantutils/tests/redfish/json_samples/'
                        'logical_drive.json')
        with open(logical_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        path = ("/redfish/v1/Systems/1/SmartStorage/"
                "ArrayControllers/0/LogicalDrives")
        self.sys_stor = logical_drive.HPELogicalDrive(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)


class HPELogicalDriveCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(HPELogicalDriveCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'logical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_stor_col = logical_drive.HPELogicalDriveCollection(
            self.conn, ('/redfish/v1/Systems/1/SmartStorage/'
                        'ArrayControllers/0/LogicalDrives'),
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor_col.redfish_version)
        self.assertEqual('HpeSmartStorageLogicalDrives',
                         self.sys_stor_col.name)
        path = ('/redfish/v1/Systems/1/SmartStorage/'
                'ArrayControllers/0/LogicalDrives/1',)
        self.assertEqual(path, self.sys_stor_col.members_identities)

    @mock.patch.object(logical_drive, 'HPELogicalDrive', autospec=True)
    def test_get_member(self, mock_eth):
        self.sys_stor_col.get_member(
            ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0/'
             'LogicalDrives/1'))
        mock_eth.assert_called_once_with(
            self.sys_stor_col._conn,
            ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0/'
             'LogicalDrives/1'),
            redfish_version=self.sys_stor_col.redfish_version)

    @mock.patch.object(logical_drive, 'HPELogicalDrive', autospec=True)
    def test_get_members(self, mock_eth):
        members = self.sys_stor_col.get_members()
        path = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers/"
                "0/LogicalDrives/1")
        calls = [
            mock.call(self.sys_stor_col._conn, path,
                      redfish_version=self.sys_stor_col.redfish_version),
        ]
        mock_eth.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test_maximum_size_mib(self):
        self.assertIsNone(self.sys_stor_col._maximum_size_mib)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'logical_drive.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = 953837
        actual = self.sys_stor_col.maximum_size_mib
        self.assertEqual(expected, actual)

    def test_logical_raid_levels(self):
        self.assertIsNone(self.sys_stor_col._logical_raid_levels)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'logical_drive.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = ['0']
        actual = self.sys_stor_col.logical_raid_levels
        self.assertEqual(expected, actual)
