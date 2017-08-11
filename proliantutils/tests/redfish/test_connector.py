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

import retrying
import sys

import mock
from sushy import connector
from sushy import exceptions
import testtools

from oslo_utils import importutils


class HPEConnectorTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEConnectorTestCase, self).setUp()
        self.imp_str = 'proliantutils.redfish.connector'

    def _get_connector(self):
        try:
            sys.modules.pop(self.imp_str)
        except KeyError:
            pass
        connector = importutils.try_import(
            self.imp_str)
        return connector

    @mock.patch.object(retrying, 'retry', autospec=True)
    def test__op_retry(self, retry_mock):
        retry_mock.return_value = lambda x: "Hello"
        hpe_connector = self._get_connector()
        self.assertEqual("Hello", hpe_connector.HPEConnector._op)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_no_exception(self, conn_mock):
        hpe_connector = self._get_connector()
        conn_mock.side_effect = ["Hello", exceptions.ConnectionError,
                                 "Hello", "World"]

        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', username='user',
            password='pass', verify=True)
        headers = {'X-Fake': 'header'}
        hpe_conn._op('GET', path='fake/path', data=None, headers=headers)
        conn_mock.assert_called_once_with(hpe_conn, 'GET', path='fake/path',
                                          data=None, headers=headers)
        self.assertEqual(1, conn_mock.call_count)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_with_exception(self, conn_mock):
        hpe_connector = self._get_connector()
        conn_mock.side_effect = [exceptions.ConnectionError,
                                 exceptions.ConnectionError, "Hello", "World"]

        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', username='user',
            password='pass', verify=True)
        headers = {'X-Fake': 'header'}
        hpe_conn._op('GET', path='fake/path', data=None, headers=headers)
        self.assertEqual(3, conn_mock.call_count)

    @mock.patch.object(connector.Connector, '_op', autospec=True)
    def test__op_all_exception(self, conn_mock):
        hpe_connector = self._get_connector()
        conn_mock.side_effect = [
            exceptions.ConnectionError] * (
                hpe_connector.HPEConnector.MAX_RETRY_ATTEMPTS) + (
            ["Hello", "World"])

        hpe_conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', username='user',
            password='pass', verify=True)
        headers = {'X-Fake': 'header'}
        self.assertRaises(
            exceptions.ConnectionError, hpe_conn._op,
            'GET', path='fake/path', data=None, headers=headers)
        self.assertEqual(hpe_connector.HPEConnector.MAX_RETRY_ATTEMPTS,
                         conn_mock.call_count)

    def tearDown(self):
        super(HPEConnectorTestCase, self).tearDown()
        try:
            sys.modules.pop(self.imp_str)
        except KeyError:
            pass
