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
            dr_json = json.loads(f.read())
            self.conn.get.return_value.json.return_value = dr_json['drive1']

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
                'ArrayControllers/0/DiskDrives/3',
                '/redfish/v1/Systems/1/SmartStorage/'
                'ArrayControllers/0/DiskDrives/4',)
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
        path2 = ("/redfish/v1/Systems/1/SmartStorage/ArrayControllers/"
                 "0/DiskDrives/4")
        calls = [
            mock.call(self.sys_stor_col._conn, path,
                      redfish_version=self.sys_stor_col.redfish_version),
            mock.call(self.sys_stor_col._conn, path2,
                      redfish_version=self.sys_stor_col.redfish_version),
        ]
        mock_eth.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))

    def test_maximum_size_mib(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        expected = 572325
        actual = self.sys_stor_col.maximum_size_mib
        self.assertEqual(expected, actual)

    def test_has_ssd(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        actual = self.sys_stor_col.has_ssd
        self.assertTrue(actual)

    def test_has_hdd(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor_col.has_hdd)

    def test_get_all_hdd_drives(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        self.assertEqual(self.sys_stor_col.get_all_hdd_drives, ['1I:0:1'])

    def test_get_all_ssd_drives(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        self.assertEqual(self.sys_stor_col.get_all_ssd_drives, ['1I:0:1'])

    def test_has_disk_erase_completed_true(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            self.conn.get.return_value.json.side_effect = dr_json['disk-erase-completed']
        self.assertTrue(self.sys_stor_col.has_disk_erase_completed)

    def test_has_disk_erase_completed_false(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            self.conn.get.return_value.json.return_value = dr_json['disk-erase-progress']
        self.assertFalse(self.sys_stor_col.has_disk_erase_completed)

    def test_has_rotational(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor_col.has_rotational)

    def test_drive_rotational_speed_rpm(self):
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'disk_drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val = [dr_json['drive1'], dr_json['drive2']]
            self.conn.get.return_value.json.side_effect = val
        expected = set([10000])
        self.assertEqual(expected,
                         self.sys_stor_col.drive_rotational_speed_rpm)
