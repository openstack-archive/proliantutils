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

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_configuration(self, controller_exec_cmd_mock,
                                  get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

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

        manager.create_configuration(raid_info)

        ld1_drives = '5I:1:1,5I:1:2'
        ld2_drives = '5I:1:3,5I:1:4,6I:1:5'
        controller_exec_cmd_mock.assert_any_call("create",
                                                 "type=logicaldrive",
                                                 "drives=%s" % ld2_drives,
                                                 "raid=5",
                                                 "size=%d" % (100*1024))
        # Verify that we created the 50GB disk the last.
        controller_exec_cmd_mock.assert_called_with("create",
                                                    "type=logicaldrive",
                                                    "drives=%s" % ld1_drives,
                                                    "raid=1",
                                                    "size=%d" % (50*1024))

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

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_delete_configuration(self, controller_exec_cmd_mock,
                                  get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        manager.delete_configuration()

        controller_exec_cmd_mock.assert_called_with("logicaldrive",
                                                    "all",
                                                    "delete",
                                                    "forced")

    def test_get_configuration(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        raid_info_returned = manager.get_configuration()

        ld1_expected = {'size_gb': 558,
                        'raid_level': '1',
                        'controller': 'Smart Array P822 in Slot 2',
                        'physical_disks': ['5I:1:1',
                                           '5I:1:2'],
                        'volume_name': '01F42227PDVTF0BRH5T0MOAB64',
                        'root_device_hint': {
                            'wwn': '600508B1001C321CCA06EB7CD847939D'}}

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
