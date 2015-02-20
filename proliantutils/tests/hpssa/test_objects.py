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
from oslo.concurrency import processutils
import testtools

from proliantutils import exception
from proliantutils.hpssa import objects
from proliantutils.hpssa import types
from proliantutils.tests.hpssa import raid_constants


@mock.patch.object(objects.Server, '_get_all_details')
class ServerTest(testtools.TestCase):

    def test_server_object_no_logical_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()

        # Assertions on server
        self.assertEqual(1, len(server.controllers))

        # Assertions on RAID controller properties
        controller = server.controllers[0]
        self.assertEqual(server, controller.parent)
        self.assertIsInstance(controller.properties, dict)
        self.assertEqual('Smart Array P822 in Slot 2', controller.id)
        self.assertEqual(7, len(controller.unassigned_physical_drives))
        self.assertFalse(controller.raid_arrays)

        # Assertion on physical drives on controller
        physical_drives_expected = ['5I:1:1', '5I:1:2', '5I:1:3', '5I:1:4',
                                    '6I:1:5', '6I:1:6', '6I:1:7']
        physical_drives_found = map(lambda x: x.id,
                                    controller.unassigned_physical_drives)
        self.assertEqual(sorted(physical_drives_expected),
                         sorted(physical_drives_found))

        physical_drive = filter(lambda x: x.id == '5I:1:1',
                                controller.unassigned_physical_drives)[0]
        self.assertEqual(controller, physical_drive.parent)
        self.assertEqual(600, physical_drive.size_gb)
        self.assertEqual(types.INTERFACE_TYPE_SAS,
                         physical_drive.interface_type)
        self.assertEqual(types.DISK_TYPE_HDD,
                         physical_drive.disk_type)

    def test_server_object_one_logical_drive(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()

        controller = server.controllers[0]
        self.assertEqual(5, len(controller.unassigned_physical_drives))
        self.assertEqual(1, len(controller.raid_arrays))

        # Assertion on raid_arrays
        array = controller.raid_arrays[0]
        self.assertEqual(array.parent, controller)
        self.assertIsInstance(array.properties, dict)
        self.assertEqual('A', array.id)
        self.assertEqual(1, len(array.logical_drives))
        self.assertEqual(2, len(array.physical_drives))

        # Assertion on logical drives of array
        logical_drive = array.logical_drives[0]
        self.assertEqual('1', logical_drive.id)
        self.assertEqual(logical_drive.parent, array)
        self.assertEqual(558, logical_drive.size_gb)
        self.assertEqual(types.RAID_1, logical_drive.raid_level)
        self.assertIsInstance(logical_drive.properties, dict)

        # Assertion on physical drives of array
        physical_drive = filter(lambda x: x.id == '5I:1:1',
                                array.physical_drives)[0]
        self.assertEqual(array, physical_drive.parent)
        self.assertEqual(600, physical_drive.size_gb)

        # Assertion on physical drives of controller
        physical_drive = filter(lambda x: x.id == '5I:1:3',
                                controller.unassigned_physical_drives)[0]
        self.assertEqual(controller, physical_drive.parent)
        self.assertEqual(600, physical_drive.size_gb)

    def test_get_controller_by_id(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()

        id = 'Smart Array P822 in Slot 2'
        self.assertEqual(server.controllers[0],
                         server.get_controller_by_id(id))
        self.assertIsNone(server.get_controller_by_id('foo'))

    def test_get_logical_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()

        exp_ld = server.controllers[0].raid_arrays[0].logical_drives[0]
        self.assertEqual(exp_ld, server.get_logical_drives()[0])

    def test_get_logical_drives_no_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        self.assertFalse(server.get_logical_drives())


@mock.patch.object(objects.Server, '_get_all_details')
class ControllerTest(testtools.TestCase):

    @mock.patch.object(processutils, 'execute')
    def test_execute_cmd(self, processutils_mock, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        processutils_mock.return_value = ('stdout', 'stderr')

        stdout, stderr = controller.execute_cmd('foo', 'bar')

        processutils_mock.assert_called_once_with("hpssacli",
                                                  "controller",
                                                  "slot=2",
                                                  "foo",
                                                  "bar")
        self.assertEqual(stdout, 'stdout')
        self.assertEqual(stderr, 'stderr')

    @mock.patch.object(processutils, 'execute')
    def test_execute_cmd_fails(self, processutils_mock, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES
        server = objects.Server()
        controller = server.controllers[0]

        processutils_mock.side_effect = OSError

        self.assertRaises(exception.HPSSAOperationError,
                          controller.execute_cmd,
                          'foo', 'bar')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_logical_drive(self, execute_mock,
                                  get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        logical_drive_info = {'size_gb': 50,
                              'raid_level': '1',
                              'volume_name': 'boot_volume',
                              'is_boot_volume': 'true',
                              'controller': 'Smart Array P822 in Slot 2',
                              'physical_disks': ['5I:1:1',
                                                 '5I:1:2',
                                                 '5I:1:3']}

        controller.create_logical_drive(logical_drive_info,
                                        ['5I:1:1',
                                         '5I:1:2',
                                         '5I:1:3'])
        execute_mock.assert_called_once_with("create",
                                             "type=logicaldrive",
                                             "drives=5I:1:1,5I:1:2,5I:1:3",
                                             "raid=1",
                                             "size=51200")

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_delete_all_logical_drives(self, execute_mock,
                                       get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        controller.delete_all_logical_drives()
        execute_mock.assert_called_once_with("logicaldrive", "all",
                                             "delete", "forced")

    def test_get_physical_drive_by_id(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()
        controller = server.controllers[0]
        array = controller.raid_arrays[0]

        physical_drive = filter(lambda x: x.id == '5I:1:1',
                                array.physical_drives)[0]
        self.assertEqual(physical_drive,
                         controller.get_physical_drive_by_id('5I:1:1'))

        physical_drive = filter(lambda x: x.id == '5I:1:3',
                                controller.unassigned_physical_drives)[0]
        self.assertEqual(physical_drive,
                         controller.get_physical_drive_by_id('5I:1:3'))

        self.assertIsNone(controller.get_physical_drive_by_id('foo'))
