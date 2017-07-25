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

from proliantutils.redfish.resources.system.storage import simple_storage


class SimpleStorageTestCase(testtools.TestCase):

    def setUp(self):
        super(SimpleStorageTestCase, self).setUp()
        self.conn = mock.Mock()
        simple_file = ('proliantutils/tests/redfish/json_samples/'
                       'simple_storage.json')
        with open(simple_file, 'r') as f:
            self.simple_storage_json = json.loads(f.read())
            self.conn.get.return_value.json.return_value = self.simple_storage_json

        simple_path = ("/redfish/v1/Systems/437XR1138R2/SimpleStorage/1")
        self.sys_simple = simple_storage.SimpleStorage(
            self.conn, simple_path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_simple._parse_attributes()
        self.assertEqual('1.0.2', self.sys_simple.redfish_version)
        self.assertEqual('1', self.sys_simple.identity)
        self.assertEqual('Simple Storage Controller', self.sys_simple.name)
        self.assertEqual('System SATA', self.sys_simple.description)
        self.assertEqual(self.simple_storage_json.get('Devices'),
                         self.sys_simple.devices)

    def test_maximum_size_bytes(self):
        self.assertIsNone(self.sys_simple._maximum_size_bytes)
        self.conn.get.return_value.json.reset_mock()
        expected = 8000000000000
        actual = self.sys_simple.maximum_size_bytes
        self.assertEqual(expected, actual)


class SimpleStorageCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(SimpleStorageCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'simple_storage_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_simple_col = simple_storage.SimpleStorageCollection(
            self.conn, '/redfish/v1/Systems/437XR1138R2/SimpleStorage',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_simple_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_simple_col.redfish_version)
        self.assertEqual('Simple Storage Collection',
                         self.sys_simple_col.name)
        simple_path = ('/redfish/v1/Systems/437XR1138R2/SimpleStorage/1',)
        self.assertEqual(simple_path, self.sys_simple_col.members_identities)

    @mock.patch.object(simple_storage, 'SimpleStorage', autospec=True)
    def test_get_member(self, mock_simple):
        self.sys_simple_col.get_member(
            '/redfish/v1/Systems/437XR1138R2/SimpleStorage/1')
        mock_simple.assert_called_once_with(
            self.sys_simple_col._conn,
            '/redfish/v1/Systems/437XR1138R2/SimpleStorage/1',
            redfish_version=self.sys_simple_col.redfish_version)

    @mock.patch.object(simple_storage, 'SimpleStorage', autospec=True)
    def test_get_members(self, mock_simple):
        members = self.sys_simple_col.get_members()
        simple_path = ("/redfish/v1/Systems/437XR1138R2/SimpleStorage/1")
        calls = [
            mock.call(self.sys_simple_col._conn, simple_path,
                      redfish_version=self.sys_simple_col.redfish_version),
        ]
        mock_simple.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test_maximum_size_bytes(self):
        self.assertIsNone(self.sys_simple_col._maximum_size_bytes)
        self.conn.get.return_value.json.reset_mock()
        path = ('proliantutils/tests/redfish/json_samples/'
                'simple_storage.json')
        with open(path, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        expected = 8000000000000
        actual = self.sys_simple_col.maximum_size_bytes
        self.assertEqual(expected, actual)
