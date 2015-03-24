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
import httplib
import json

import mock
import testtools

from proliantutils import exception
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.tests.ilo import ris_sample_outputs as ris_outputs


class IloRisTestCase(testtools.TestCase):

    def setUp(self):
        super(IloRisTestCase, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "admin", "Admin")

    @mock.patch.object(ribcl.RIBCLOperations, 'get_one_time_boot')
    def test_fallback_to_ribcl(self, boot_mock):
        self.client.get_one_time_boot()
        boot_mock.assert_called_once_with()

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

    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPSConnection')
    def test__rest_op_request_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.request.side_effect = RuntimeError("boom")
        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', {}, None)
        https_con_mock.assert_called_once_with(host='1.2.3.4', strict=True)
        self.assertIn("boom", str(exc))

    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPConnection')
    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPSConnection')
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

    @mock.patch.object(httplib, 'HTTPSConnection')
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
