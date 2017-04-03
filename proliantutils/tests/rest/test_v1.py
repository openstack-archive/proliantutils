# Copyright 2017 Hewlett Packard Enterprise Development Company, L.P.
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

import base64
import json

import mock
import requests
from requests.packages import urllib3
from requests.packages.urllib3 import exceptions as urllib3_exceptions
import testtools

from proliantutils import exception
from proliantutils.rest import v1
from proliantutils.tests.rest import rest_sample_outputs as rest_outputs


class RestClientBaseInitAndLowdashTestCase(testtools.TestCase):

    @mock.patch.object(urllib3, 'disable_warnings')
    def test_init(self, disable_warning_mock):
        rest_client = v1.RestClientBase(
            "x.x.x.x", "admin", "Admin", bios_password='foo',
            cacert='/somepath')

        self.assertEqual(rest_client.host, "x.x.x.x")
        self.assertEqual(rest_client.login, "admin")
        self.assertEqual(rest_client.password, "Admin")
        self.assertEqual(rest_client.bios_password, "foo")
        self.assertEqual({}, rest_client.message_registries)
        self.assertEqual(rest_client.cacert, '/somepath')

    @mock.patch.object(urllib3, 'disable_warnings')
    def test_init_without_cacert(self, disable_warning_mock):
        rest_client = v1.RestClientBase(
            "x.x.x.x", "admin", "Admin", bios_password='foo')

        self.assertEqual(rest_client.host, "x.x.x.x")
        self.assertEqual(rest_client.login, "admin")
        self.assertEqual(rest_client.password, "Admin")
        self.assertIsNone(rest_client.cacert)
        disable_warning_mock.assert_called_once_with(
            urllib3_exceptions.InsecureRequestWarning)

    def test__okay(self):
        rest_client = v1.RestClientBase("1.2.3.4", "admin", "Admin")
        self.assertEqual('[iLO 1.2.3.4] foo', rest_client._('foo'))


class RestClientBaseTestCase(testtools.TestCase):

    def setUp(self):
        super(RestClientBaseTestCase, self).setUp()
        self.client = v1.RestClientBase("1.2.3.4", "admin", "Admin")

    @mock.patch.object(requests, 'get')
    def test__rest_op_okay(self, request_mock):
        sample_headers = rest_outputs.HEADERS_FOR_REST_OP
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)
        sample_response_body = rest_outputs.RESPONSE_BODY_FOR_REST_OP
        response_mock_obj = mock.MagicMock(
            status_code=200, text=sample_response_body,
            headers=exp_headers)
        request_mock.return_value = response_mock_obj

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', None, None)

        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)
        request_mock.assert_called_once_with(
            'https://1.2.3.4/v1/foo',
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            data="null", verify=False)

    @mock.patch.object(requests, 'get')
    def test__rest_op_request_error(self, request_mock):
        request_mock.side_effect = RuntimeError("boom")

        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', {}, None)

        request_mock.assert_called_once_with(
            'https://1.2.3.4/v1/foo',
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            data="null", verify=False)
        self.assertIn("boom", str(exc))

    @mock.patch.object(requests, 'get')
    def test__rest_op_continous_redirection(self, request_mock):
        sample_response_body = rest_outputs.RESPONSE_BODY_FOR_REST_OP
        sample_headers = rest_outputs.HEADERS_FOR_REST_OP
        sample_headers.append(('location', 'https://foo'))
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)
        response_mock_obj = mock.MagicMock(
            status_code=301, text=sample_response_body,
            headers=exp_headers)
        request_mock.side_effect = [response_mock_obj,
                                    response_mock_obj,
                                    response_mock_obj,
                                    response_mock_obj,
                                    response_mock_obj]

        exc = self.assertRaises(exception.IloConnectionError,
                                self.client._rest_op,
                                'GET', '/v1/foo', {}, None)

        self.assertEqual(5, request_mock.call_count)
        self.assertIn('https://1.2.3.4/v1/foo', str(exc))

    @mock.patch.object(requests, 'get')
    def test__rest_op_one_redirection(self, request_mock):
        sample_response_body = rest_outputs.RESPONSE_BODY_FOR_REST_OP
        sample_headers1 = rest_outputs.HEADERS_FOR_REST_OP
        sample_headers2 = rest_outputs.HEADERS_FOR_REST_OP
        sample_headers1.append(('location', 'https://5.6.7.8/v1/foo'))
        exp_headers1 = dict((x.lower(), y) for x, y in sample_headers1)
        exp_headers2 = dict((x.lower(), y) for x, y in sample_headers2)
        response_mock_obj1 = mock.MagicMock(
            status_code=301, text=sample_response_body,
            headers=exp_headers1)
        response_mock_obj2 = mock.MagicMock(
            status_code=200, text=sample_response_body,
            headers=exp_headers2)
        request_mock.side_effect = [response_mock_obj1,
                                    response_mock_obj2]

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', {}, None)

        exp_headers = dict((x.lower(), y) for x, y in sample_headers2)
        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)
        request_mock.assert_has_calls([
            mock.call('https://1.2.3.4/v1/foo',
                      headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
                      data="null", verify=False),
            mock.call('https://5.6.7.8/v1/foo',
                      headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
                      data="null", verify=False)])

    @mock.patch.object(requests, 'get')
    def test__rest_op_response_decode_error(self, request_mock):
        sample_response_body = "{[wrong json"
        sample_headers = rest_outputs.HEADERS_FOR_REST_OP
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)
        response_mock_obj = mock.MagicMock(
            status_code=200, text=sample_response_body,
            headers=exp_headers)
        request_mock.return_value = response_mock_obj

        self.assertRaises(exception.IloError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)

        request_mock.assert_called_once_with(
            'https://1.2.3.4/v1/foo',
            headers={'Authorization': 'BASIC YWRtaW46QWRtaW4='},
            data="null", verify=False)

    @mock.patch.object(requests, 'get')
    def test__rest_op_response_gzipped_response(self, request_mock):
        sample_response_body = rest_outputs.RESPONSE_BODY_FOR_REST_OP
        gzipped_response_body = base64.b64decode(
            rest_outputs.BASE64_GZIPPED_RESPONSE)
        sample_headers = rest_outputs.HEADERS_FOR_REST_OP
        exp_headers = dict((x.lower(), y) for x, y in sample_headers)
        response_mock_obj = mock.MagicMock(
            status_code=200, text=gzipped_response_body,
            headers=exp_headers)
        request_mock.return_value = response_mock_obj

        status, headers, response = self.client._rest_op(
            'GET', '/v1/foo', {}, None)

        self.assertEqual(200, status)
        self.assertEqual(exp_headers, headers)
        self.assertEqual(json.loads(sample_response_body), response)

    @mock.patch.object(v1.RestClientBase, '_rest_op')
    def test__rest_get(self, _rest_op_mock):
        self.client._rest_get('/v1/foo', {})
        _rest_op_mock.assert_called_once_with(
            'GET', '/v1/foo', {}, None)

    @mock.patch.object(v1.RestClientBase, '_rest_op')
    def test__rest_patch(self, _rest_op_mock):
        self.client._rest_patch('/v1/foo', {}, {'data': 'Lorem ipsum'})
        _rest_op_mock.assert_called_once_with(
            'PATCH', '/v1/foo', {}, {'data': 'Lorem ipsum'})

    @mock.patch.object(v1.RestClientBase, '_rest_op')
    def test__rest_put(self, _rest_op_mock):
        self.client._rest_put('/v1/foo', {}, {'data': 'Lorem ipsum'})
        _rest_op_mock.assert_called_once_with(
            'PUT', '/v1/foo', {}, {'data': 'Lorem ipsum'})

    @mock.patch.object(v1.RestClientBase, '_rest_op')
    def test__rest_post(self, _rest_op_mock):
        self.client._rest_post('/v1/foo', {}, {'data': 'Lorem ipsum'})
        _rest_op_mock.assert_called_once_with(
            'POST', '/v1/foo', {}, {'data': 'Lorem ipsum'})

    @mock.patch.object(v1.RestClientBase, '_rest_op')
    def test__rest_delete(self, _rest_op_mock):
        self.client._rest_delete('/v1/foo', None)
        _rest_op_mock.assert_called_once_with(
            'DELETE', '/v1/foo', None, None)
