# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

"""Test class for RIS Module."""

import base64
import json

import mock
from six.moves import http_client
import testtools

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ris
from proliantutils.tests.ilo import ris_sample_outputs as ris_outputs


class IloRisTestCase(testtools.TestCase):

    def setUp(self):
        super(IloRisTestCase, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "Administrator", "Admin")

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_get_http_boot_url_uefi(self, _validate_uefi_boot_mode_mock,
                                    get_bios_settings_mock):
        get_bios_settings_mock.return_value = ris_outputs.HTTP_BOOT_URL
        _validate_uefi_boot_mode_mock.return_value = True
        result = self.client.get_http_boot_url()
        _validate_uefi_boot_mode_mock.assert_called_once_with()
        self.assertEqual(
            'http://10.10.1.30:8081/startup.nsh', result['UefiShellStartupUrl']
            )

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_set_http_boot_url_uefi(self, _validate_uefi_boot_mode_mock,
                                    change_bios_setting_mock):
        _validate_uefi_boot_mode_mock.return_value = True
        self.client.set_http_boot_url('http://10.10.1.30:8081/startup.nsh')
        _validate_uefi_boot_mode_mock.assert_called_once_with()
        change_bios_setting_mock.assert_called_once_with({
            "UefiShellStartupUrl": "http://10.10.1.30:8081/startup.nsh"
            })

    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_get_http_boot_url_bios(self, _validate_uefi_boot_mode_mock):
        _validate_uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.get_http_boot_url)

    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_set_http_boot_url_bios(self, _validate_uefi_boot_mode_mock):
        _validate_uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.set_http_boot_url,
                          'http://10.10.1.30:8081/startup.nsh')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode(self, get_details_mock, rest_get_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        uri = ris_outputs.REST_GET_SECURE_BOOT['links']['self']['href']
        rest_get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                      ris_outputs.REST_GET_SECURE_BOOT)
        result = self.client.get_secure_boot_mode()
        self.assertFalse(result)
        get_details_mock.assert_called_once_with()
        rest_get_mock.assert_called_once_with(uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode_fail(self, get_details_mock, rest_get_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        uri = ris_outputs.REST_GET_SECURE_BOOT['links']['self']['href']
        rest_get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                      ris_outputs.REST_FAILURE_OUTPUT)
        exc = self.assertRaises(exception.IloError,
                                self.client.get_secure_boot_mode)
        get_details_mock.assert_called_once_with()
        rest_get_mock.assert_called_once_with(uri)
        self.assertIn('FakeFailureMessage', str(exc))

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode_not_supported(self, get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        del host_response['Oem']['Hp']['links']['SecureBoot']
        get_details_mock.return_value = host_response
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client.get_secure_boot_mode)
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_host_power_status_ok(self, get_details_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        result = self.client.get_host_power_status()
        self.assertEqual(result, 'OFF')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(common, 'wait_for_ilo_after_reset')
    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_ok(self, get_mock, post_mock, status_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 manager_data)
        post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_POST_RESPONSE)
        self.client.reset_ilo()
        get_mock.assert_called_once_with(uri)
        post_mock.assert_called_once_with(uri, None, {'Action': 'Reset'})
        status_mock.assert_called_once_with(self.client)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_fail(self, get_mock, post_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.HEADERS_FOR_REST_OP,
                                 manager_data)
        post_mock.return_value = (301, ris_outputs.HEADERS_FOR_REST_OP,
                                  ris_outputs.REST_FAILURE_OUTPUT)
        exc = self.assertRaises(exception.IloError, self.client.reset_ilo)

        get_mock.assert_called_once_with(uri)
        post_mock.assert_called_once_with(uri, None, {'Action': 'Reset'})
        self.assertIn('FakeFailureMessage', str(exc))

    @mock.patch.object(ris.RISOperations, '_get_type')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_type_mismatch(self, get_mock, type_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.HEADERS_FOR_REST_OP,
                                 manager_data)
        type_mock.return_value = 'Manager.x'
        self.assertRaises(exception.IloError, self.client.reset_ilo)
        get_mock.assert_called_once_with(uri)

    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_reset_secure_boot_keys(self, change_mock):
        self.client.reset_secure_boot_keys()
        change_mock.assert_called_once_with('ResetToDefaultKeys', True)

    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_clear_secure_boot_keys(self, change_mock):
        self.client.clear_secure_boot_keys()
        change_mock.assert_called_once_with('ResetAllKeys', True)

    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_set_secure_boot_mode(self, change_mock):
        self.client.set_secure_boot_mode(True)
        change_mock.assert_called_once_with('SecureBootEnable', True)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_product_name(self, get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_response
        result = self.client.get_product_name()
        self.assertEqual(result, 'ProLiant BL460c Gen9')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test_get_current_boot_mode(self, bios_mock):
        bios_mock.return_value = 'LegacyBios'
        result = self.client.get_current_boot_mode()
        self.assertEqual(result, 'LEGACY')

    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test_get_pending_boot_mode(self, check_mock, bios_mock):
        check_mock.return_value = ('fake', 'fake',
                                   json.loads(ris_outputs.GET_BIOS_SETTINGS))
        bios_mock.return_value = ('fake', 'fake',
                                  json.loads(ris_outputs.GET_BIOS_SETTINGS))
        result = self.client.get_pending_boot_mode()
        self.assertEqual(result, 'UEFI')

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    def test_set_pending_boot_mode_legacy(self, change_mock):
        self.client.set_pending_boot_mode('legacy')
        change_mock.assert_called_once_with({'BootMode': 'LegacyBios'})

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    def test_set_pending_boot_mode_uefi(self, change_mock):
        self.client.set_pending_boot_mode('uefi')
        expected_properties = {'BootMode': 'uefi',
                               'UefiOptimizedBoot': 'Enabled'}
        change_mock.assert_called_once_with(expected_properties)

    def test_set_pending_boot_mode_invalid_mode(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client.set_pending_boot_mode, 'invalid')

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential(self, collection_mock, patch_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.reset_ilo_credential('fake-password')
        patch_mock.assert_called_once_with(uri, None,
                                           {'Password': 'fake-password'})

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential_fail(self, collection_mock, patch_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client.reset_ilo_credential,
                          'fake-password')
        patch_mock.assert_called_once_with(uri, None,
                                           {'Password': 'fake-password'})

    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential_no_account(self, collection_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        self.client = ris.RISOperations("1.2.3.4", "Admin", "Admin")
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        self.assertRaises(exception.IloError,
                          self.client.reset_ilo_credential,
                          'fake-password')

    @mock.patch.object(ris.RISOperations, '_validate_if_patch_supported')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_bios_hash_password')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_operation_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test_reset_bios_to_default(self, check_mock, bios_mock, op_mock,
                                   get_mock, passwd_mock, patch_mock,
                                   validate_mock):
        settings_uri = '/rest/v1/systems/1/bios/Settings'
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        base_config = json.loads(ris_outputs.GET_BASE_CONFIG)
        default_config = base_config['BaseConfigs'][0]['default']
        check_mock.return_value = (ris_outputs.GET_HEADERS, 'fake',
                                   json.loads(ris_outputs.GET_BIOS_SETTINGS))
        op_mock.return_value = False
        passwd_mock.return_value = {}
        get_mock.return_value = (200, 'fake', base_config)
        bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                  settings_uri, {})
        patch_mock.return_value = (200, 'fake', 'fake')
        self.client.reset_bios_to_default()
        check_mock.assert_called_once_with()
        bios_mock.assert_called_once_with(settings)
        op_mock.assert_called_once_with(ris_outputs.GET_HEADERS, 'PATCH')
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/BaseConfigs')
        passwd_mock.assert_called_once_with(None)
        patch_mock.assert_called_once_with(settings_uri, {}, default_config)
        validate_mock.assert_called_once_with(ris_outputs.GET_HEADERS,
                                              settings_uri)

    @mock.patch.object(ris.RISOperations, 'get_secure_boot_mode')
    @mock.patch.object(ris.RISOperations, '_get_ilo_firmware_version')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_server_capabilities(self, get_details_mock, ilo_firm_mock,
                                     secure_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        ilo_firm_mock.return_value = {'ilo_firmware_version': 'iLO 4 v2.20'}
        secure_mock.return_value = False
        expected_caps = {'secure_boot': 'true',
                         'ilo_firmware_version': 'iLO 4 v2.20',
                         'rom_firmware_version': u'I36 v1.40 (01/28/2015)',
                         'server_model': u'ProLiant BL460c Gen9'}
        capabilities = self.client.get_server_capabilities()
        self.assertEqual(expected_caps, capabilities)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test__get_ilo_firmware_version(self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client._get_ilo_firmware_version()
        expected_ilo_firm = {'ilo_firmware_version': 'iLO 4 v2.20'}
        self.assertIn('ilo_firmware_version', ilo_firm)
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license(self, get_ilo_details_mock, post_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        license_uri = "/rest/v1/Managers/1/LicenseService"
        get_ilo_details_mock.return_value = (ilo_details, uri)
        post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_POST_RESPONSE)
        self.client.activate_license('testkey')
        get_ilo_details_mock.assert_called_once_with()
        post_mock.assert_called_once_with(license_uri, None,
                                          {'LicenseKey': 'testkey'})

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license_IloError(self, get_ilo_details_mock, post_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        license_uri = "/rest/v1/Managers/1/LicenseService"
        get_ilo_details_mock.return_value = (ilo_details, uri)
        post_mock.return_value = (500, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError, self.client.activate_license,
                          'testkey')
        get_ilo_details_mock.assert_called_once_with()
        post_mock.assert_called_once_with(license_uri, None,
                                          {'LicenseKey': 'testkey'})

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license_IloCommandNotSupported(self,
                                                     get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        del ilo_details['Oem']['Hp']['links']['LicenseService']
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client.activate_license, 'testkey')
        get_ilo_details_mock.assert_called_once_with()


class TestRISOperationsPrivateMethods(testtools.TestCase):

    def setUp(self):
        super(TestRISOperationsPrivateMethods, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "admin", "Admin")

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__validate_uefi_boot_mode_uefi(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'UEFI'
        result = self.client._validate_uefi_boot_mode()
        self.assertTrue(result)

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__validate_uefi_boot_mode_bios(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'LEGACY'
        result = self.client._validate_uefi_boot_mode()
        self.assertFalse(result)

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_okay(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj

        sample_response_body = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        response_mock_obj.read.return_value = sample_response_body

        sample_headers = ris_outputs.HEADERS_FOR_REST_OP
        response_mock_obj.getheaders.return_value = sample_headers
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', None, None)

        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)

        https_con_mock.assert_called_once_with(host='1.2.3.4', strict=True)
        connection_mock_obj.request.assert_called_once_with(
            'GET', '/v1/foo',
            # base64 encoded username + password for admin/Admin
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            body="null")

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_request_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.request.side_effect = RuntimeError("boom")
        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', {}, None)
        https_con_mock.assert_called_once_with(host='1.2.3.4', strict=True)
        self.assertIn("boom", str(exc))

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_get_response_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.side_effect = RuntimeError("boom")
        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', None, None)
        https_con_mock.assert_called_once_with(host='1.2.3.4', strict=True)
        connection_mock_obj.request.assert_called_once_with(
            'GET', '/v1/foo',
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            body="null")
        self.assertIn("boom", str(exc))

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_response_read_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj
        response_mock_obj.read.side_effect = RuntimeError("boom")
        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', None, None)
        self.assertIn("boom", str(exc))

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_continous_redirection(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=301)
        https_con_mock.side_effect = [connection_mock_obj,
                                      connection_mock_obj,
                                      connection_mock_obj,
                                      connection_mock_obj,
                                      connection_mock_obj]

        connection_mock_obj.getresponse.return_value = response_mock_obj

        sample_response_body = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        response_mock_obj.read.return_value = sample_response_body

        sample_headers = ris_outputs.HEADERS_FOR_REST_OP
        sample_headers.append(('location', 'https://foo'))
        response_mock_obj.getheaders.return_value = sample_headers

        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', {}, None)
        self.assertEqual(5, https_con_mock.call_count)
        self.assertEqual(5, connection_mock_obj.request.call_count)
        self.assertIn('https://1.2.3.4/v1/foo', str(exc))

    @mock.patch.object(http_client, 'HTTPConnection')
    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_one_redirection(self, https_con_mock,
                                      http_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj1 = mock.MagicMock(status=301)
        response_mock_obj2 = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        http_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.side_effect = [response_mock_obj1,
                                                       response_mock_obj2]

        sample_response_body = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        response_mock_obj1.read.return_value = sample_response_body
        response_mock_obj2.read.return_value = sample_response_body

        sample_headers1 = ris_outputs.HEADERS_FOR_REST_OP
        sample_headers2 = ris_outputs.HEADERS_FOR_REST_OP
        sample_headers1.append(('location', 'http://5.6.7.8/v1/foo'))
        response_mock_obj1.getheaders.return_value = sample_headers1
        response_mock_obj2.getheaders.return_value = sample_headers2

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', {}, None)

        exp_headers = dict((x.lower(), y) for x, y in sample_headers1)
        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)

        https_con_mock.assert_any_call(host='1.2.3.4', strict=True)
        http_con_mock.assert_any_call(host='5.6.7.8', strict=True)
        self.assertEqual(2, connection_mock_obj.request.call_count)
        self.assertTrue(response_mock_obj1.read.called)
        self.assertTrue(response_mock_obj2.read.called)

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_response_decode_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj

        sample_response_body = "{[wrong json"
        response_mock_obj.read.return_value = sample_response_body

        sample_headers = ris_outputs.HEADERS_FOR_REST_OP
        response_mock_obj.getheaders.return_value = sample_headers

        self.assertRaises(exception.IloError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)
        https_con_mock.assert_called_once_with(host='1.2.3.4', strict=True)
        connection_mock_obj.request.assert_called_once_with(
            'GET', '/v1/foo',
            # base64 encoded username + password for admin/Admin
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            body="null")

    @mock.patch.object(http_client, 'HTTPSConnection')
    def test__rest_op_response_gzipped_response(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj

        sample_response_body = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        gzipped_response_body = base64.b64decode(
            ris_outputs.BASE64_GZIPPED_RESPONSE)
        response_mock_obj.read.return_value = gzipped_response_body

        sample_headers = ris_outputs.HEADERS_FOR_REST_OP
        response_mock_obj.getheaders.return_value = sample_headers
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', {}, None)

        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test___change_bios_setting(self, check_bios_mock, patch_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        properties = {'fake-property': 'fake-value'}
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client._change_bios_setting(properties)
        check_bios_mock.assert_called_once_with(properties.keys())
        patch_mock.assert_called_once_with(bios_uri, {}, properties)

    @mock.patch.object(ris.RISOperations, '_validate_if_patch_supported')
    @mock.patch.object(ris.RISOperations, '_operation_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test___change_bios_setting_fail(self, check_bios_mock, patch_mock,
                                        settings_mock, op_mock,
                                        validate_mock):
        bios_uri = '/rest/v1/systems/1/bios/Settings'
        properties = {'fake-property': 'fake-value'}
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        op_mock.return_value = False
        settings_mock.return_value = (ris_outputs.GET_HEADERS,
                                      bios_uri, settings)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client._change_bios_setting,
                          properties)
        check_bios_mock.assert_called_once_with(properties.keys())
        op_mock.assert_called_once_with(ris_outputs.GET_HEADERS, 'PATCH')
        settings_mock.assert_called_once_with(settings)
        patch_mock.assert_called_once_with(bios_uri, {}, properties)

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings(self, get_details_mock, patch_mock,
                                           get_bios_mock, change_bios_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        get_bios_mock.return_value = "test"
        secure_boot_uri = '/rest/v1/Systems/1/SecureBoot'
        bios_dict = {'CustomPostMessage': 'test '}
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client._change_secure_boot_settings('fake-property',
                                                 'fake-value')
        get_details_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(secure_boot_uri, None,
                                           {'fake-property': 'fake-value'})
        get_bios_mock.assert_called_once_with('CustomPostMessage')
        change_bios_mock.assert_called_once_with(bios_dict)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings_not_supported(self,
                                                         get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        del host_response['Oem']['Hp']['links']['SecureBoot']
        get_details_mock.return_value = host_response
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._change_secure_boot_settings,
                          'fake-property', 'fake-value')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings_fail(self, get_details_mock,
                                                patch_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        secure_boot_uri = '/rest/v1/Systems/1/SecureBoot'
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client._change_secure_boot_settings,
                          'fake-property', 'fake-value')
        get_details_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(secure_boot_uri, None,
                                           {'fake-property': 'fake-value'})

    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__get_bios_setting(self, bios_mock):
        bios_mock.return_value = ('fake', 'fake',
                                  json.loads(ris_outputs.GET_BIOS_SETTINGS))
        result = self.client._get_bios_setting('BootMode')
        bios_mock.assert_called_once_with(['BootMode'])
        self.assertEqual(result, 'Uefi')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 settings)
        self.client._get_bios_settings_resource(settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Settings')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource_key_error(self, get_mock):
        settings = json.loads(ris_outputs.GET_BASE_CONFIG)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_settings_resource,
                          settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource_fail(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        settings_uri = '/rest/v1/systems/1/bios/Settings'
        get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                 settings)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_settings_resource,
                          settings)
        get_mock.assert_called_once_with(settings_uri)
