# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

import os
import shutil

import mock
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_utils import uuidutils
from pyremotevbox import vbox
import requests
from six.moves import builtins as __builtin__
import testtools

from proliantutils import exception
from proliantutils.ilo import vbox as ilo_vbox

CONF = cfg.CONF


@mock.patch.object(vbox, 'VirtualBoxHost', autospec=True)
class VirtualBoxOperationsTestCase(testtools.TestCase):

    def setUp(self):
        CONF.vbox_emulator.shared_root = "/path/to/share"
        CONF.vbox_emulator.host_share_location = "C:\\my_share_loc"
        super(VirtualBoxOperationsTestCase, self).setUp()

    def test_init_missing_host_share_location(self, host_class_mock):
        CONF.vbox_emulator.host_share_location = None
        CONF.vbox_emulator.shared_root = "foo"

        self.assertRaises(
            exception.VirtualBoxEmulatorError,
            ilo_vbox.VirtualBoxOperations,
            "foo", "bar", "1", "2", "3")

    def test_init_missing_shared_root(self, host_class_mock):
        CONF.vbox_emulator.host_share_location = "foo"
        CONF.vbox_emulator.shared_root = None

        self.assertRaises(
            exception.VirtualBoxEmulatorError,
            ilo_vbox.VirtualBoxOperations,
            "foo", "bar", "1", "2", "3")

    def _setup_and_return_vm_mock(self, host_class_mock):
        host_object_mock = mock.MagicMock(spec=['find_vm'])
        vm_object_mock = mock.MagicMock(
            spec=['get_power_status', 'get_boot_device', 'stop', 'start',
                  'set_boot_device', 'attach_device', 'detach_device',
                  'get_attached_device', 'get_firmware_type',
                  'set_firmware_type'])
        host_class_mock.return_value = host_object_mock
        host_object_mock.find_vm.return_value = vm_object_mock
        return host_object_mock, vm_object_mock

    def test_init(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)

        retval = ilo_vbox.VirtualBoxOperations("foo", "bar", "1", "2", "3")

        self.assertIsInstance(retval, ilo_vbox.VirtualBoxOperations)
        self.assertEqual(vm_object_mock, retval.vm)
        host_class_mock.assert_called_once_with()
        host_object_mock.find_vm.assert_called_once_with("foo")

    def test_get_all_licenses(self, host_class_mock):
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        self.assertEqual(
            'VirtualBox Advanced License',
            ilo_vbox_client.get_all_licenses())

    def _test_get_host_power_status_off(self, host_class_mock, retval,
                                        expected_val):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        vm_object_mock.get_power_status.return_value = retval
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        self.assertEqual(expected_val, ilo_vbox_client.get_host_power_status())

        vm_object_mock.get_power_status.assert_called_once_with()

    def test_get_host_power_status_off(self, host_class_mock):
        self._test_get_host_power_status_off(
            host_class_mock, retval=vbox.STATE_POWERED_OFF,
            expected_val='OFF')

    def test_get_host_power_status_on(self, host_class_mock):
        self._test_get_host_power_status_off(
            host_class_mock, retval=vbox.STATE_POWERED_ON,
            expected_val='ON')

    def test_get_host_power_status_error(self, host_class_mock):
        self._test_get_host_power_status_off(
            host_class_mock, retval=vbox.STATE_ERROR,
            expected_val='ERROR')

    def test_get_host_power_status_bad_value(self, host_class_mock):
        self._test_get_host_power_status_off(
            host_class_mock, retval='foo',
            expected_val='ERROR')

    def _test_get_one_time_boot(self, host_class_mock, retval,
                                expected_val):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        vm_object_mock.get_boot_device.return_value = retval
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        self.assertEqual(expected_val, ilo_vbox_client.get_one_time_boot())

        vm_object_mock.get_boot_device.assert_called_once_with()

    def test_get_one_time_boot_network(self, host_class_mock):
        self._test_get_one_time_boot(
            host_class_mock, retval=vbox.DEVICE_NETWORK,
            expected_val='NETWORK')

    def test_get_one_time_boot_cdrom(self, host_class_mock):
        self._test_get_one_time_boot(
            host_class_mock, retval=vbox.DEVICE_CDROM,
            expected_val='CDROM')

    def test_get_one_time_boot_disk(self, host_class_mock):
        self._test_get_one_time_boot(
            host_class_mock, retval=vbox.DEVICE_DISK,
            expected_val='HDD')

    def test_get_one_time_boot_floppy(self, host_class_mock):
        self._test_get_one_time_boot(
            host_class_mock, retval=vbox.DEVICE_FLOPPY,
            expected_val='FLOPPY')

    def test_reset_server(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.reset_server()

        vm_object_mock.stop.assert_called_once_with()
        vm_object_mock.start.assert_called_once_with()

    def test_press_pwr_btn(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.press_pwr_btn()

        vm_object_mock.stop.assert_called_once_with()

    def test_hold_pwr_btn(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.hold_pwr_btn()

        vm_object_mock.stop.assert_called_once_with()

    def test_set_host_power_on(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_host_power('ON')

        vm_object_mock.start.assert_called_once_with()

    def test_set_host_power_off(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_host_power('OFF')

        vm_object_mock.stop.assert_called_once_with()

    def _test_set_one_time_boot(self, host_class_mock, param, expected_val):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_one_time_boot(param)

        vm_object_mock.set_boot_device.assert_called_once_with(expected_val)

    def test_set_one_time_boot_network(self, host_class_mock):
        self._test_set_one_time_boot(
            host_class_mock, param='NETWORK',
            expected_val=vbox.DEVICE_NETWORK)

    def test_set_one_time_boot_cdrom(self, host_class_mock):
        self._test_set_one_time_boot(
            host_class_mock, param='CDROM',
            expected_val=vbox.DEVICE_CDROM)

    def test_set_one_time_boot_hdd(self, host_class_mock):
        self._test_set_one_time_boot(
            host_class_mock, param='HDD',
            expected_val=vbox.DEVICE_DISK)

    def test_set_one_time_boot_floppy(self, host_class_mock):
        self._test_set_one_time_boot(
            host_class_mock, param='FLOPPY',
            expected_val=vbox.DEVICE_DISK)

    @mock.patch.object(shutil, 'copyfileobj', autospec=True)
    @mock.patch.object(__builtin__, 'open', autospec=True)
    @mock.patch.object(uuidutils, 'generate_uuid', autospec=True)
    @mock.patch.object(requests, 'get', autospec=True)
    @mock.patch.object(
        ilo_vbox.VirtualBoxOperations, 'eject_virtual_media', autospec=True)
    def test_insert_virtual_media_cdrom(self, eject_mock, requests_get_mock,
                                        uuid_mock, open_mock, copy_mock,
                                        host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        requests_get_mock.return_value.raw = 'infile'
        uuid_mock.return_value = "filename"
        fileobj_mock = mock.MagicMock()
        mock_file_handle = mock.MagicMock()
        mock_file_handle.__enter__.return_value = fileobj_mock
        open_mock.return_value = mock_file_handle

        ilo_vbox_client.insert_virtual_media('http://loc', 'CDROM')

        eject_mock.assert_called_once_with(ilo_vbox_client, 'CDROM')
        expected_filename = "filename.iso"
        host_filename = '/path/to/share/' + expected_filename
        requests_get_mock.assert_called_once_with('http://loc',
                                                  stream=True)
        uuid_mock.assert_called_once_with()
        open_mock.assert_called_once_with(host_filename, 'w')
        copy_mock.assert_called_once_with('infile', fileobj_mock)
        vm_object_mock.attach_device.assert_called_once_with(
            vbox.DEVICE_CDROM, "C:\\my_share_loc\\" + expected_filename)

    @mock.patch.object(os, 'remove', autospec=True)
    @mock.patch.object(processutils, 'execute', autospec=True)
    @mock.patch.object(shutil, 'copyfileobj', autospec=True)
    @mock.patch.object(__builtin__, 'open', autospec=True)
    @mock.patch.object(uuidutils, 'generate_uuid', autospec=True)
    @mock.patch.object(requests, 'get', autospec=True)
    @mock.patch.object(
        ilo_vbox.VirtualBoxOperations, 'eject_virtual_media', autospec=True)
    def test_insert_virtual_media_floppy(self, eject_mock, requests_get_mock,
                                         uuid_mock, open_mock, copy_mock,
                                         execute_mock, remove_mock,
                                         host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        requests_get_mock.return_value.raw = 'infile'
        uuid_mock.return_value = "filename"
        fileobj_mock = mock.MagicMock()
        mock_file_handle = mock.MagicMock()
        mock_file_handle.__enter__.return_value = fileobj_mock
        open_mock.return_value = mock_file_handle

        ilo_vbox_client.insert_virtual_media('http://loc', 'FLOPPY')

        eject_mock.assert_called_once_with(ilo_vbox_client, 'FLOPPY')
        requests_get_mock.assert_called_once_with('http://loc',
                                                  stream=True)
        uuid_mock.assert_called_once_with()
        open_mock.assert_called_once_with('/path/to/share/filename.dsk', 'w')
        copy_mock.assert_called_once_with('infile', fileobj_mock)
        execute_mock.assert_called_once_with(
            "qemu-img", "convert", "-f", "raw", "-O", "vdi",
            '/path/to/share/filename.dsk', '/path/to/share/filename.vdi')
        remove_mock.assert_called_once_with('/path/to/share/filename.dsk')
        vm_object_mock.attach_device.assert_called_once_with(
            vbox.DEVICE_DISK, "C:\\my_share_loc\\filename.vdi")

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_host_power_status',
                       autospec=True)
    def test_eject_virtual_media_powered_on(self, power_mock, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        power_mock.return_value = 'ON'

        ilo_vbox_client.eject_virtual_media('FLOPPY')

        self.assertFalse(vm_object_mock.get_attached_device.called)

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_host_power_status',
                       autospec=True)
    def _test_eject_virtual_media(self, power_mock, remove_mock,
                                  host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        power_mock.return_value = 'OFF'
        vm_object_mock.get_attached_device.return_value = (
            "C:\\my_share_loc\\filename.iso")

        ilo_vbox_client.eject_virtual_media('FLOPPY')

        vm_object_mock.get_attached_device.assert_called_once_with(
            vbox.DEVICE_DISK)
        remove_mock.assert_called_once_with("/path/to/share/filename.iso")
        vm_object_mock.detach_device.assert_called_once_with(vbox.DEVICE_DISK)

    @mock.patch.object(os, 'remove', autospec=True)
    def test_eject_virtual_media(self, remove_mock, host_class_mock):
        self._test_eject_virtual_media(remove_mock=remove_mock,
                                       host_class_mock=host_class_mock)

    @mock.patch.object(os, 'remove', autospec=True)
    def test_eject_virtual_media_remove_exception(
            self, remove_mock, host_class_mock):
        remove_mock.side_effect = OSError
        self._test_eject_virtual_media(remove_mock=remove_mock,
                                       host_class_mock=host_class_mock)

    def _test_get_current_boot_mode(self, host_class_mock, retval,
                                    expected_val):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        vm_object_mock.get_firmware_type.return_value = retval
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        self.assertEqual(expected_val, ilo_vbox_client.get_current_boot_mode())

        vm_object_mock.get_firmware_type.assert_called_once_with()

    def test_get_current_boot_mode_bios(self, host_class_mock):
        self._test_get_current_boot_mode(
            host_class_mock, retval=vbox.FIRMWARE_BIOS,
            expected_val='LEGACY')

    def test_get_current_boot_mode_uefi(self, host_class_mock):
        self._test_get_current_boot_mode(
            host_class_mock, retval=vbox.FIRMWARE_EFI,
            expected_val='UEFI')

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_current_boot_mode',
                       autospec=True)
    def test_get_pending_boot_mode(self, current_boot_mode_mock,
                                   host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        current_boot_mode_mock.return_value = 'foo'
        self.assertEqual('foo', ilo_vbox_client.get_pending_boot_mode())
        current_boot_mode_mock.assert_called_once_with(mock.ANY)

    def test_get_supported_boot_mode(self, host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        self.assertEqual('LEGACY_UEFI',
                         ilo_vbox_client.get_supported_boot_mode())

    def _test_set_pending_boot_mode(
            self, host_class_mock, param, expected_val):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_pending_boot_mode(param)

        vm_object_mock.set_firmware_type.assert_called_once_with(expected_val)

    def test_set_pending_boot_mode_bios(self, host_class_mock):
        self._test_set_pending_boot_mode(
            host_class_mock, param='LEGACY',
            expected_val=vbox.FIRMWARE_BIOS)

    def test_set_pending_boot_mode_uefi(self, host_class_mock):
        self._test_set_pending_boot_mode(
            host_class_mock, param='UEFI',
            expected_val=vbox.FIRMWARE_EFI)

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_one_time_boot',
                       autospec=True)
    def test_get_persistent_boot(self, get_one_time_boot_mock,
                                 host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        get_one_time_boot_mock.return_value = 'foo'
        self.assertEqual('foo', ilo_vbox_client.get_persistent_boot())
        get_one_time_boot_mock.assert_called_once_with(mock.ANY)

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'set_one_time_boot',
                       autospec=True)
    def test_set_persistent_boot(self, set_one_time_boot_mock,
                                 host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_persistent_boot(['foo', 'bar'])

        set_one_time_boot_mock.assert_called_once_with(mock.ANY, 'foo')

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'set_one_time_boot',
                       autospec=True)
    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_host_power_status',
                       autospec=True)
    def test_set_persistent_boot_powered_off(self, get_host_power_status_mock,
                                             set_one_time_boot_mock,
                                             host_class_mock):
        get_host_power_status_mock.return_value = 'OFF'
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_persistent_boot(['foo', 'bar'])

        set_one_time_boot_mock.assert_called_once_with(mock.ANY, 'foo')

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'set_one_time_boot',
                       autospec=True)
    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'get_host_power_status',
                       autospec=True)
    def test_set_persistent_boot_powered_on(self, get_host_power_status_mock,
                                            set_one_time_boot_mock,
                                            host_class_mock):
        get_host_power_status_mock.return_value = 'ON'
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.set_persistent_boot(['foo', 'bar'])

        self.assertFalse(set_one_time_boot_mock.called)

    @mock.patch.object(ilo_vbox.VirtualBoxOperations, 'set_persistent_boot',
                       autospec=True)
    def test_update_persistent_boot(self, set_persistent_boot_mock,
                                    host_class_mock):
        host_object_mock, vm_object_mock = self._setup_and_return_vm_mock(
            host_class_mock)
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")

        ilo_vbox_client.update_persistent_boot(['foo', 'bar'])

        set_persistent_boot_mock.assert_called_once_with(
            mock.ANY, ['foo', 'bar'])

    def test_get_product_name(self, host_class_mock):
        ilo_vbox_client = ilo_vbox.VirtualBoxOperations(
            "foo", "bar", "1", "2", "3")
        self.assertEqual('VirtualBox VM', ilo_vbox_client.get_product_name())
