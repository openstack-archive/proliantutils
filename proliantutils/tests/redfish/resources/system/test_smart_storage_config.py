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
from proliantutils.hpssa import manager
from proliantutils.redfish.resources.system import smart_storage_config


class HPESmartStorageConfigTestCase(testtools.TestCase):

    def setUp(self):
        super(HPESmartStorageConfigTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/smart_storage_config.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.load(f))

        self.ssc_inst = smart_storage_config.HPESmartStorageConfig(
            self.conn, '/redfish/v1/Systems/1/smartstorageconfig',
            redfish_version='1.0.2')

    def test_attributes(self):
        physical_drive = [{'LegacyBootPriority': 'None',
                           'Location': '1I:1:2',
                           'LocationFormat': 'ControllerPort:Box:Bay'}]
        self.assertEqual('smartstorageconfig', self.ssc_inst.controller_id)
        self.assertEqual('Slot 0', self.ssc_inst.location)
        self.assertEqual(physical_drive, self.ssc_inst.physical_drives)
        self.assertEqual(
            '600508B1001C045A9BAAC9F4F49498AE',
            self.ssc_inst.logical_drives[0].volume_unique_identifier)
        self.assertEqual("/redfish/v1/systems/1/smartstorageconfig/settings/",
                         self.ssc_inst.settings_uri)

    def test_delete_raid(self):
        settings_uri = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        data = {
            "LogicalDrives": [{
                "Actions": [{"Action": "LogicalDriveDelete"}],
                "VolumeUniqueIdentifier": "600508B1001C045A9BAAC9F4F49498AE"}],
            "DataGuard": "Permissive",
        }
        self.ssc_inst.delete_raid()
        self.ssc_inst._conn.put.assert_called_once_with(settings_uri,
                                                        data=data)

    def test_delete_raid_logical_drive_not_found(self):
        type(self.ssc_inst).logical_drives = mock.PropertyMock(
            return_value=[])
        self.assertRaises(exception.IloLogicalDriveNotFoundError,
                          self.ssc_inst.delete_raid)

    @mock.patch.object(manager, 'validate', autospec=True)
    def test_create_raid(self, validate_mock):
        settings_uri = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        ld1 = {'size_gb': 50,
               'raid_level': '1',
               'physical_disks': ['5I:1:1', '5I:1:2']}
        raid_config = {'logical_disks': [ld1]}
        validate_mock.return_value = True
        self.ssc_inst.create_raid(raid_config)
        data = {"DataGuard": "Disabled",
                "LogicalDrives": [
                    {"CapacityGiB": 50, "Raid": "Raid1",
                     "DataDrives": ['5I:1:1', '5I:1:2']}]}
        validate_mock.assert_called_once_with(raid_config)
        self.ssc_inst._conn.put.assert_called_once_with(settings_uri,
                                                        data=data)

    @mock.patch.object(manager, 'validate', autospec=True)
    def test_create_raid_multiple_logical_drives(self, validate_mock):
        settings_uri = "/redfish/v1/systems/1/smartstorageconfig/settings/"
        ld1 = {'size_gb': 50,
               'raid_level': '0',
               'physical_disks': ['5I:1:1']}
        ld2 = {'size_gb': 100,
               'raid_level': '1',
               'number_of_physical_disks': 2}
        raid_config = {'logical_disks': [ld1, ld2]}
        validate_mock.return_value = True
        self.ssc_inst.create_raid(raid_config)
        data = {"DataGuard": "Disabled",
                "LogicalDrives": [
                    {"CapacityGiB": 50, "Raid": "Raid0",
                     "DataDrives": ['5I:1:1']},
                    {"CapacityGiB": 100, "Raid": "Raid1",
                     "DataDrives": {"DataDriveCount": 2}}]}
        validate_mock.assert_called_once_with(raid_config)
        self.ssc_inst._conn.put.assert_called_once_with(settings_uri,
                                                        data=data)

    def test__generic_format_delete_scenario(self):
        expected_data = []
        raid_config = {"LogicalDrives": []}
        self.assertEqual(expected_data,
                         self.ssc_inst._generic_format(raid_config))

    def test__generic_format_create_scenario(self):
        expected_data = [{'controller': 'HPE Smart Array P408i-p SR Gen10',
                          'physical_disks': [u'2I:1:2', u'2I:1:1'],
                          'raid_level': u'0',
                          'root_device_hint': {
                              'wwn': u'0x600508B1001C045A9BAAC9F4F49498AE'},
                          'size_gb': 2235,
                          'volume_name': u'01A27294PFJHD0ARCA218H 63E0'}]
        result = self.ssc_inst._generic_format(
            self.ssc_inst.json, controller='HPE Smart Array P408i-p SR Gen10')
        self.assertEqual(expected_data, result)

    def test__check_smart_storage_message(self):
        result, mesg = self.ssc_inst._check_smart_storage_message()
        self.assertEqual(True, result)
        self.assertEqual("", mesg)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_generic_format', autospec=True)
    def test_read_raid_post_create(self, format_mock, message_mock):
        message_mock.return_value = True, 'Success'
        ld1 = {"size_gb": 150, "raid_level": '0', "is_root_volume": True}
        type(self.ssc_inst).logical_drives = mock.PropertyMock(
            return_value=[ld1])
        ld1['controller'] = 'HPE Smart Array P408i-p SR Gen10'
        format_mock.return_value = [ld1]
        expected = {'logical_disks': [ld1]}
        self.assertEqual(
            expected, self.ssc_inst.read_raid(controller=ld1['controller']))
        self.assertTrue(message_mock.called)
        self.assertTrue(format_mock.called)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_generic_format', autospec=True)
    def test_read_raid_post_delete(self, format_mock, message_mock):
        message_mock.return_value = True, 'Success'
        format_mock.return_value = []
        type(self.ssc_inst).logical_drives = mock.PropertyMock(
            return_value=[])
        expected = {'logical_disks': []}
        self.assertEqual(expected, self.ssc_inst.read_raid())
        self.assertTrue(message_mock.called)
        self.assertTrue(format_mock.called)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    def test_read_raid_failed(self, message_mock):
        ld1 = {"size_gb": 150, "raid_level": '0', "is_root_volume": True}
        type(self.ssc_inst).logical_drives = mock.PropertyMock(
            return_value=[ld1])
        ld1['controller'] = 'HPE Smart Array P408i-p SR Gen10'
        physical_drive = [{'LegacyBootPriority': 'None',
                           'Location': '1I:1:2',
                           'LocationFormat': 'ControllerPort:Box:Bay'}]
        type(self.ssc_inst).physical_drives = mock.PropertyMock(
            return_value=physical_drive)
        message_mock.return_value = False, 'err_mesg'
        self.assertRaisesRegexp(
            exception.IloError,
            'Failed to perform the create_raid operation successfully',
            self.ssc_inst.read_raid, ld1['controller'])

    def test_read_raid_logical_drive_not_found(self):
        type(self.ssc_inst).logical_drives = mock.PropertyMock(
            return_value=[])
        model = 'HPE Smart Array P408i-p SR Gen10'
        self.assertRaises(exception.IloLogicalDriveNotFoundError,
                          self.ssc_inst.read_raid, model)

    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_check_smart_storage_message', autospec=True)
    @mock.patch.object(smart_storage_config.HPESmartStorageConfig,
                       '_generic_format', autospec=True)
    def test_read_raid_controller_not_configured_post_delete(
            self, format_mock, message_mock):
        message_mock.return_value = False, ''
        type(self.ssc_inst).physical_drives = mock.PropertyMock(
            return_value=None)
        self.ssc_inst.read_raid()
        self.assertTrue(message_mock.called)
        self.assertFalse(format_mock.called)
