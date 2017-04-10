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
from oslo_concurrency import processutils
import testtools

from proliantutils import exception
from proliantutils.hpssa import constants
from proliantutils.hpssa import objects
from proliantutils.tests.unit.hpssa import raid_constants


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

        physical_drive = list(filter(lambda x: x.id == '5I:1:1',
                                     controller.unassigned_physical_drives))[0]
        self.assertEqual(controller, physical_drive.parent)
        self.assertEqual(500, physical_drive.size_gb)
        self.assertEqual(constants.INTERFACE_TYPE_SAS,
                         physical_drive.interface_type)
        self.assertEqual(constants.DISK_TYPE_HDD,
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
        self.assertEqual(557, logical_drive.size_gb)
        self.assertEqual(constants.RAID_1, logical_drive.raid_level)
        self.assertIsInstance(logical_drive.properties, dict)

        # Assertion on physical drives of array
        physical_drive = list(filter(lambda x: x.id == '5I:1:1',
                                     array.physical_drives))[0]
        self.assertEqual(array, physical_drive.parent)
        self.assertEqual(500, physical_drive.size_gb)

        # Assertion on physical drives of controller
        physical_drive = list(filter(lambda x: x.id == '5I:1:3',
                                     controller.unassigned_physical_drives))[0]
        self.assertEqual(controller, physical_drive.parent)
        self.assertEqual(400, physical_drive.size_gb)

    def test_server_object_one_logical_drive_raid_level_mappping(
            self, get_all_details_mock):
        stdout = raid_constants.HPSSA_ONE_DRIVE_RAID_50
        get_all_details_mock.return_value = stdout

        server = objects.Server()

        logical_drive = server.controllers[0].raid_arrays[0].logical_drives[0]
        self.assertEqual(constants.RAID_50, logical_drive.raid_level)

    def test_get_controller_by_id(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()

        id = 'Smart Array P822 in Slot 2'
        self.assertEqual(server.controllers[0],
                         server.get_controller_by_id(id))
        self.assertIsNone(server.get_controller_by_id('foo'))

    def test_get_physical_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        exp_pds = [server.controllers[0].unassigned_physical_drives[0],
                   server.controllers[0].unassigned_physical_drives[1],
                   server.controllers[0].unassigned_physical_drives[2],
                   server.controllers[0].unassigned_physical_drives[3],
                   server.controllers[0].unassigned_physical_drives[4],
                   server.controllers[0].raid_arrays[0].physical_drives[0],
                   server.controllers[0].raid_arrays[0].physical_drives[1]]
        self.assertEqual(exp_pds, server.get_physical_drives())

    def test_get_logical_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE

        server = objects.Server()

        exp_ld = server.controllers[0].raid_arrays[0].logical_drives[0]
        self.assertEqual(exp_ld, server.get_logical_drives()[0])

    def test_get_logical_drives_no_drives(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        self.assertFalse(server.get_logical_drives())

    def test_get_logical_drive_by_wwn(self, get_all_details_mock):

        two_drives = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = two_drives
        server = objects.Server()

        wwn = '0x600508b1001cc42c'
        ld_ret = server.get_logical_drive_by_wwn(wwn)
        raid_arrays = server.controllers[0].raid_arrays
        ld_exp = [x.logical_drives[0] for x in raid_arrays
                  if x.logical_drives[0].raid_level == '5'][0]
        self.assertEqual(ld_exp, ld_ret)

    def test_get_logical_drive_by_wwn_not_exist(self, get_all_details_mock):

        two_drives = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = two_drives
        server = objects.Server()

        wwn = 'foo'
        ld_ret = server.get_logical_drive_by_wwn(wwn)
        self.assertIsNone(ld_ret)


@mock.patch.object(objects.Server, '_get_all_details')
class ControllerTest(testtools.TestCase):

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test_execute_cmd(self, processutils_mock, path_mock,
                         get_all_details_mock):
        path_mock.return_value = True
        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        processutils_mock.return_value = ('stdout', 'stderr')

        stdout, stderr = controller.execute_cmd('foo', 'bar')

        processutils_mock.assert_called_once_with("ssacli",
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
    def test_create_logical_drive_with_physical_disks(self, execute_mock,
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

        controller.create_logical_drive(logical_drive_info)
        execute_mock.assert_called_once_with("create",
                                             "type=logicaldrive",
                                             "drives=5I:1:1,5I:1:2,5I:1:3",
                                             "raid=1",
                                             "size=51200", process_input='y')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_logical_drive_max_size_gb(self, execute_mock,
                                              get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        logical_drive_info = {'size_gb': 'MAX',
                              'raid_level': '1',
                              'controller': 'Smart Array P822 in Slot 2',
                              'physical_disks': ['5I:1:1',
                                                 '5I:1:2',
                                                 '5I:1:3']}

        controller.create_logical_drive(logical_drive_info)
        execute_mock.assert_called_once_with("create",
                                             "type=logicaldrive",
                                             "drives=5I:1:1,5I:1:2,5I:1:3",
                                             "raid=1", process_input='y')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_logical_drive_with_raid_array(self, execute_mock,
                                                  get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        logical_drive_info = {'size_gb': 50,
                              'raid_level': '1',
                              'volume_name': 'boot_volume',
                              'is_boot_volume': 'true',
                              'controller': 'Smart Array P822 in Slot 2',
                              'array': 'A'}

        controller.create_logical_drive(logical_drive_info)
        execute_mock.assert_called_once_with("array", "A",
                                             "create",
                                             "type=logicaldrive",
                                             "raid=1",
                                             "size=51200", process_input='y')

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_create_logical_drive_raid_level_mapping(self, execute_mock,
                                                     get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_NO_DRIVES

        server = objects.Server()
        controller = server.controllers[0]

        logical_drive_info = {'size_gb': 50,
                              'raid_level': '5+0',
                              'volume_name': 'boot_volume',
                              'is_boot_volume': 'true',
                              'controller': 'Smart Array P822 in Slot 2',
                              'physical_disks': ['5I:1:1',
                                                 '5I:1:2',
                                                 '5I:1:3',
                                                 '5I:1:4',
                                                 '5I:1:5',
                                                 '6I:1:6']}

        controller.create_logical_drive(logical_drive_info)
        execute_mock.assert_called_once_with(
            "create", "type=logicaldrive",
            "drives=5I:1:1,5I:1:2,5I:1:3,5I:1:4,5I:1:5,6I:1:6",
            "raid=50", "size=51200", process_input='y')

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

        physical_drive = list(filter(lambda x: x.id == '5I:1:1',
                                     array.physical_drives))[0]
        self.assertEqual(physical_drive,
                         controller.get_physical_drive_by_id('5I:1:1'))

        physical_drive = list(filter(lambda x: x.id == '5I:1:3',
                                     controller.unassigned_physical_drives))[0]
        self.assertEqual(physical_drive,
                         controller.get_physical_drive_by_id('5I:1:3'))

        self.assertIsNone(controller.get_physical_drive_by_id('foo'))

    @mock.patch.object(objects.Controller, 'execute_cmd')
    def test_erase_devices(self, execute_mock,
                           get_all_details_mock):
        get_all_details_mock.return_value = raid_constants.SSA_ERASE_DRIVE
        server = objects.Server()
        controller = server.controllers[0]
        controller.erase_devices('1I:2:1')
        execute_mock.assert_called_once_with('pd 1I:2:1', 'modify', 'erase',
                                             'erasepattern=overwrite',
                                             'unrestricted=off',
                                             'forced')


@mock.patch.object(objects.Server, '_get_all_details')
class LogicalDriveTest(testtools.TestCase):

    def test_get_logical_drive_dict(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        logical_drive = server.controllers[0].raid_arrays[0].logical_drives[0]
        ret = logical_drive.get_logical_drive_dict()
        self.assertEqual(557, ret['size_gb'])
        self.assertEqual('1', ret['raid_level'])
        self.assertEqual('0x600508b1001c321c',
                         ret['root_device_hint']['wwn'])
        self.assertEqual('Smart Array P822 in Slot 2',
                         ret['controller'])
        self.assertEqual(sorted(['5I:1:1', '5I:1:2']),
                         sorted(ret['physical_disks']))
        self.assertEqual('01F42227PDVTF0BRH5T0MOAB64',
                         ret['volume_name'])

    def test___init__bad_size_logical_drive(self, get_all_details_mock):

        ret = raid_constants.HPSSA_BAD_SIZE_LOGICAL_DRIVE
        get_all_details_mock.return_value = ret
        ex = self.assertRaises(exception.HPSSAOperationError,
                               objects.Server)
        msg = ("unknown size '558.9foo' for logical disk '1' of RAID array "
               "'A' in controller 'Smart Array P822 in Slot 2'")
        self.assertIn(msg, str(ex))


@mock.patch.object(objects.Server, '_get_all_details')
class ArrayTest(testtools.TestCase):

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_okay(self, execute_mock,
                                 get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        execute_mock.return_value = (
            raid_constants.ARRAY_ACCOMODATE_LOGICAL_DISK, None)
        logical_disk = {'size_gb': 500, 'raid_level': '5'}
        server = objects.Server()
        ret_val = server.controllers[0].raid_arrays[0].can_accomodate(
            logical_disk)
        self.assertTrue(ret_val)

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_max_size_gb_okay(self, execute_mock,
                                             get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        execute_mock.return_value = (
            raid_constants.ARRAY_ACCOMODATE_LOGICAL_DISK, None)
        logical_disk = {'size_gb': 'MAX', 'raid_level': '5'}
        server = objects.Server()
        ret_val = server.controllers[0].raid_arrays[0].can_accomodate(
            logical_disk)
        self.assertTrue(ret_val)

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_not_enough_space(self, execute_mock,
                                             get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        execute_mock.return_value = (
            raid_constants.ARRAY_ACCOMODATE_LOGICAL_DISK, None)
        logical_disk = {'size_gb': 1500, 'raid_level': '5'}
        server = objects.Server()
        ret_val = server.controllers[0].raid_arrays[0].can_accomodate(
            logical_disk)
        self.assertFalse(ret_val)

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_invalid_raid_level(self, execute_mock,
                                               get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        exc = processutils.ProcessExecutionError(
            stdout=raid_constants.ARRAY_ACCOMODATE_LOGICAL_DISK_INVALID,
            stderr=None,
            exit_code=1)
        execute_mock.side_effect = exc
        logical_disk = {'size_gb': 1500, 'raid_level': '1'}
        server = objects.Server()
        ret_val = server.controllers[0].raid_arrays[0].can_accomodate(
            logical_disk)
        self.assertFalse(ret_val)

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_some_other_error(self, execute_mock,
                                             get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        exc = processutils.ProcessExecutionError(
            stdout=raid_constants.ARRAY_ACCOMODATE_LOGICAL_DISK_INVALID,
            stderr=None,
            exit_code=2)
        execute_mock.side_effect = exc
        logical_disk = {'size_gb': 1500, 'raid_level': '1'}
        server = objects.Server()
        self.assertRaises(
            exception.HPSSAOperationError,
            server.controllers[0].raid_arrays[0].can_accomodate,
            logical_disk)

    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_oserror(self, execute_mock,
                                    get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        get_all_details_mock.return_value = current_config
        execute_mock.side_effect = OSError
        logical_disk = {'size_gb': 1500, 'raid_level': '1'}
        server = objects.Server()
        self.assertRaises(
            exception.HPSSAOperationError,
            server.controllers[0].raid_arrays[0].can_accomodate,
            logical_disk)

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test_can_accomodate_map_raid_level(self, execute_mock, path_mock,
                                           get_all_details_mock):
        current_config = raid_constants.HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1
        path_mock.return_value = True
        execute_mock.return_value = ("", None)
        get_all_details_mock.return_value = current_config
        logical_disk = {'size_gb': 1500, 'raid_level': '5+0'}
        server = objects.Server()
        server.controllers[0].raid_arrays[0].can_accomodate(logical_disk)
        execute_mock.assert_called_once_with(
            "ssacli", "controller", "slot=2", "array", mock.ANY, "create",
            "type=logicaldrive", "raid=50", "size=?")


@mock.patch.object(objects.Server, '_get_all_details')
class PhysicalDriveTest(testtools.TestCase):

    def test___init__bad_size_logical_drive(self, get_all_details_mock):

        ret = raid_constants.HPSSA_BAD_SIZE_PHYSICAL_DRIVE
        get_all_details_mock.return_value = ret
        ex = self.assertRaises(exception.HPSSAOperationError,
                               objects.Server)
        msg = ("unknown size '500foo' for physical disk '5I:1:1' of "
               "controller 'Smart Array P822 in Slot 2'")
        self.assertIn(msg, str(ex))

    def test___init__physical_disk_size_mb(self, get_all_details_mock):

        ret = raid_constants.HPSSA_SMALL_SIZE_PHYSICAL_DRIVE
        get_all_details_mock.return_value = ret
        server = objects.Server()
        self.assertEqual(
            2, server.controllers[0].unassigned_physical_drives[0].size_gb)

    def test___init__physical_disk_ssd(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_DRIVES_SSD
        server = objects.Server()
        d = [x for x in server.controllers[0].unassigned_physical_drives]
        drives = sorted((x for x in d),
                        key=lambda x: x.get_physical_drive_dict()['id'])
        ret_sas = drives[0].get_physical_drive_dict()
        ret_sata = drives[1].get_physical_drive_dict()

        self.assertEqual(200, ret_sas['size_gb'])
        self.assertEqual('Smart Array P822 in Slot 2',
                         ret_sas['controller'])
        self.assertEqual('6I:1:7', ret_sas['id'])
        self.assertEqual('ssd', ret_sas['disk_type'])
        self.assertEqual('sas', ret_sas['interface_type'])
        self.assertEqual('HP      EF0600FARNA', ret_sas['model'])
        self.assertEqual('HPD6', ret_sas['firmware'])
        self.assertEqual('ready', ret_sas['status'])

        self.assertEqual('6I:1:8', ret_sata['id'])
        self.assertEqual('ssd', ret_sata['disk_type'])
        self.assertEqual('sata', ret_sata['interface_type'])

        self.assertEqual('OK', ret_sata['erase_status'])

    def test_get_physical_drive_dict_part_of_array(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        d = server.controllers[0].raid_arrays[0].physical_drives[0]
        d = [x for x in server.controllers[0].raid_arrays[0].physical_drives
             if x.id == '5I:1:1']
        ret = d[0].get_physical_drive_dict()
        self.assertEqual(500, ret['size_gb'])
        self.assertEqual('Smart Array P822 in Slot 2', ret['controller'])
        self.assertEqual('5I:1:1', ret['id'])
        self.assertEqual('hdd', ret['disk_type'])
        self.assertEqual('sas', ret['interface_type'])
        self.assertEqual('HP      EF0600FARNA', ret['model'])
        self.assertEqual('HPD6', ret['firmware'])
        self.assertEqual('active', ret['status'])
        self.assertEqual('OK', ret['erase_status'])

    def test_get_physical_drive_dict_unassigned(self, get_all_details_mock):

        get_all_details_mock.return_value = raid_constants.HPSSA_ONE_DRIVE
        server = objects.Server()
        d = server.controllers[0].unassigned_physical_drives[0]
        d = [x for x in server.controllers[0].unassigned_physical_drives
             if x.id == '5I:1:3']
        ret = d[0].get_physical_drive_dict()
        self.assertEqual('Smart Array P822 in Slot 2', ret['controller'])
        self.assertEqual(400, ret['size_gb'])
        self.assertEqual('5I:1:3', ret['id'])
        self.assertEqual('hdd', ret['disk_type'])
        self.assertEqual('sas', ret['interface_type'])
        self.assertEqual('HP      EF0600FARNA', ret['model'])
        self.assertEqual('HPD6', ret['firmware'])
        self.assertEqual('ready', ret['status'])
        self.assertEqual('OK', ret['erase_status'])


class PrivateMethodsTestCase(testtools.TestCase):

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test__ssacli(self, execute_mock, path_mock):
        execute_mock.return_value = ("stdout", "stderr")
        path_mock.return_value = True
        stdout, stderr = objects._ssacli("foo", "bar",
                                         check_exit_code=[0, 1, 2, 3])
        execute_mock.assert_called_once_with(
            "ssacli", "foo", "bar", check_exit_code=[0, 1, 2, 3])
        self.assertEqual("stdout", stdout)
        self.assertEqual("stderr", stderr)

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test__ssacli_raises_error(self, execute_mock, path_mock):
        path_mock.return_value = True
        execute_mock.side_effect = OSError
        self.assertRaises(exception.HPSSAOperationError,
                          objects._ssacli, "foo", "bar")

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test__ssacli_raises_error_no_transform(self, execute_mock, path_mock):
        path_mock.return_value = True
        execute_mock.side_effect = OSError
        self.assertRaises(OSError,
                          objects._ssacli, "foo", "bar",
                          dont_transform_to_hpssa_exception=True)
        execute_mock.assert_called_once_with("ssacli", "foo", "bar")

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test__ssacli_raises_error_no_controller(self, execute_mock, path_mock):
        path_mock.return_value = True
        value = ("Error: No controllers detected. Possible causes:"
                 " The driver for the installed controller(s) is not loaded."
                 " On LINUX, the scsi_generic (sg) driver module is not"
                 " loaded. See the README file for more details.")
        execute_mock.side_effect = processutils.ProcessExecutionError(
            value)
        ex = self.assertRaises(exception.HPSSAOperationError,
                               objects._ssacli, "foo", "bar")
        msg = ("SSA controller not found. Enable ssa controller"
               " to continue with the desired operation")
        self.assertIn(msg, str(ex))

    @mock.patch('os.path.exists')
    @mock.patch.object(processutils, 'execute')
    def test__hpssacli_exists(self, execute_mock, path_mock):
        execute_mock.return_value = ("stdout", "stderr")
        path_mock.return_value = False
        stdout, stderr = objects._ssacli("foo", "bar",
                                         check_exit_code=[0, 1, 2, 3])
        execute_mock.assert_called_once_with(
            "hpssacli", "foo", "bar", check_exit_code=[0, 1, 2, 3])
        self.assertEqual("stdout", stdout)
        self.assertEqual("stderr", stderr)
