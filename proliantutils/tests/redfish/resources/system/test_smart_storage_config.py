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

from proliantutils.hpssa import manager
from proliantutils.redfish.resources.system import smart_storage_config


class HPESmartStorageConfigTestCase(testtools.TestCase):

    def setUp(self):
        super(HPESmartStorageConfigTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/smart_storage_config.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.ssc_inst = smart_storage_config.HPESmartStorageConfig(
            self.conn, '/redfish/v1/Systems/1/smartstorageconfig',
            redfish_version='1.0.2')

    def test__get_smart_storage_config_url(self):
        expected_url = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        observed_url = self.ssc_inst._get_smart_storage_config_url()
        self.assertEqual(expected_url, observed_url)

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

    @mock.patch.object(manager, 'validate', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_get_smart_storage_config_url', autospec=True)
    def test_create_raid(self, url_mock, validate_mock):
        ld1 = {'size_gb': 50,
               'raid_level': '1',
               'physical_disks': ['5I:1:1',
                                  '5I:1:2']}
        raid_config = {'logical_disks': [ld1]}
        validate_mock.return_value = True
        self.ssc_inst.create_raid(raid_config)
        validate_mock.assert_called_once_with(raid_config)
        self.assertTrue(url_mock.called)
        self.assertTrue(self.ssc_inst._conn.put.called)

    @mock.patch.object(manager, 'validate', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_get_smart_storage_config_url', autospec=True)
    def test_create_raid_multiple_logical_drives(self, url_mock,
                                                 validate_mock):
        ld1 = {'size_gb': 50,
               'raid_level': '0',
               'physical_disks': ['5I:1:1']}
        ld2 = {'size_gb': 100,
               'raid_level': '1',
               'number_of_physical_disks': 2}
        raid_config = {'logical_disks': [ld1, ld2]}
        validate_mock.return_value = True
        self.ssc_inst.create_raid(raid_config)
        validate_mock.assert_called_once_with(raid_config)
        self.assertTrue(url_mock.called)
        self.assertTrue(self.ssc_inst._conn.put.called)
