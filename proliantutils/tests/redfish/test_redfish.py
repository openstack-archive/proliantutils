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
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.update_service import update_service
from sushy.resources.system import system


class RedfishOperationsTestCase(testtools.TestCase):

    @mock.patch.object(main, 'HPESushy', autospec=True)
    def setUp(self, sushy_mock):
        super(RedfishOperationsTestCase, self).setUp()
        self.sushy = mock.MagicMock()
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

    def test__get_system_collection_path(self):
        self.assertEqual('/redfish/v1/Systems/',
                         self.rf_client._get_system_collection_path())

    def test__get_system_collection_path_missing_systems_attr(self):
        self.rf_client._sushy.json.pop('Systems')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'The attribute Systems is missing',
            self.rf_client._get_system_collection_path)

    def test__get_sushy_system_fail(self):
        self.rf_client._sushy.get_system.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish System "apple" was not found.',
            self.rf_client._get_sushy_system, 'apple')

    def test_get_product_name(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.sushy.get_system().json = system_json['Default']
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
        self.sushy.get_system().json = system_json['Default']
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

    @mock.patch.object(redfish.RedfishOperations,
                       'get_firmware_update_progress', autospec=True)
    def test_update_firmware(self, get_firmware_update_progress_mock):
        # | GIVEN |
        (self.sushy.get_update_service.return_value.flash_firmware_update.
         return_value.status_code) = 200
        get_firmware_update_progress_mock.return_value = 'Complete', 100
        # | WHEN |
        self.rf_client.update_firmware('fw_file_url', 'ilo')
        # | THEN |
        (self.sushy.get_update_service.return_value.flash_firmware_update.
            assert_called_once_with({'ImageURI': 'fw_file_url'}))
        (self.sushy.get_update_service.return_value.
         wait_for_redfish_firmware_update_to_complete.
         assert_called_once_with(self.rf_client))
        get_firmware_update_progress_mock.assert_called_once_with(
            self.rf_client)

    def test_update_firmware_throws_if_flash_fwu_fail(self):
        (self.sushy.get_update_service.return_value.flash_firmware_update.
         return_value.status_code) = 500
        self.assertRaisesRegex(exception.IloError,
                               '500 invalid response code '
                               'received for fw update',
                               self.rf_client.update_firmware, 'fw_file_url',
                               'cpld')

    @mock.patch.object(redfish.RedfishOperations,
                       'get_firmware_update_progress', autospec=True)
    def test_update_firmware_throws_if_error_occurs_in_update(
            self, get_firmware_update_progress_mock):
        (self.sushy.get_update_service.return_value.flash_firmware_update.
         return_value.status_code) = 200
        get_firmware_update_progress_mock.return_value = 'Error', 0
        self.assertRaisesRegex(exception.IloError,
                               'Unable to update firmware',
                               self.rf_client.update_firmware, 'fw_file_url',
                               'cpld')

    @mock.patch.object(redfish.RedfishOperations, '_get_update_service')
    def test_get_firmware_update_progress(self, _get_update_service_mock):
        # GIVEN
        with open('proliantutils/tests/redfish/'
                  'json_samples/update_service.json', 'r') as f:
            conn_mock = mock.MagicMock()
            conn_mock.get.return_value.json.return_value = json.loads(f.read())
        update_service_inst = update_service.HPEUpdateService(
            conn_mock, '/redfish/v1/UpdateService', redfish_version='1.0.x')
        _get_update_service_mock.return_value = update_service_inst
        # WHEN
        state, percent = self.rf_client.get_firmware_update_progress()
        # THEN
        self.assertEqual(('Updating', 24), (state, percent))
