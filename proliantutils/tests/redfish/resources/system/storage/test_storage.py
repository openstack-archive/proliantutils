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
        storage_file = 'proliantutils/tests/redfish/json_samples/storage1.json'
        with open(storage_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

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
        expected_controller = [{
            "@odata.id": "/redfish/v1/Systems/437XR1138R2/Storage/1#/"
                         "StorageControllers/0",
            "@odata.type": "#Storage.v1_0_0.StorageController",
            "Id": "0",
            "Name": "Contoso Integrated RAID",
            "Description": "Contoso Integrated RAID",
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "Identifiers": [{
                "DurableNameFormat": "NAA",
                "DurableName": "345C59DBD970859C"
            }],
            "Manufacturer": "Contoso",
            "Model": "12Gbs Integrated RAID",
            "SerialNumber": "2M220100SL",
            "PartNumber": "CT18754",
            "SpeedGbps": 12,
            "FirmwareVersion": "1.0.0.7",
            "SupportedControllerProtocols": [
                "PCIe"
            ],
            "SupportedDeviceProtocols": [
                "SAS",
                "SATA"
            ]
            }]
        self.assertEqual(expected_controller,
                         self.sys_stor.storage_controllers)
        drives = [{
            "@odata.id": "/redfish/v1/Systems/437XR1138R2/Storage/1/"
                         "Drives/35D38F11ACEF7BD3"
            }, {
            "@odata.id": "/redfish/v1/Systems/437XR1138R2/Storage/1/"
                         "Drives/3F5A8C54207B7233"
            }]
        self.assertEqual(drives, self.sys_stor.drives)

    def test_volumes(self):
        log_coll = None
        log_dr = None
        self.assertIsNone(self.sys_stor._volumes)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/volume1_collection.json') as f:
            log_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/volume1.json') as f:
            log_dr = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [log_coll, log_dr]
        actual_log_dr = self.sys_stor.volumes
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_log_dr,
                      self.sys_stor.volumes)
        self.conn.get.return_value.json.assert_not_called()

    def test_drives_list(self):
        dr1 = None
        dr2 = None
        self.assertIsNone(self.sys_stor._drives_list)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/drive1.json') as f:
            dr1 = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/drive2.json') as f:
            dr2 = json.loads(f.read())
        self.conn.get.return_value.json.side_effect = [dr1, dr2]
        actual_dr = self.sys_stor.drives_list
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_dr,
                      self.sys_stor.drives_list)
        self.conn.get.return_value.json.assert_not_called()

    def test_drives_maximum_size_bytes(self):
        self.assertIsNone(self.sys_stor._drives_maximum_size_bytes)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive2.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor.drives_maximum_size_bytes
        self.assertEqual(expected, actual)


class StorageCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/json_samples/'
                  'storage1_collection.json', 'r') as f:
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
        self.assertIsNone(self.sys_stor_col._volumes_maximum_size_bytes)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'volume1_collection.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'volume1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor_col.volumes_maximum_size_bytes
        self.assertEqual(expected, actual)

    def test_drives_maximum_size_bytes(self):
        self.assertIsNone(self.sys_stor_col._drives_maximum_size_bytes)
        self.conn.get.return_value.json.reset_mock()
        val = []
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive1.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
        path = ('proliantutils/tests/redfish/json_samples/'
                'drive2.json')
        with open(path, 'r') as f:
            val.append(json.loads(f.read()))
            self.conn.get.return_value.json.side_effect = val
        expected = 899527000000
        actual = self.sys_stor_col.drives_maximum_size_bytes
        self.assertEqual(expected, actual)
