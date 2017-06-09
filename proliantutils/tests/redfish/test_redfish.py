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
from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.manager import virtual_media
from proliantutils.redfish.resources.system import constants as sys_cons
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
