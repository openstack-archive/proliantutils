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

import collections

import ddt
import json
import mock
import sushy
import testtools

from proliantutils import exception
from proliantutils.ilo import constants as ilo_cons
from proliantutils.redfish import main
from proliantutils.redfish import redfish
from proliantutils.redfish.resources.account_service import account
from proliantutils.redfish.resources.account_service import account_service
from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.manager import virtual_media
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import iscsi
from proliantutils.redfish.resources.system import memory
from proliantutils.redfish.resources.system import pci_device
from proliantutils.redfish.resources.system import smart_storage_config
from proliantutils.redfish.resources.system.storage import array_controller
from proliantutils.redfish.resources.system.storage \
    import common as common_storage
from proliantutils.redfish.resources.system import system as pro_sys
from sushy.resources.system import system


@ddt.ddt
class RedfishOperationsTestCase(testtools.TestCase):

    @mock.patch.object(main, 'HPESushy', autospec=True)
    def setUp(self, sushy_mock):
        super(RedfishOperationsTestCase, self).setUp()
        self.sushy = mock.MagicMock()
        self.sushy.get_system_collection_path.return_value = (
            '/redfish/v1/Systems')
        self.sushy.get_manager_collection_path.return_value = (
            '/redfish/v1/Managers')
        sushy_mock.return_value = self.sushy
        with open('proliantutils/tests/redfish/'
                  'json_samples/root.json', 'r') as f:
            self.sushy.json = json.loads(f.read())

        self.rf_client = redfish.RedfishOperations(
            '1.2.3.4', username='foo', password='bar')
        sushy_mock.assert_called_once_with(
            'https://1.2.3.4', 'foo', 'bar', '/redfish/v1/', False)

    @mock.patch.object(main, 'HPESushy', autospec=True)
    def test_sushy_init_fail(self, sushy_mock):
        sushy_mock.side_effect = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloConnectionError,
            'The Redfish controller at "https://1.2.3.4" has thrown error',
            redfish.RedfishOperations,
            '1.2.3.4', username='foo', password='bar')

    def test__get_sushy_system_fail(self):
        self.rf_client._sushy.get_system.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish System "apple" was not found.',
            self.rf_client._get_sushy_system, 'apple')

    def test__get_sushy_manager_fail(self):
        self.rf_client._sushy.get_manager.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish Manager "banana" was not found.',
            self.rf_client._get_sushy_manager, 'banana')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_product_name(self, get_system_mock):
        product_mock = mock.PropertyMock(return_value='ProLiant DL180 Gen10')
        type(get_system_mock.return_value).model = product_mock
        product_name = self.rf_client.get_product_name()
        self.assertEqual('ProLiant DL180 Gen10', product_name)

    def test_get_host_power_status(self):
        self.sushy.get_system().power_state = sushy.SYSTEM_POWER_STATE_ON
        power_state = self.rf_client.get_host_power_status()
        self.assertEqual('ON', power_state)

    def test_reset_server(self):
        self.rf_client.reset_server()
        self.sushy.get_system().reset_system.assert_called_once_with(
            sushy.RESET_FORCE_RESTART)

    def test_reset_server_invalid_value(self):
        self.sushy.get_system().reset_system.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to reset server.',
            self.rf_client.reset_server)

    @mock.patch.object(redfish.RedfishOperations, 'get_host_power_status')
    def test_set_host_power_no_change(self, get_host_power_status_mock):
        get_host_power_status_mock.return_value = 'ON'
        self.rf_client.set_host_power('ON')
        self.assertTrue(get_host_power_status_mock.called)
        self.assertFalse(self.sushy.get_system().reset_system.called)

    @mock.patch.object(redfish.RedfishOperations, 'get_host_power_status')
    def test_set_host_power_failure(self, get_host_power_status_mock):
        get_host_power_status_mock.return_value = 'OFF'
        self.sushy.get_system().reset_system.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to set power state of server to ON',
            self.rf_client.set_host_power, 'ON')

    def test_set_host_power_invalid_input(self):
        self.assertRaisesRegex(
            exception.InvalidInputError,
            'The parameter "target_value" value "Off" is invalid.',
            self.rf_client.set_host_power, 'Off')

    @mock.patch.object(redfish.RedfishOperations, 'get_host_power_status')
    def test_set_host_power_change(self, get_host_power_status_mock):
        get_host_power_status_mock.return_value = 'OFF'
        self.rf_client.set_host_power('ON')
        self.sushy.get_system().reset_system.assert_called_once_with(
            sushy.RESET_ON)

    def test_press_pwr_btn(self):
        self.rf_client.press_pwr_btn()
        self.sushy.get_system().push_power_button.assert_called_once_with(
            sys_cons.PUSH_POWER_BUTTON_PRESS)

    def test_press_pwr_btn_fail(self):
        self.sushy.get_system().push_power_button.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to press power button',
            self.rf_client.press_pwr_btn)

    def test_hold_pwr_btn(self):
        self.rf_client.hold_pwr_btn()
        self.sushy.get_system().push_power_button.assert_called_once_with(
            sys_cons.PUSH_POWER_BUTTON_PRESS_AND_HOLD)

    def test_hold_pwr_btn_fail(self):
        self.sushy.get_system().push_power_button.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to press and hold power button',
            self.rf_client.hold_pwr_btn)

    def test_get_one_time_boot_not_set(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.sushy.get_system().json = system_json['default']
        boot = self.rf_client.get_one_time_boot()
        self.assertEqual('Normal', boot)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_one_time_boot_set_cdrom(self, get_system_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn = mock.Mock()
        self.conn.get.return_value.json.return_value = system_json[
            'System_op_for_one_time_boot_cdrom']
        self.sys_inst = system.System(self.conn,
                                      '/redfish/v1/Systems/437XR1138R2',
                                      redfish_version='1.0.2')
        get_system_mock.return_value = self.sys_inst
        ret = self.rf_client.get_one_time_boot()
        self.assertEqual(ret, 'CDROM')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_pending_boot_mode(self, get_system_mock):
        for cons_val in redfish.BOOT_MODE_MAP.keys():
            (get_system_mock.return_value.bios_settings.
             pending_settings.boot_mode) = cons_val
            result = self.rf_client.get_pending_boot_mode()
            self.assertEqual(redfish.BOOT_MODE_MAP[cons_val], result)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_pending_boot_mode_fail(self, get_system_mock):
        bios_settings_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.bios_settings).pending_settings = (
            bios_settings_mock)
        self.assertRaisesRegex(
            exception.IloError,
            'The pending BIOS Settings was not found.',
            self.rf_client.get_pending_boot_mode)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_current_boot_mode(self, get_system_mock):
        for cons_val in redfish.BOOT_MODE_MAP.keys():
            get_system_mock.return_value.bios_settings.boot_mode = cons_val
            result = self.rf_client.get_current_boot_mode()
            self.assertEqual(redfish.BOOT_MODE_MAP[cons_val], result)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_current_boot_mode_fail(self, get_system_mock):
        bios_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value).bios_settings = bios_mock
        self.assertRaisesRegex(
            exception.IloError,
            'The current BIOS Settings was not found.',
            self.rf_client.get_current_boot_mode)

    def test_activate_license(self):
        self.rf_client.activate_license('testkey')
        (self.sushy.get_manager.return_value.set_license.
         assert_called_once_with('testkey'))

    def test_activate_license_fail(self):
        self.sushy.get_manager.return_value.set_license.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update the license',
            self.rf_client.activate_license, 'key')

    def _setup_virtual_media(self):
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/manager.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        manager_mock = manager.HPEManager(
            self.conn, '/redfish/v1/Managers/1',
            redfish_version='1.0.2')

        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())
        return manager_mock, vmedia_collection_json, vmedia_json

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_virtual_media(self, eject_mock, manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_inserted']]

        self.rf_client.eject_virtual_media('CDROM')

        eject_mock.assert_called_once_with()

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_virtual_media_invalid_device(self, eject_mock,
                                                manager_mock):
        self.assertRaisesRegex(
            exception.IloError,
            "Invalid device 'XXXXX'. Valid devices: FLOPPY or CDROM.",
            self.rf_client.eject_virtual_media,
            'XXXXX')

        self.assertFalse(eject_mock.called)
        self.assertFalse(manager_mock.called)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_virtual_media_not_inserted(self, eject_mock, manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['default']]

        self.rf_client.eject_virtual_media('CDROM')

        self.assertFalse(eject_mock.called)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_virtual_media_floppy(self, eject_mock, manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_floppy']]

        self.rf_client.eject_virtual_media('FLOPPY')

        self.assertFalse(eject_mock.called)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_virtual_media_fail(self, eject_mock, manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        eject_mock.side_effect = sushy.exceptions.SushyError
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_inserted']]

        msg = ("The Redfish controller failed to eject the virtual"
               " media device 'CDROM'.")
        self.assertRaisesRegex(exception.IloError, msg,
                               self.rf_client.eject_virtual_media,
                               'CDROM')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_virtual_media(self, insert_mock, eject_mock, manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['default']]
        url = 'http://1.2.3.4:5678/xyz.iso'

        self.rf_client.insert_virtual_media(url, 'CDROM')

        self.assertFalse(eject_mock.called)
        insert_mock.assert_called_once_with(url)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_virtual_media_floppy(self, insert_mock, eject_mock,
                                         manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_floppy']]
        url = 'http://1.2.3.4:5678/xyz.iso'

        self.rf_client.insert_virtual_media(url, 'FLOPPY')

        self.assertFalse(eject_mock.called)
        insert_mock.assert_called_once_with(url)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_virtual_media_inserted(self, insert_mock, eject_mock,
                                           manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_inserted']]
        url = 'http://1.2.3.4:5678/xyz.iso'

        self.rf_client.insert_virtual_media(url, 'CDROM')

        eject_mock.assert_called_once_with()
        insert_mock.assert_called_once_with(url)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_virtual_media_fail(self, insert_mock, eject_mock,
                                       manager_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        insert_mock.side_effect = sushy.exceptions.SushyError
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['vmedia_inserted']]
        url = 'http://1.2.3.4:5678/xyz.iso'
        msg = ("The Redfish controller failed to insert the media url "
               "%s in the virtual media device 'CDROM'.") % url

        self.assertRaisesRegex(exception.IloError, msg,
                               self.rf_client.insert_virtual_media,
                               url, 'CDROM')

    @mock.patch.object(virtual_media.VirtualMedia, 'set_vm_status')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_set_vm_status(self, manager_mock, set_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['default']]

        self.rf_client.set_vm_status(device='CDROM')

        set_mock.assert_called_once_with(True)

    @mock.patch.object(virtual_media.VirtualMedia, 'set_vm_status')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_set_vm_status_fail(self, manager_mock, set_mock):
        manager_mock.return_value, vmedia_collection_json, vmedia_json = (
            self._setup_virtual_media())
        set_mock.side_effect = sushy.exceptions.SushyError
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['default']]
        msg = ("The Redfish controller failed to set the virtual "
               "media status.")

        self.assertRaisesRegex(exception.IloError, msg,
                               self.rf_client.set_vm_status,
                               'CDROM')

    @mock.patch.object(virtual_media.VirtualMedia, 'set_vm_status')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_set_vm_status_not_supported_boot_option(self, manager_mock,
                                                     set_mock):
        msg = ("Virtual media boot option 'XXXX' is invalid.")
        self.assertRaisesRegex(exception.IloInvalidInputError, msg,
                               self.rf_client.set_vm_status,
                               device='CDROM', boot_option='XXXX')
        self.assertFalse(manager_mock.called)
        self.assertFalse(set_mock.called)

    @mock.patch.object(virtual_media.VirtualMedia, 'set_vm_status')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_set_vm_status_boot_option_connect(self, manager_mock, set_mock):
        self.rf_client.set_vm_status(device='CDROM', boot_option='CONNECT')
        self.assertFalse(manager_mock.called)
        self.assertFalse(set_mock.called)

    def test_update_firmware(self):
        self.rf_client.update_firmware('fw_file_url', 'ilo')
        (self.sushy.get_update_service.return_value.flash_firmware.
         assert_called_once_with(self.rf_client, 'fw_file_url'))

    def test_update_firmware_flash_firmware_fail(self):
        (self.sushy.get_update_service.return_value.
         flash_firmware.side_effect) = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update firmware',
            self.rf_client.update_firmware, 'fw_file_url', 'cpld')

    def test_update_firmware_get_update_service_fail(self):
        self.sushy.get_update_service.side_effect = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update firmware',
            self.rf_client.update_firmware, 'fw_file_url', 'cpld')

    @mock.patch.object(redfish.RedfishOperations, 'get_current_boot_mode')
    def test__is_boot_mode_uefi_uefi(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = (
            redfish.BOOT_MODE_MAP.get(sys_cons.BIOS_BOOT_MODE_UEFI))
        result = self.rf_client._is_boot_mode_uefi()
        self.assertTrue(result)

    @mock.patch.object(redfish.RedfishOperations, 'get_current_boot_mode')
    def test__is_boot_mode_uefi_bios(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = (
            redfish.BOOT_MODE_MAP.get(sys_cons.BIOS_BOOT_MODE_LEGACY_BIOS))
        result = self.rf_client._is_boot_mode_uefi()
        self.assertFalse(result)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_persistent_boot_device_uefi_cdrom(self, get_sushy_system_mock,
                                                   _uefi_boot_mode_mock):
        (get_sushy_system_mock.return_value.
         bios_settings.boot_settings.
         get_persistent_boot_device.return_value) = (sushy.
                                                     BOOT_SOURCE_TARGET_CD)
        _uefi_boot_mode_mock.return_value = True
        result = self.rf_client.get_persistent_boot_device()
        self.assertEqual(
            result,
            redfish.DEVICE_REDFISH_TO_COMMON.get(sushy.BOOT_SOURCE_TARGET_CD))

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_persistent_boot_device_bios(self, get_sushy_system_mock,
                                             _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        result = self.rf_client.get_persistent_boot_device()
        self.assertEqual(result, None)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_persistent_boot_device_cdrom_continuous(self,
                                                         get_system_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn = mock.Mock()
        self.conn.get.return_value.json.return_value = system_json[
            'System_op_for_cdrom_persistent_boot']
        self.sys_inst = system.System(self.conn,
                                      '/redfish/v1/Systems/437XR1138R2',
                                      redfish_version='1.0.2')
        get_system_mock.return_value = self.sys_inst
        ret = self.rf_client.get_persistent_boot_device()
        self.assertEqual(ret, 'CDROM')

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_persistent_boot_device_exp(self, get_system_mock,
                                            _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = True
        boot_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.bios_settings).boot_settings = (
            boot_mock)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller is unable to get persistent boot device.',
            self.rf_client.get_persistent_boot_device)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_set_pending_boot_mode(self, get_system_mock):
        self.rf_client.set_pending_boot_mode('uefi')
        (get_system_mock.return_value.
         bios_settings.pending_settings.set_pending_boot_mode.
         assert_called_once_with('uefi'))

    def test_set_pending_boot_mode_invalid_input(self):
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            'Invalid Boot mode: "test" specified',
            self.rf_client.set_pending_boot_mode, 'test')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_set_pending_boot_mode_fail(self, get_system_mock):
        (get_system_mock.return_value.bios_settings.
         pending_settings.set_pending_boot_mode.side_effect) = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to set pending boot mode.',
            self.rf_client.set_pending_boot_mode, 'uefi')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_update_persistent_boot(self, get_system_mock):
        self.rf_client.update_persistent_boot(['NETWORK'])
        (get_system_mock.return_value.update_persistent_boot.
         assert_called_once_with(['NETWORK'], mac=None, persistent=True))

    def test_update_persistent_boot_invalid_input(self):
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            ('Invalid input "test". Valid devices: NETWORK, '
             'HDD, ISCSI or CDROM.'),
            self.rf_client.update_persistent_boot, ['test'])

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_update_persistent_boot_fail(self, get_system_mock):
        get_system_mock.return_value.update_persistent_boot.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update persistent boot.',
            self.rf_client.update_persistent_boot,
            ['NETWORK'])

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_set_one_time_boot(self, get_system_mock):
        self.rf_client.set_one_time_boot('CDROM')
        (get_system_mock.return_value.update_persistent_boot.
         assert_called_once_with(['CDROM'], mac=None, persistent=False))

    def test_set_one_time_boot_invalid_input(self):
        self.assertRaisesRegex(
            exception.IloInvalidInputError,
            ('Invalid input "test". Valid devices: NETWORK, '
             'HDD, ISCSI or CDROM.'),
            self.rf_client.set_one_time_boot, 'test')

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_set_one_time_boot_fail(self, get_system_mock):
        get_system_mock.return_value.update_persistent_boot.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to set one time boot.',
            self.rf_client.set_one_time_boot,
            'CDROM')

    def _setup_reset_ilo_credential(self):
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        account_mock = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

        with open('proliantutils/tests/redfish/'
                  'json_samples/account_collection.json', 'r') as f:
            account_collection_json = json.loads(f.read())

        with open('proliantutils/tests/redfish/'
                  'json_samples/account.json', 'r') as f:
            account_json = json.loads(f.read())

        return account_mock, account_collection_json, account_json

    @mock.patch.object(main.HPESushy, 'get_account_service')
    def test_reset_ilo_credential(self, account_mock):
        account_mock.return_value, account_collection_json, account_json = (
            self._setup_reset_ilo_credential())
        self.conn.get.return_value.json.side_effect = [
            account_collection_json, account_json]

        self.rf_client.reset_ilo_credential('fake-password')
        (self.sushy.get_account_service.return_value.
         accounts.get_member_details.return_value.
         update_credentials.assert_called_once_with('fake-password'))

    @mock.patch.object(main.HPESushy, 'get_account_service')
    def test_reset_ilo_credential_fail(self, account_mock):
        account_mock.return_value, account_collection_json, account_json = (
            self._setup_reset_ilo_credential())
        self.conn.get.return_value.json.side_effect = [
            account_collection_json, account_json]

        (self.sushy.get_account_service.return_value.accounts.
         get_member_details.return_value.
         update_credentials.side_effect) = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update credentials',
            self.rf_client.reset_ilo_credential, 'fake-password')

    @mock.patch.object(account.HPEAccount, 'update_credentials')
    def test_reset_ilo_credential_get_account_service_fail(self, update_mock):
        account_service_not_found_error = sushy.exceptions.SushyError
        account_service_not_found_error.message = (
            'HPEAccountService not found!!')
        self.sushy.get_account_service.side_effect = (
            account_service_not_found_error)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update credentials for foo. '
            'Error HPEAccountService not found!!',
            self.rf_client.reset_ilo_credential, 'fake-password')
        self.assertFalse(update_mock.called)

    @mock.patch.object(main.HPESushy, 'get_account_service')
    def test_reset_ilo_credential_no_member(self, account_mock):
        (self.sushy.get_account_service.return_value.accounts.
         get_member_details.return_value) = None
        self.assertRaisesRegex(
            exception.IloError,
            'No account found with username: foo',
            self.rf_client.reset_ilo_credential, 'fake-password')

    @ddt.data((sys_cons.SUPPORTED_LEGACY_BIOS_ONLY,
               ilo_cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY),
              (sys_cons.SUPPORTED_UEFI_ONLY,
               ilo_cons.SUPPORTED_BOOT_MODE_UEFI_ONLY),
              (sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI,
               ilo_cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI))
    @ddt.unpack
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_supported_boot_mode(self, supported_boot,
                                     expected_boot_val,
                                     get_system_mock):
        type(get_system_mock.return_value).supported_boot_mode = (
            supported_boot)
        actual_val = self.rf_client.get_supported_boot_mode()
        self.assertEqual(expected_boot_val, actual_val)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_supported_boot_mode_error(self, get_system_mock):
        supported_boot_mode_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value).supported_boot_mode = (
            supported_boot_mode_mock)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to get the supported boot modes.',
            self.rf_client.get_supported_boot_mode)

    @mock.patch.object(common_storage, 'get_drive_rotational_speed_rpm')
    @mock.patch.object(common_storage, 'has_nvme_ssd')
    @mock.patch.object(common_storage, 'has_rotational')
    @mock.patch.object(common_storage, 'has_ssd')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_get_server_capabilities(self, get_manager_mock, get_system_mock,
                                     ssd_mock, rotational_mock,
                                     nvme_mock, speed_mock):
        type(get_system_mock.return_value.pci_devices).gpu_devices = (
            [mock.MagicMock(spec=pci_device.PCIDevice)])
        type(get_system_mock.return_value.bios_settings).sriov = (
            sys_cons.SRIOV_ENABLED)
        type(get_system_mock.return_value.bios_settings).cpu_vt = (
            sys_cons.CPUVT_ENABLED)
        type(get_system_mock.return_value.secure_boot).current_boot = (
            sys_cons.SECUREBOOT_CURRENT_BOOT_ENABLED)
        type(get_system_mock.return_value).rom_version = (
            'U31 v1.00 (03/11/2017)')
        type(get_manager_mock.return_value).firmware_version = 'iLO 5 v1.15'
        type(get_system_mock.return_value).model = 'ProLiant DL180 Gen10'
        nic_mock = mock.PropertyMock(return_value='1Gb')
        type(get_system_mock.return_value.pci_devices).max_nic_capacity = (
            nic_mock)
        tpm_mock = mock.PropertyMock(return_value=sys_cons.TPM_PRESENT_ENABLED)
        type(get_system_mock.return_value.bios_settings).tpm_state = (
            tpm_mock)
        type(get_system_mock.return_value).supported_boot_mode = (
            sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI)
        iscsi_mock = mock.MagicMock(spec=iscsi.ISCSISettings)
        iscsi_mock.is_iscsi_boot_supported = mock.MagicMock(return_value=True)
        type(get_system_mock.return_value.bios_settings).iscsi_settings = (
            iscsi_mock)
        type(get_system_mock.return_value.smart_storage.
             array_controllers).members_identities = [
            mock.MagicMock(array_controller.HPEArrayController)]
        MemoryData = collections.namedtuple(
            'MemoryData', ['has_persistent_memory', 'has_nvdimm_n',
                           'has_logical_nvdimm_n'])
        mem = MemoryData(has_persistent_memory=True,
                         has_nvdimm_n=True,
                         has_logical_nvdimm_n=False)
        memory_mock = mock.MagicMock(spec=memory.MemoryCollection)
        memory_mock.details = mock.MagicMock(return_value=mem)
        get_system_mock.return_value.memory = memory_mock
        ssd_mock.return_value = True
        rotational_mock.return_value = True
        nvme_mock.return_value = True
        raid_mock = mock.PropertyMock(return_value=set(['0', '1']))
        type(get_system_mock.return_value.
             smart_storage).logical_raid_levels = (raid_mock)
        speed_mock.return_value = set(['10000', '15000'])
        actual = self.rf_client.get_server_capabilities()
        expected = {'pci_gpu_devices': 1, 'sriov_enabled': 'true',
                    'secure_boot': 'true', 'cpu_vt': 'true',
                    'rom_firmware_version': 'U31 v1.00 (03/11/2017)',
                    'ilo_firmware_version': 'iLO 5 v1.15',
                    'nic_capacity': '1Gb',
                    'trusted_boot': 'true',
                    'server_model': 'ProLiant DL180 Gen10',
                    'boot_mode_bios': 'true',
                    'boot_mode_uefi': 'true', 'iscsi_boot': 'true',
                    'hardware_supports_raid': 'true',
                    'persistent_memory': 'true',
                    'nvdimm_n': 'true',
                    'logical_nvdimm_n': 'false',
                    'has_ssd': 'true',
                    'has_rotational': 'true',
                    'has_nvme_ssd': 'true',
                    'logical_raid_level_0': 'true',
                    'logical_raid_level_1': 'true',
                    'drive_rotational_10000_rpm': 'true',
                    'drive_rotational_15000_rpm': 'true'}
        self.assertEqual(expected, actual)

    @mock.patch.object(common_storage, 'get_drive_rotational_speed_rpm')
    @mock.patch.object(common_storage, 'has_nvme_ssd')
    @mock.patch.object(common_storage, 'has_rotational')
    @mock.patch.object(common_storage, 'has_ssd')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_manager')
    def test_get_server_capabilities_optional_capabilities_absent(
            self, get_manager_mock, get_system_mock, ssd_mock,
            rotational_mock, nvme_mock, speed_mock):
        type(get_system_mock.return_value.pci_devices).gpu_devices = (
            [mock.MagicMock(spec=pci_device.PCIDevice)])
        type(get_system_mock.return_value.bios_settings).sriov = (
            sys_cons.SRIOV_DISABLED)
        type(get_system_mock.return_value.bios_settings).cpu_vt = (
            sys_cons.CPUVT_DISABLED)
        type(get_system_mock.return_value.secure_boot).current_boot = (
            sys_cons.SECUREBOOT_CURRENT_BOOT_DISABLED)
        type(get_system_mock.return_value).rom_version = (
            'U31 v1.00 (03/11/2017)')
        type(get_manager_mock.return_value).firmware_version = 'iLO 5 v1.15'
        type(get_system_mock.return_value).model = 'ProLiant DL180 Gen10'
        nic_mock = mock.PropertyMock(return_value='1Gb')
        type(get_system_mock.return_value.pci_devices).max_nic_capacity = (
            nic_mock)
        type(get_system_mock.return_value.pci_devices).nic_capacity = (
            nic_mock)
        tpm_mock = mock.PropertyMock(return_value=sys_cons.TPM_NOT_PRESENT)
        type(get_system_mock.return_value.bios_settings).tpm_state = (
            tpm_mock)
        type(get_system_mock.return_value).supported_boot_mode = (
            sys_cons.SUPPORTED_UEFI_ONLY)
        iscsi_mock = mock.MagicMock(spec=iscsi.ISCSISettings)
        iscsi_mock.is_iscsi_boot_supported = mock.MagicMock(return_value=False)
        type(get_system_mock.return_value.bios_settings).iscsi_settings = (
            iscsi_mock)
        type(get_system_mock.return_value.smart_storage.
             array_controllers).members_identities = []
        MemoryData = collections.namedtuple(
            'MemoryData', ['has_persistent_memory', 'has_nvdimm_n',
                           'has_logical_nvdimm_n'])
        mem = MemoryData(has_persistent_memory=False,
                         has_nvdimm_n=False,
                         has_logical_nvdimm_n=False)
        memory_mock = mock.MagicMock(spec=memory.MemoryCollection)
        get_system_mock.return_value.memory = memory_mock
        memory_mock.details = mock.MagicMock(return_value=mem)
        ssd_mock.return_value = False
        rotational_mock.return_value = False
        nvme_mock.return_value = False
        raid_mock = mock.PropertyMock(return_value=set())
        type(get_system_mock.return_value.
             smart_storage).logical_raid_levels = (raid_mock)
        speed_mock.return_value = set()
        actual = self.rf_client.get_server_capabilities()
        expected = {'pci_gpu_devices': 1,
                    'rom_firmware_version': 'U31 v1.00 (03/11/2017)',
                    'ilo_firmware_version': 'iLO 5 v1.15',
                    'nic_capacity': '1Gb',
                    'server_model': 'ProLiant DL180 Gen10',
                    'boot_mode_bios': 'false', 'boot_mode_uefi': 'true'}
        self.assertEqual(expected, actual)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_server_capabilities_gpu_fail(self, get_system_mock):
        gpu_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.pci_devices).gpu_devices = (
            gpu_mock)
        self.assertRaises(exception.IloError,
                          self.rf_client.get_server_capabilities)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    @mock.patch.object(bios.BIOSPendingSettings, 'update_bios_data_by_post')
    def test_reset_bios_to_default(self, update_bios_mock, get_system_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            bios_default_json = json.loads(f.read())
        self.conn = mock.Mock()
        self.conn.get.return_value.json.side_effect = [
            system_json['default'], bios_json['Default'],
            bios_json['BIOS_pending_settings_default'], bios_default_json]
        self.sys_inst = pro_sys.HPESystem(self.conn,
                                          '/redfish/v1/Systems/437XR1138R2',
                                          redfish_version='1.0.2')
        get_system_mock.return_value = self.sys_inst
        data = bios_default_json['BaseConfigs'][0]['default']
        self.rf_client.reset_bios_to_default()
        update_bios_mock.assert_called_once_with(data)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_reset_bios_to_default_fail(self, get_system_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            bios_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios_base_configs.json', 'r') as f:
            bios_default_json = json.loads(f.read())
        self.conn = mock.Mock()
        self.conn.get.return_value.json.side_effect = [
            system_json['default'], bios_json['Default'],
            bios_json['BIOS_pending_settings_default'], bios_default_json]
        (get_system_mock.return_value.bios_settings.
         update_bios_to_default.side_effect) = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloError,
            "The Redfish controller is unable to update bios settings"
            " to default", self.rf_client.reset_bios_to_default)

    @mock.patch.object(redfish.LOG, 'debug', autospec=True)
    def test_get_secure_boot_mode(self, log_debug_mock):
        sushy_system_mock = self.sushy.get_system.return_value
        type(sushy_system_mock.secure_boot).current_boot = mock.PropertyMock(
            return_value=sys_cons.SECUREBOOT_CURRENT_BOOT_ENABLED)
        self.rf_client.get_secure_boot_mode()
        log_debug_mock.assert_called_once_with(
            '[iLO 1.2.3.4] Secure boot is Enabled')

        log_debug_mock.reset_mock()
        type(sushy_system_mock.secure_boot).current_boot = mock.PropertyMock(
            return_value=sys_cons.SECUREBOOT_CURRENT_BOOT_DISABLED)
        self.rf_client.get_secure_boot_mode()
        log_debug_mock.assert_called_once_with(
            '[iLO 1.2.3.4] Secure boot is Disabled')

    def test_get_secure_boot_mode_on_fail(self):
        sushy_system_mock = self.sushy.get_system.return_value
        type(sushy_system_mock).secure_boot = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloCommandNotSupportedError,
            'The Redfish controller failed to provide '
            'information about secure boot on the server.',
            self.rf_client.get_secure_boot_mode)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_set_secure_boot_mode(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        self.rf_client.set_secure_boot_mode(True)
        secure_boot_mock = self.sushy.get_system.return_value.secure_boot
        secure_boot_mock.enable_secure_boot.assert_called_once_with(True)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_set_secure_boot_mode_in_bios(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = False
        self.assertRaisesRegex(
            exception.IloCommandNotSupportedInBiosError,
            'System is not in UEFI boot mode. "SecureBoot" related resources '
            'cannot be changed.',
            self.rf_client.set_secure_boot_mode, True)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_set_secure_boot_mode_on_fail(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        secure_boot_mock = self.sushy.get_system.return_value.secure_boot
        secure_boot_mock.enable_secure_boot.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to set secure boot settings '
            'on the server.',
            self.rf_client.set_secure_boot_mode, True)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_set_secure_boot_mode_for_invalid_value(
            self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        secure_boot_mock = self.sushy.get_system.return_value.secure_boot
        secure_boot_mock.enable_secure_boot.side_effect = (
            exception.InvalidInputError('Invalid input'))
        self.assertRaises(
            exception.IloError,
            self.rf_client.set_secure_boot_mode, 'some-non-boolean')

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_reset_secure_boot_keys(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        self.rf_client.reset_secure_boot_keys()
        sushy_system_mock = self.sushy.get_system.return_value
        sushy_system_mock.secure_boot.reset_keys.assert_called_once_with(
            sys_cons.SECUREBOOT_RESET_KEYS_DEFAULT)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_reset_secure_boot_keys_in_bios(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = False
        self.assertRaisesRegex(
            exception.IloCommandNotSupportedInBiosError,
            'System is not in UEFI boot mode. "SecureBoot" related resources '
            'cannot be changed.',
            self.rf_client.reset_secure_boot_keys)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_reset_secure_boot_keys_on_fail(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        sushy_system_mock = self.sushy.get_system.return_value
        sushy_system_mock.secure_boot.reset_keys.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to reset secure boot keys '
            'on the server.',
            self.rf_client.reset_secure_boot_keys)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_clear_secure_boot_keys(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        self.rf_client.clear_secure_boot_keys()
        sushy_system_mock = self.sushy.get_system.return_value
        sushy_system_mock.secure_boot.reset_keys.assert_called_once_with(
            sys_cons.SECUREBOOT_RESET_KEYS_DELETE_ALL)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_clear_secure_boot_keys_in_bios(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = False
        self.assertRaisesRegex(
            exception.IloCommandNotSupportedInBiosError,
            'System is not in UEFI boot mode. "SecureBoot" related resources '
            'cannot be changed.',
            self.rf_client.clear_secure_boot_keys)

    @mock.patch.object(redfish.RedfishOperations, '_is_boot_mode_uefi',
                       autospec=True)
    def test_clear_secure_boot_keys_on_fail(self, _is_boot_mode_uefi_mock):
        _is_boot_mode_uefi_mock.return_value = True
        sushy_system_mock = self.sushy.get_system.return_value
        sushy_system_mock.secure_boot.reset_keys.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to clear secure boot keys '
            'on the server.',
            self.rf_client.clear_secure_boot_keys)

    @mock.patch.object(common_storage, 'get_local_gb')
    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_essential_properties(self, get_system_mock, local_gb_mock):
        memory_mock = mock.PropertyMock(return_value=20)
        type(get_system_mock.return_value.memory_summary).size_gib = (
            memory_mock)
        count_mock = mock.PropertyMock(return_value=40)
        type(get_system_mock.return_value.processors.summary).count = (
            count_mock)
        arch_mock = mock.PropertyMock(return_value='x86 or x86-64')
        type(get_system_mock.return_value.processors.summary).architecture = (
            arch_mock)
        type(get_system_mock.return_value.ethernet_interfaces).summary = (
            {'1': '12:44:6A:3B:04:11'})

        local_gb_mock.return_value = 600
        actual = self.rf_client.get_essential_properties()
        expected = {'properties': {'cpus': 40,
                                   'cpu_arch': 'x86',
                                   'memory_mb': 20480,
                                   'local_gb': 600},
                    'macs': {'1': '12:44:6A:3B:04:11'}}
        self.assertEqual(expected, actual)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_essential_properties_fail(self, get_system_mock):
        memory_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.memory_summary).size_gib = (
            memory_mock)
        self.assertRaisesRegex(
            exception.IloError,
            "The Redfish controller failed to get the "
            "resource data. Error None",
            self.rf_client.get_essential_properties)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_delete_raid_configuration(self, get_system_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        controllers = (
            get_system_mock.return_value.smart_storage_config_controllers.
            return_value) = (system_json['System_oem_specific_configs']['Oem']
                             ['Hpe']['SmartStorageConfig'])
        self.rf_client.delete_raid_configuration()
        for value in controllers:
            (get_system_mock.return_value.get_smart_storage_config.
             assert_called_once_with(value))
            (get_system_mock.return_value.get_smart_storage_config().
             delete_raid.assert_called_once_with())

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_delete_raid_configuration_allcontrollers(self, get_system_mock):
        self.rf_client.delete_raid_configuration()
        (get_system_mock.return_value.smart_storage_config_controllers.
         assert_called_once_with())

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_delete_raid_configuration_fail(self, get_system_mock):
        (get_system_mock.return_value.smart_storage_config_controllers.
         side_effect) = sushy.exceptions.SushyError
        self.assertRaisesRegex(
            exception.IloError,
            "The Redfish controller failed to delete the "
            "raid configuration",
            self.rf_client.delete_raid_configuration)
