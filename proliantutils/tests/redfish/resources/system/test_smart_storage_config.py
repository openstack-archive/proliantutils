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

from proliantutils import exception
from proliantutils.redfish.resources.system import smart_storage_config


class HPESmartStorageConfigTestCase(testtools.TestCase):

    def setUp(self):
        super(HPESmartStorageConfigTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/smart_storage_config.json', 'r') as f:
            ssc_json = json.loads(f.read())
            self.conn.get.return_value.json.return_value = ssc_json['default']

        self.ssc_inst = smart_storage_config.HPESmartStorageConfig(
            self.conn, '/redfish/v1/Systems/1/smartstorageconfig',
            redfish_version='1.0.2')

    def test__get_smart_storage_config_url(self):
        expected_url = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        observed_url = self.ssc_inst._get_smart_storage_config_url()
        self.assertEqual(expected_url, observed_url)


    def test__generic_format_delete_scenario(self):
        expected_data = []
        raid_config = self.conn.get.return_value.json.return_value
        result = self.ssc_inst._generic_format(raid_config)
        self.assertEqual(expected_data, result)

    def test__generic_format_create_scenario(self):
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/smart_storage_config.json', 'r') as f:
            ssc_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = (
            ssc_json['create_config'])
        self.ssc_inst = smart_storage_config.HPESmartStorageConfig(
            self.conn, '/redfish/v1/Systems/1/smartstorageconfig',
            redfish_version='1.0.2')
        raid_config = self.conn.get.return_value.json.return_value
        result = self.ssc_inst._generic_format(raid_config)
        fields = ['size_gb', 'raid_level', 'root_device_hint', 'controller',
                  'physical_disks', 'volume_name']
        for data in result:
            data_fields = data.keys()
            for f in fields:
                self.assertEqual(True, f in data_fields)

    def test__check_smart_storage_message(self):
        result, mesg = self.ssc_inst._check_smart_storage_message()
        self.assertEqual(True, result)
        self.assertEqual("", mesg)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_get_smart_storage_config_url', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_generic_format', autospec=True)
    def test_read_raid(self, format_mock, url_mock, message_mock):
        message_mock.return_value = True, 'Success'
        url_mock.return_value = "test_url"
        format_mock.return_value = "formatted_data"
        self.ssc_inst.read_raid()
        self.assertTrue(url_mock.called)
        self.assertTrue(message_mock.called)
        self.assertTrue(format_mock.called)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    def test_read_raid_failed(self, message_mock):
        message_mock.return_value = False, 'err_mesg'
        self.assertRaisesRegex(
            exception.IloError,
            'Failed to perform the raid operation successfully',
            self.ssc_inst.read_raid)

    def test_delete_raid(self):
        settings_uri = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        data = {
            "LogicalDrives": [],
            "DataGuard": "Disabled",
            "PhysicalDrives": [{'LegacyBootPriority': 'None',
                                'Location': '1I:1:2',
                                'LocationFormat': 'ControllerPort:Box:Bay'}],
            "Actions": [{"Action": "FactoryReset"}]
        }
        self.ssc_inst.delete_raid()
        self.ssc_inst._conn.put.assert_called_once_with(settings_uri,
                                                        data=data)

