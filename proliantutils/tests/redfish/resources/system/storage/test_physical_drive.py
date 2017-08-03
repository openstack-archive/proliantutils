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

from proliantutils.redfish.resources.system.storage import physical_drive


class HPEPhysicalDriveTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEPhysicalDriveTestCase, self).setUp()
        self.conn = mock.Mock()
        logical_file = ('proliantutils/tests/redfish/json_samples/'
                        'disk_drive.json')
        with open(logical_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        path = ("/redfish/v1/Systems/1/SmartStorage/"
                "ArrayControllers/0/DiskDrives")
        self.sys_stor = physical_drive.HPEPhysicalDrive(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)


class HPEPhysicalDriveCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEPhysicalDriveCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'disk_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_stor_col = physical_drive.HPEPhysicalDriveCollection(
            self.conn, ('/redfish/v1/Systems/1/SmartStorage/'
                        'ArrayControllers/0/DiskDrives'),
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor_col.redfish_version)
        self.assertEqual('HpeSmartStorageDiskDrives',
                         self.sys_stor_col.name)
        path = ('/redfish/v1/Systems/1/SmartStorage/'
                'ArrayControllers/0/DiskDrives/3',)
        self.assertEqual(path, self.sys_stor_col.members_identities)

    @mock.patch.object(physical_drive, 'HPEPhysicalDrive', autospec=True)
    def test_get_member(self, mock_eth):
        self.sys_stor_col.get_member(
            ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0/'
             'DiskDrives/3'))
        mock_eth.assert_called_once_with(
            self.sys_stor_col._conn,
            ('/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0/'
             'DiskDrives/3'),
            redfish_version=self.sys_stor_col.redfish_version)

    @mock.patch.object(physical_drive, 'HPEPhysicalDrive', autospec=True)
    def test_get_members(self, mock_eth):
        members = self.sys_stor_col.get_members()
        path = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers/"
                "0/DiskDrives/3")
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
                'disk_drive.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = 572325
        actual = self.sys_stor_col.maximum_size_mib
        self.assertEqual(expected, actual)

    def test_has_ssd(self):
        self.assertIsNone(self.sys_stor_col._has_ssd)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual = self.sys_stor_col.has_ssd
        self.assertFalse(actual)
