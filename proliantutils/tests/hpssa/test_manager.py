# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import testtools

from proliantutils import exception
from proliantutils.hpssa import manager
from proliantutils.hpssa import objects
from proliantutils.tests.hpssa import raid_constants


@mock.patch.object(objects.Server, '_get_all_details')
class ManagerTestCases(testtools.TestCase):

    def _test_create_configuration_with_disk_input(self,
                                                   controller_exec_cmd_mock,
                                                   get_all_details_mock):
        ld1 = {'size_gb': 50,
               'raid_level': '1',
               'controller': 'Smart Array P822 in Slot 2',
               'physical_disks': ['5I:1:1',
                                  '5I:1:2']}
        ld2 = {'size_gb': 100,
               'raid_level': '5',
               'controller': 'Smart Array P822 in Slot 2',
               'physical_disks': ['5I:1:3',
                                  '5I:1:4',
                                  '6I:1:5']}

        raid_info = {'logical_disks': [ld1, ld2]}

        current_config = manager.create_configuration(raid_info)

        ld1_drives = '5I:1:1,5I:1:2'
        ld2_drives = '5I:1:3,5I:1:4,6I:1:5'
        controller_exec_cmd_mock.assert_any_call("create",
                                                 "type=logicaldrive",
                                                 "drives=%s" % ld2_drives,
                                                 "raid=5",
                                                 "size=%d" % (100*1024),
                                                 process_input='y')
        # Verify that we created the 50GB disk the last.
        controller_exec_cmd_mock.assert_called_with("create",
                                                    "type=logicaldrive",
                                                    "drives=%s" % ld1_drives,
                                                    "raid=1",
                                                    "size=%d" % (50*1024),
                                                    process_input='y')

        ld1_ret = [x for x in current_config['logical_disks']
                   if x['raid_level'] == '1'][0]
        ld2_ret = [x for x in current_config['logical_disks']
                   if x['raid_level'] == '5'][0]

        self.assertIsNotNone(ld1_ret['root_device_hint']['wwn'])
        self.assertIsNotNone(ld2_ret['root_device_hint']['wwn'])
        self.assertIsNotNone(ld1_ret['volume_name'])
        self.assertIsNotNone(ld2_ret['volume_name'])

        # Assert physical disk info
        pds_active = [x['id'] for x in current_config['physical_disks']
                      if x['status'] == 'active']
        pds_ready = [x['id'] for x in current_config['physical_disks']
                     if x['status'] == 'ready']
        pds_active_expected = ['5I:1:3', '5I:1:4', '6I:1:5',
                               '5I:1:1', '5I:1:2']
        pds_ready_expected = ['6I:1:6', '6I:1:7']
        self.assertEqual(sorted(pds_active_expected), sorted(pds_active))
        self.assertEqual(sorted(pds_ready_expected), sorted(pds_ready))

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_with_disk_input_create_succeeds(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES
        one_drive = raid_constants.HPSSA_ONE_DRIVE_100GB_RAID_5
        two_drives = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        self._test_create_configuration_with_disk_input(
            controller_exec_cmd_mock, get_all_details_mock)

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_with_disk_input_create_fails(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES
        one_drive = raid_constants.HPSSA_ONE_DRIVE_100GB_RAID_5
        get_all_details_mock.side_effect = [no_drives, one_drive, one_drive]
        ex = self.assertRaises(exception.HPSSAOperationError,
                               self._test_create_configuration_with_disk_input,
                               controller_exec_cmd_mock, get_all_details_mock)
        self.assertIn("raid_level '1' and size 50 GB not found", str(ex))

    def test_create_configuration_invalid_logical_disks(self,
                                                        get_all_details_mock):

        raid_info = {}
        self.assertRaises(exception.InvalidInputError,
                          manager.create_configuration,
                          raid_info)

        raid_info = {'logical_disks': 'foo'}
        self.assertRaises(exception.InvalidInputError,
                          manager.create_configuration,
                          raid_info)

        no_drives = raid_constants.HPSSA_NO_DRIVES
        get_all_details_mock.return_value = no_drives
        raid_info = {'logical_disks': [
                     {'size_gb': 50,
                      'raid_level': '1',
                      'controller': 'Smart Array P822 in Slot 0',
                      'physical_disks': ["6I:1:5", "6I:1:6"]}]}
        msg = ("Invalid Input: Unable to find controller named 'Smart Array "
               "P822 in Slot 0'. The available controllers are "
               "'Smart Array P822 in Slot 2'.")
        ex = self.assertRaises(exception.InvalidInputError,
                               manager.create_configuration,
                               raid_info)
        self.assertEqual(msg, str(ex))

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_without_disk_input_succeeds(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES
        one_drive = raid_constants.HPSSA_ONE_DRIVE_100GB_RAID_5
        two_drives = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        raid_info = {'logical_disks': [{'size_gb': 50,
                                        'raid_level': '1'},
                                       {'size_gb': 100,
                                        'raid_level': '5'}]}
        current_config = manager.create_configuration(raid_info)
        controller_exec_cmd_mock.assert_any_call("create",
                                                 "type=logicaldrive",
                                                 mock.ANY,
                                                 "raid=5",
                                                 "size=%d" % (100*1024),
                                                 process_input='y')
        # Verify that we created the 50GB disk the last.
        controller_exec_cmd_mock.assert_called_with("create",
                                                    "type=logicaldrive",
                                                    mock.ANY,
                                                    "raid=1",
                                                    "size=%d" % (50*1024),
                                                    process_input='y')

        ld1_ret = [x for x in current_config['logical_disks']
                   if x['raid_level'] == '1'][0]
        ld2_ret = [x for x in current_config['logical_disks']
                   if x['raid_level'] == '5'][0]
        self.assertEqual('0x600508b1001cc42c',
                         ld2_ret['root_device_hint']['wwn'])
        self.assertEqual('0x600508b1001ce1e1',
                         ld1_ret['root_device_hint']['wwn'])

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_without_disk_input_fails_on_disk_type(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES
        one_drive = raid_constants.HPSSA_ONE_DRIVE_100GB_RAID_5
        two_drives = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        raid_info = {'logical_disks': [{'size_gb': 50,
                                        'raid_level': '1',
                                        'disk_type': 'ssd'},
                                       {'size_gb': 100,
                                        'raid_level': '5',
                                        'disk_type': 'hdd'}]}
        exc = self.assertRaises(exception.PhysicalDisksNotFoundError,
                                manager.create_configuration,
                                raid_info)
        self.assertIn("of size 50 GB and raid level 1", str(exc))

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_share_physical_disks(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES_3_PHYSICAL_DISKS
        one_drive = raid_constants.ONE_DRIVE_RAID_1
        two_drives = raid_constants.TWO_DRIVES_50GB_RAID1
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        controller_exec_cmd_mock.side_effect = [
            (None, None),
            (raid_constants.DRIVE_2_RAID_1_OKAY_TO_SHARE, None),
            (None, None)]
        raid_info = {'logical_disks': [{'size_gb': 50,
                                        'share_physical_disks': True,
                                        'number_of_physical_disks': 2,
                                        'raid_level': '0',
                                        'disk_type': 'hdd'},
                                       {'size_gb': 50,
                                        'share_physical_disks': True,
                                        'raid_level': '1',
                                        'disk_type': 'hdd'}]}
        raid_info = manager.create_configuration(raid_info)
        ld1 = raid_info['logical_disks'][0]
        ld2 = raid_info['logical_disks'][1]
        self.assertEqual('Smart Array P822 in Slot 2', ld1['controller'])
        self.assertEqual('Smart Array P822 in Slot 2', ld2['controller'])
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ld1['physical_disks']))
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ld2['physical_disks']))
        controller_exec_cmd_mock.assert_any_call(
            'create', 'type=logicaldrive', 'drives=5I:1:1,5I:1:2',
            'raid=1', 'size=51200', process_input='y')
        controller_exec_cmd_mock.assert_any_call(
            'array', 'A', 'create', 'type=logicaldrive', 'raid=0', 'size=?',
            dont_transform_to_hpssa_exception=True)
        controller_exec_cmd_mock.assert_any_call(
            'array', 'A', 'create', 'type=logicaldrive', 'raid=0',
            'size=51200', process_input='y')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_share_nonshare_physical_disks(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.HPSSA_NO_DRIVES_3_PHYSICAL_DISKS
        one_drive = raid_constants.ONE_DRIVE_RAID_1
        two_drives = raid_constants.TWO_DRIVES_50GB_RAID1
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        controller_exec_cmd_mock.side_effect = [
            (None, None),
            (raid_constants.DRIVE_2_RAID_1_OKAY_TO_SHARE, None),
            (None, None)]
        raid_info = {'logical_disks': [{'size_gb': 50,
                                        'raid_level': '1',
                                        'disk_type': 'hdd'},
                                       {'size_gb': 50,
                                        'share_physical_disks': True,
                                        'raid_level': '0',
                                        'disk_type': 'hdd'}]}
        raid_info = manager.create_configuration(raid_info)
        ld1 = raid_info['logical_disks'][0]
        ld2 = raid_info['logical_disks'][1]
        self.assertEqual('Smart Array P822 in Slot 2', ld1['controller'])
        self.assertEqual('Smart Array P822 in Slot 2', ld2['controller'])
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ld1['physical_disks']))
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ld2['physical_disks']))
        controller_exec_cmd_mock.assert_any_call(
            'create', 'type=logicaldrive', 'drives=5I:1:1,5I:1:2',
            'raid=1', 'size=51200', process_input='y')
        controller_exec_cmd_mock.assert_any_call(
            'create', 'type=logicaldrive', 'drives=5I:1:3', 'raid=0',
            'size=51200', process_input='y')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration_max_as_size_gb(
            self, controller_exec_cmd_mock, get_all_details_mock):
        no_drives = raid_constants.NO_DRIVES_HPSSA_7_DISKS
        one_drive = raid_constants.ONE_DRIVE_RAID_1_50_GB
        two_drives = raid_constants.TWO_DRIVES_50GB_RAID1_MAXGB_RAID5
        get_all_details_mock.side_effect = [no_drives, one_drive, two_drives]
        raid_info = {'logical_disks': [{'size_gb': 50,
                                        'raid_level': '1',
                                        'disk_type': 'hdd'},
                                       {'size_gb': 'MAX',
                                        'raid_level': '5',
                                        'disk_type': 'hdd'}]}
        raid_info = manager.create_configuration(raid_info)
        ld1 = raid_info['logical_disks'][0]
        ld2 = raid_info['logical_disks'][1]
        self.assertEqual('Smart Array P822 in Slot 3', ld1['controller'])
        self.assertEqual('Smart Array P822 in Slot 3', ld2['controller'])
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ld1['physical_disks']))
        self.assertEqual(sorted(['5I:1:3', '5I:1:4', '6I:1:5']),
                         sorted(ld2['physical_disks']))
        controller_exec_cmd_mock.assert_any_call(
            'create', 'type=logicaldrive', 'drives=5I:1:1,5I:1:2',
            'raid=1', 'size=51200', process_input='y')
        controller_exec_cmd_mock.assert_any_call(
            'create', 'type=logicaldrive', 'drives=5I:1:3,5I:1:4,6I:1:5',
            'raid=5', process_input='y')

    def test__sort_shared_logical_disks(self, get_all_details_mock):
        logical_disk_sorted_expected = [
            {'size_gb': 500, 'disk_type': 'hdd', 'raid_level': '1'},
            {'share_physical_disks': True, 'size_gb': 450, 'disk_type': 'hdd',
             'number_of_physical_disks': 6, 'raid_level': '0'},
            {'share_physical_disks': True, 'size_gb': 200, 'disk_type': 'hdd',
             'raid_level': '1+0'},
            {'share_physical_disks': True, 'size_gb': 200, 'disk_type': 'hdd',
             'raid_level': '0'},
            {'share_physical_disks': True, 'size_gb': 100, 'disk_type': 'hdd',
             'raid_level': '0'}]
        logical_disks = [{'size_gb': 500,
                          'disk_type': 'hdd',
                          'raid_level': '1'},
                         {'share_physical_disks': True,
                          'size_gb': 450,
                          'disk_type': 'hdd',
                          'number_of_physical_disks': 6,
                          'raid_level': '0'},
                         {'share_physical_disks': True,
                          'size_gb': 200,
                          'disk_type': 'hdd',
                          'raid_level': '1+0'},
                         {'share_physical_disks': True,
                          'size_gb': 200,
                          'disk_type': 'hdd',
                          'raid_level': '0'},
                         {'share_physical_disks': True,
                          'size_gb': 100,
                          'disk_type': 'hdd',
                          'raid_level': '0'}]
        logical_disks_sorted = manager._sort_shared_logical_disks(
            logical_disks)
        self.assertEqual(logical_disks_sorted, logical_disk_sorted_expected)

    def test__sort_shared_logical_disks_raid10(self, get_all_details_mock):
        logical_disk_sorted_expected = [
            {'size_gb': 600, 'disk_type': 'hdd', 'raid_level': '1'},
            {'share_physical_disks': False, 'size_gb': 400, 'disk_type': 'hdd',
             'raid_level': '1+0'},
            {'share_physical_disks': False, 'size_gb': 100, 'disk_type': 'hdd',
             'raid_level': '5'},
            {'share_physical_disks': True, 'size_gb': 550, 'disk_type': 'hdd',
             'raid_level': '1'},
            {'share_physical_disks': True, 'size_gb': 200, 'disk_type': 'hdd',
             'raid_level': '1+0'},
            {'share_physical_disks': True, 'size_gb': 450, 'disk_type': 'hdd',
             'number_of_physical_disks': 5, 'raid_level': '0'},
            {'share_physical_disks': True, 'size_gb': 300, 'disk_type': 'hdd',
             'raid_level': '5'}]
        logical_disks = [
            {'size_gb': 600, 'disk_type': 'hdd', 'raid_level': '1'},
            {'share_physical_disks': True, 'size_gb': 550, 'disk_type': 'hdd',
             'raid_level': '1'},
            {'share_physical_disks': True, 'size_gb': 450, 'disk_type': 'hdd',
             'number_of_physical_disks': 5, 'raid_level': '0'},
            {'share_physical_disks': False, 'size_gb': 400, 'disk_type': 'hdd',
             'raid_level': '1+0'},
            {'share_physical_disks': True, 'size_gb': 300, 'disk_type': 'hdd',
             'raid_level': '5'},
            {'share_physical_disks': True, 'size_gb': 200, 'disk_type': 'hdd',
             'raid_level': '1+0'},
            {'share_physical_disks': False, 'size_gb': 100, 'disk_type': 'hdd',
             'raid_level': '5'}]
        logical_disks_sorted = manager._sort_shared_logical_disks(
            logical_disks)
        self.assertEqual(logical_disks_sorted, logical_disk_sorted_expected)

    @mock.patch.object(manager, 'get_configuration')
    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_delete_configuration(self, controller_exec_cmd_mock,
                                  get_configuration_mock,
                                  get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        get_configuration_mock.return_value = 'foo'

        ret = manager.delete_configuration()

        controller_exec_cmd_mock.assert_called_with(
            "logicaldrive", "all", "delete", "forced")
        get_configuration_mock.assert_called_once_with()
        self.assertEqual('foo', ret)

    @mock.patch.object(manager, 'get_configuration')
    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_delete_configuration_no_arrays(
            self, controller_exec_cmd_mock,
            get_configuration_mock, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES
        get_configuration_mock.return_value = 'foo'

        ret = manager.delete_configuration()

        self.assertFalse(controller_exec_cmd_mock.called)
        get_configuration_mock.assert_called_once_with()
        self.assertEqual('foo', ret)

    def test_get_configuration(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        raid_info_returned = manager.get_configuration()

        ld1_expected = {'size_gb': 557,
                        'raid_level': '1',
                        'controller': 'Smart Array P822 in Slot 2',
                        'physical_disks': ['5I:1:1',
                                           '5I:1:2'],
                        'volume_name': '01F42227PDVTF0BRH5T0MOAB64',
                        'root_device_hint': {
                            'wwn': '0x600508b1001c321c'}}

        # NOTE(rameshg87: Cannot directly compare because
        # of 'physical_disks' key.
        ld1_returned = raid_info_returned['logical_disks'][0]
        self.assertEqual(ld1_expected['size_gb'],
                         ld1_returned['size_gb'])
        self.assertEqual(ld1_expected['raid_level'],
                         ld1_returned['raid_level'])
        self.assertEqual(ld1_expected['controller'],
                         ld1_returned['controller'])
        self.assertEqual(ld1_expected['volume_name'],
                         ld1_returned['volume_name'])
        self.assertEqual(ld1_expected['root_device_hint'],
                         ld1_returned['root_device_hint'])
        self.assertEqual(sorted(ld1_expected['physical_disks']),
                         sorted(ld1_returned['physical_disks']))

        # Assert physical disk info
        pds_active = [x['id'] for x in raid_info_returned['physical_disks']
                      if x['status'] == 'active']
        pds_ready = [x['id'] for x in raid_info_returned['physical_disks']
                     if x['status'] == 'ready']
        pds_active_expected = ['5I:1:1', '5I:1:2']
        pds_ready_expected = ['6I:1:6', '6I:1:7', '5I:1:3',
                              '5I:1:4', '6I:1:5']
        self.assertEqual(sorted(pds_active_expected), sorted(pds_active))
        self.assertEqual(sorted(pds_ready_expected), sorted(pds_ready))


class RaidConfigValidationTestCases(testtools.TestCase):

    def test_validate_fails_min_disks_number(self):
        raid_config = {'logical_disks':
                       [{'size_gb': 100,
                         'raid_level': '5',
                         'number_of_physical_disks': 2}]}
        msg = "RAID level 5 requires at least 3 disks"
        self.assertRaisesRegex(exception.InvalidInputError, msg,
                               manager.validate, raid_config)

    def test_validate_fails_min_physical_disks(self):
        raid_config = {'logical_disks':
                       [{'size_gb': 100, 'raid_level': '5',
                         'physical_disks': ['foo']}]}
        msg = "RAID level 5 requires at least 3 disks"
        self.assertRaisesRegex(exception.InvalidInputError, msg,
                               manager.validate, raid_config)
