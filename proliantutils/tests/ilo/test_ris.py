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
import ris_sample_outputs as ris_outputs
import testtools

from proliantutils import exception
from proliantutils.ilo import ris


class TestRISOperationsPrivateMethods(testtools.TestCase):

    def setUp(self):
        super(TestRISOperationsPrivateMethods, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "admin", "Admin")

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
            'GET', '/v1/foo', {}, None)

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
        self.assertRaises(exception.IloConnectionError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)

    @mock.patch.object(httplib, 'HTTPSConnection')
    def test__rest_op_get_response_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.side_effect = RuntimeError("boom")
        self.assertRaises(exception.IloConnectionError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)

    @mock.patch.object(httplib, 'HTTPSConnection')
    def test__rest_op_response_read_error(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=200)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj
        response_mock_obj.read.side_effect = RuntimeError("boom")
        self.assertRaises(exception.IloConnectionError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)

    @mock.patch.object(httplib, 'HTTPSConnection')
    def test__rest_op_continous_redirection(self, https_con_mock):
        connection_mock_obj = mock.MagicMock()
        response_mock_obj = mock.MagicMock(status=301)
        https_con_mock.return_value = connection_mock_obj
        connection_mock_obj.getresponse.return_value = response_mock_obj

        sample_response_body = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        response_mock_obj.read.return_value = sample_response_body

        sample_headers = ris_outputs.HEADERS_FOR_REST_OP
        sample_headers.append(('location', 'foo'))
        response_mock_obj.getheaders.return_value = sample_headers

        self.assertRaises(exception.IloConnectionError,
                          self.client._rest_op,
                          'GET', '/v1/foo', {}, None)

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

    @mock.patch.object(httplib, 'HTTPSConnection')
    def test__rest_op_response_gzipped_resonse(self, https_con_mock):
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
