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
import time

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.redfish import main
from proliantutils.redfish import redfish
from proliantutils.redfish.resources import update_service
from sushy import auth


class HPEUpdateServiceTestCase(testtools.TestCase):

    @mock.patch.object(main, 'HPESushy', autospec=True)
    def setUp(self, sushy_mock):
        super(HPEUpdateServiceTestCase, self).setUp()
        self.conn = mock.MagicMock()
        self.sushy = mock.MagicMock()
        sushy_mock.return_value = self.sushy
        with open('proliantutils/tests/redfish/'
                  'json_samples/update_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.rf_client = redfish.RedfishOperations(
            '1.2.3.4', username='foo', password='bar')
        basic_auth = auth.BasicAuth(username='foo', password='bar')
        args, kwargs = sushy_mock.call_args
        self.assertEqual(('https://1.2.3.4',), args)
        self.assertFalse(kwargs.get('verify'))
        self.assertEqual('/redfish/v1/', kwargs.get('root_prefix'))
        self.assertTrue(isinstance(kwargs.get('auth'), auth.BasicAuth))
        self.us_inst = update_service.HPEUpdateService(
            self.conn, '/redfish/v1/UpdateService/1',
            redfish_version='1.0.2')

    def test__get_firmware_update_element(self):
        value = self.us_inst._get_firmware_update_element()
        expected_uri = ('/redfish/v1/UpdateService/Actions/'
                        'UpdateService.SimpleUpdate/')
        self.assertEqual(expected_uri, value.target_uri)

    def test__get_firmware_update_element_missing_url_action(self):
        self.us_inst._actions.update_firmware = None
        self.assertRaisesRegex(
            sushy.exceptions.MissingActionError,
            'action #UpdateService.SimpleUpdate',
            self.us_inst._get_firmware_update_element)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(update_service.HPEUpdateService,
                       'wait_for_redfish_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_flash_firmware(self,
                            wait_for_redfish_firmware_update_to_complete_mock,
                            get_firmware_update_progress_mock,
                            sleep_mock):
        # | GIVEN |
        target_uri = ('/redfish/v1/UpdateService/Actions/'
                      'UpdateService.SimpleUpdate/')
        get_firmware_update_progress_mock.return_value = 'Complete', None
        # | WHEN |
        self.us_inst.flash_firmware(self.rf_client, 'web_url')
        # | THEN |
        self.us_inst._conn.post.assert_called_once_with(
            target_uri, data={'ImageURI': 'web_url'})
        self.assertTrue(wait_for_redfish_firmware_update_to_complete_mock.
                        called)
        self.assertTrue(get_firmware_update_progress_mock.called)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_flash_firmware_post_fails(self, get_firmware_update_progress_mock,
                                       sleep_mock):
        get_firmware_update_progress_mock.return_value = 'Complete', None
        self.us_inst._conn.post.side_effect = (
            sushy.exceptions.SushyError)
        self.assertRaisesRegex(
            exception.IloError,
            'The Redfish controller failed to update firmware',
            self.us_inst.flash_firmware, self.rf_client, 'web_url')

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(update_service.HPEUpdateService,
                       'wait_for_redfish_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_flash_firmware_get_firmware_update_progress_throws_exception(
        self, wait_for_redfish_firmware_update_to_complete_mock,
            get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        self.us_inst._conn.post.return_value.status_code = 200
        get_firmware_update_progress_mock.side_effect = (
            sushy.exceptions.SushyError)
        # | WHEN & THEN|
        self.assertRaisesRegex(
            exception.IloError,
            'Failed to get firmware progress update',
            self.us_inst.flash_firmware, self.rf_client, 'web_url')

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(update_service.HPEUpdateService,
                       'wait_for_redfish_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_flash_firmware_get_firmware_update_progress_in_error_state(
        self, wait_for_redfish_firmware_update_to_complete_mock,
            get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        self.us_inst._conn.post.return_value.status_code = 200
        get_firmware_update_progress_mock.side_effect = [('Error', None)]
        # | WHEN & THEN|
        self.assertRaisesRegex(
            exception.IloError,
            'Unable to update firmware',
            self.us_inst.flash_firmware, self.rf_client, 'web_url')

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(update_service.HPEUpdateService,
                       'wait_for_redfish_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_flash_firmware_get_firmware_update_progress_in_unknown_state(
        self, wait_for_redfish_firmware_update_to_complete_mock,
            get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        target_uri = ('/redfish/v1/UpdateService/Actions/'
                      'UpdateService.SimpleUpdate/')
        get_firmware_update_progress_mock.return_value = 'Unknown', None
        # | WHEN |
        self.us_inst.flash_firmware(self.rf_client, 'web_url')
        # | THEN |
        self.us_inst._conn.post.assert_called_once_with(
            target_uri, data={'ImageURI': 'web_url'})
        self.assertTrue(wait_for_redfish_firmware_update_to_complete_mock.
                        called)
        self.assertTrue(get_firmware_update_progress_mock.called)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_redfish_firmware_update_to_complete_ok(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        get_firmware_update_progress_mock.side_effect = [('Updating', 25),
                                                         ('Complete', None)]
        # | WHEN |
        (self.us_inst.
         wait_for_redfish_firmware_update_to_complete(self.rf_client))
        # | THEN |
        self.assertEqual(2, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_redfish_firmware_update_to_complete_multiple_retries(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        get_firmware_update_progress_mock.side_effect = [('Idle', 0),
                                                         ('Updating', 25),
                                                         ('Updating', 50),
                                                         ('Updating', 75),
                                                         ('Error', 0)]
        # | WHEN |
        (self.us_inst.
         wait_for_redfish_firmware_update_to_complete(self.rf_client))
        # | THEN |
        self.assertEqual(5, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_redfish_firmware_update_to_complete_retry_on_exception(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        get_firmware_update_progress_mock.side_effect = [('Updating', 25),
                                                         exc,
                                                         ('Complete', None)]
        # | WHEN |
        (self.us_inst.
         wait_for_redfish_firmware_update_to_complete(self.rf_client))
        # | THEN |
        self.assertEqual(3, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_redfish_firmware_update_to_complete_very_quick_update(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        get_firmware_update_progress_mock.side_effect = [('Complete', None)]
        # | WHEN |
        (self.us_inst.
         wait_for_redfish_firmware_update_to_complete(self.rf_client))
        # | THEN |
        self.assertEqual(1, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(update_service.HPEUpdateService,
                       'get_firmware_update_progress', autospec=True)
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_redfish_firmware_update_to_complete_fail(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        get_firmware_update_progress_mock.side_effect = exc
        # | WHEN & THEN|
        self.assertRaises(exception.IloError,
                          (self.us_inst.
                           wait_for_redfish_firmware_update_to_complete),
                          self.rf_client)
        self.assertEqual(10, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(update_service.HPEUpdateService, 'refresh',
                       autospec=True)
    def test_get_firmware_update_progress(self, refresh_mock):
        refresh_mock.return_value.status_code = 200
        state, percent = self.us_inst.get_firmware_update_progress()
        self.assertEqual(('Updating', 24), (state, percent))

    @mock.patch.object(update_service.HPEUpdateService,
                       'refresh', autospec=True)
    def test_get_firmware_update_progress_refresh_exception(self,
                                                            refresh_mock):
        refresh_mock.side_effect = (sushy.exceptions.SushyError)
        state, percent = self.us_inst.get_firmware_update_progress()
        self.assertEqual(('Unknown', 'Unknown'), (state, percent))
