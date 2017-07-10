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
import sushy
import testtools

from proliantutils import exception
from proliantutils.redfish import main
from proliantutils.redfish import redfish
from proliantutils.redfish.resources.account_service import account
from proliantutils.redfish.resources.account_service import account_service
from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.manager import virtual_media
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import pci_device
from proliantutils.redfish.resources.system import system as pro_sys
from sushy.resources.system import system


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

    def test_get_product_name(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.sushy.get_system().json = system_json['default']
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

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_server_capabilities(self, get_system_mock):
        type(get_system_mock.return_value.pci_devices).gpu_devices = (
            [mock.MagicMock(spec=pci_device.PCIDevice)])
        type(get_system_mock.return_value.bios_settings).sriov = (
            sys_cons.SRIOV_ENABLED)
        nic_mock = mock.PropertyMock(return_value='1Gb')
        type(get_system_mock.return_value.pci_devices).max_nic_capacity = (
            nic_mock)
        actual = self.rf_client.get_server_capabilities()
        expected = {'pci_gpu_devices': 1,
                    'nic_capacity': '1Gb',
                    'sriov_enabled': 'true'}
        self.assertEqual(expected, actual)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_server_capabilities_gpu_fail(self, get_system_mock):
        gpu_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.pci_devices).gpu_devices = (
            gpu_mock)
        self.assertRaises(exception.IloError,
                          self.rf_client.get_server_capabilities)

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    @mock.patch.object(bios.BIOSPendingSettings, 'update_bios_data')
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

    @mock.patch.object(redfish.RedfishOperations, '_get_sushy_system')
    def test_get_server_capabilities_nic_fail(self, get_system_mock):
        nic_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(get_system_mock.return_value.pci_devices).max_nic_capacity = (
            nic_mock)
        self.assertRaises(exception.IloError,
                          self.rf_client.get_server_capabilities)
