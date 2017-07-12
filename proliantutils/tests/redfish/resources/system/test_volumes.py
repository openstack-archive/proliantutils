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

from proliantutils.redfish.resources.system import volumes


class VolumesTestCase(testtools.TestCase):

    def setUp(self):
        super(VolumesTestCase, self).setUp()
        self.conn = mock.Mock()
        vol_file = 'proliantutils/tests/redfish/json_samples/volume1.json'
        with open(vol_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        vol_path = ("/redfish/v1/Systems/437XR1138R2/Storage/1/Volumes/1")
        self.sys_vol = volumes.Volumes(
            self.conn, vol_path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_vol._parse_attributes()
        self.assertEqual('1.0.2', self.sys_vol.redfish_version)
        self.assertEqual('1', self.sys_vol.identity)
        self.assertEqual('Virtual Disk 1', self.sys_vol.name)
        self.assertEqual('Enabled', self.sys_vol.status.state)
        self.assertEqual('OK', self.sys_vol.status.health)
        self.assertEqual(False, self.sys_vol.encrypted)
        self.assertEqual('Mirrored', self.sys_vol.volume_type)
        self.assertEqual(899527000000, self.sys_vol.capacity_bytes)


class VolumesCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(VolumesCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'volume1_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_vol_col = volumes.VolumesCollection(
            self.conn, '/redfish/v1/Systems/437XR1138R2/Storage/1/Volumes',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_vol_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_vol_col.redfish_version)
        self.assertEqual('Storage Volume Collection',
                         self.sys_vol_col.name)
        vol_path = ('/redfish/v1/Systems/437XR1138R2/Storage/1/Volumes/1',)
        self.assertEqual(vol_path, self.sys_vol_col.members_identities)

    @mock.patch.object(volumes, 'Volumes', autospec=True)
    def test_get_member(self, mock_vol):
        self.sys_vol_col.get_member(
            '/redfish/v1/Systems/437XR1138R2/Volumes/1')
        mock_vol.assert_called_once_with(
            self.sys_vol_col._conn,
            ('/redfish/v1/Systems/437XR1138R2/Volumes/1'),
            redfish_version=self.sys_vol_col.redfish_version)

    @mock.patch.object(volumes, 'Volumes', autospec=True)
    def test_get_members(self, mock_vol):
        members = self.sys_vol_col.get_members()
        vol_path = ("/redfish/v1/Systems/437XR1138R2/Storage/1/Volumes/1")
        calls = [
            mock.call(self.sys_vol_col._conn, vol_path,
                      redfish_version=self.sys_vol_col.redfish_version),
        ]
        mock_vol.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test_maximum_size(self):
        self.assertIsNone(self.sys_vol_col._maximum_size)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'volume1.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = 899527000000
        actual = self.sys_vol_col.maximum_size
        self.assertEqual(expected, actual)
