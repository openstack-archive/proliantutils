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

from proliantutils.redfish.resources.system.storage import storage


class StorageTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageTestCase, self).setUp()
        self.conn = mock.Mock()
        storage_file = 'proliantutils/tests/redfish/json_samples/storage.json'
        with open(storage_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.stor_json = self.conn.get.return_value.json.return_value

        path = ("/redfish/v1/Systems/437XR1138R2/Storage/1")
        self.sys_stor = storage.Storage(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)
        self.assertEqual('1', self.sys_stor.identity)
        self.assertEqual('Local Storage Controller', self.sys_stor.name)
        self.assertEqual('Integrated RAID Controller',
                         self.sys_stor.description)
        self.assertEqual(self.stor_json.get('Drives'),
                         self.sys_stor.drives)

    def test_volumes(self):
        log_coll = None
        log_dr = None
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/volume_collection.json') as f:
            log_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/volume.json') as f:
            log_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [log_coll, log_dr]
        actual_volumes = self.sys_stor.volumes
        self.assertIs(actual_volumes,
                      self.sys_stor.volumes)
        self.sys_stor.invalidate()
        self.sys_stor.refresh(force=False)
        self.assertTrue(actual_volumes._is_stale)

    def test__drives_list(self):
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/drive.json') as f:
            dr_json = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [dr_json['drive1'],
                                                       dr_json['drive2'],
                                                       dr_json['drive3']]
        actual_dr = self.sys_stor._drives_list()
        self.assertIsInstance(actual_dr, list)

    def test_drives_maximum_size_bytes(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor.drives_maximum_size_bytes
        self.assertEqual(expected, actual)

    def test_has_ssd_true(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor.has_ssd)

    def test_has_rotational(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor.has_rotational)

    def test_has_nvme_ssd(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor.has_nvme_ssd)

    def test_drive_rotational_speed_rpm(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        expected = set([15000, 10000])
        self.assertEqual(expected,
                         self.sys_stor.drive_rotational_speed_rpm)


class StorageCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'storage_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_stor_col = storage.StorageCollection(
            self.conn, '/redfish/v1/Systems/437XR1138R2/Storage',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor_col.redfish_version)
        self.assertEqual('Storage Collection',
                         self.sys_stor_col.name)
        path = ('/redfish/v1/Systems/437XR1138R2/Storage/1',)
        self.assertEqual(path, self.sys_stor_col.members_identities)

    @mock.patch.object(storage, 'Storage', autospec=True)
    def test_get_member(self, mock_eth):
        self.sys_stor_col.get_member(
            '/redfish/v1/Systems/437XR1138R2/Storage/1')
        mock_eth.assert_called_once_with(
            self.sys_stor_col._conn,
            ('/redfish/v1/Systems/437XR1138R2/Storage/1'),
            redfish_version=self.sys_stor_col.redfish_version)

    @mock.patch.object(storage, 'Storage', autospec=True)
    def test_get_members(self, mock_eth):
        members = self.sys_stor_col.get_members()
        path = ("/redfish/v1/Systems/437XR1138R2/Storage/1")
        calls = [
            mock.call(self.sys_stor_col._conn, path,
                      redfish_version=self.sys_stor_col.redfish_version),
        ]
        mock_eth.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test_volumes_maximum_size_bytes(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'volume_collection.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'volume.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor_col.volumes_maximum_size_bytes
        self.assertEqual(expected, actual)

    def test_drives_maximum_size_bytes(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor_col.drives_maximum_size_bytes
        self.assertEqual(expected, actual)

    def test_has_ssd_true(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor_col.has_ssd)

    def test_has_rotational(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor_col.has_rotational)

    def test_has_nvme_ssd(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        self.assertTrue(self.sys_stor_col.has_nvme_ssd)

    def test_drive_rotational_speed_rpm(self):
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive.json')
        with open(path, 'r') as f:
            dr_json = json.loads(f.read())
            val.append(dr_json['drive1'])
            val.append(dr_json['drive2'])
            val.append(dr_json['drive3'])
            self.conn.get.return_value.json.side_effect = val
        expected = set([15000, 10000])
        self.assertEqual(expected,
                         self.sys_stor_col.drive_rotational_speed_rpm)
