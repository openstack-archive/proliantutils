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

import mock
from sushy import connector
from sushy import exceptions
import testtools

from proliantutils.redfish import connector as hpe_connector


class HPEConnectorTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEConnectorTestCase, self).setUp()

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_no_exception(self, conn_mock):
        response = mock.MagicMock()
        type(response).status_code = mock.PropertyMock(return_value=200)
        conn_mock.side_effect = [response, exceptions.ConnectionError,
                                 response, response]
        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', verify=True)
        headers = {'X-Fake': 'header'}
        hpe_conn._op('GET', path='fake/path', data=None, headers=headers)
        conn_mock.assert_called_once_with(hpe_conn, 'GET', path='fake/path',
                                          data=None, headers=headers,
                                          allow_redirects=False)
        self.assertEqual(1, conn_mock.call_count)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_with_exception(self, conn_mock):
        response = mock.MagicMock()
        type(response).status_code = mock.PropertyMock(return_value=501)
        conn_mock.side_effect = [exceptions.ConnectionError,
                                 exceptions.ConnectionError,
                                 response, response]
        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', verify=True)
        headers = {'X-Fake': 'header'}
        lval = hpe_conn._op('GET', path='fake/path', data=None,
                            headers=headers)
        self.assertEqual(3, conn_mock.call_count)
        self.assertEqual(lval.status_code, 501)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_all_exception(self, conn_mock):
        conn_mock.side_effect = [
            exceptions.ConnectionError] * (
                hpe_connector.HPEConnector.MAX_RETRY_ATTEMPTS) + (
            ["Hello", "World"])
        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', verify=True)
        headers = {'X-Fake': 'header'}
        self.assertRaises(
            exceptions.ConnectionError, hpe_conn._op,
            'GET', path='fake/path', data=None, headers=headers)
        self.assertEqual(hpe_connector.HPEConnector.MAX_RETRY_ATTEMPTS,
                         conn_mock.call_count)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_with_redirection_false_status_308(self, conn_mock):
        response = mock.MagicMock()
        type(response).status_code = mock.PropertyMock(return_value=308)
        headers = {'X-Fake': 'header', 'Location': 'http://foo.bar:1234/new_path'}
        type(response).headers = headers
        response_redirect = mock.MagicMock()
        type(response_redirect).status_code = (
            mock.PropertyMock(return_value=200))
        conn_mock.side_effect = [response, response_redirect]
        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', verify=True)
        headers = {'X-Fake': 'header'}
        res = hpe_conn._op('GET', path='fake/path',
                           data=None, headers=headers)
        calls = [mock.call(hpe_conn, 'GET', path='fake/path', data=None,
                           headers=headers, allow_redirects=False),
                 mock.call(hpe_conn, 'GET', path='/new_path', data=None,
                           headers=headers, allow_redirects=False)]
        conn_mock.assert_has_calls(calls)
        self.assertEqual(res.status_code, 200)
