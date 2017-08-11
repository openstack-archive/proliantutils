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
import testtools

from oslo_utils import importutils


class HPEConnectorTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEConnectorTestCase, self).setUp()
        self.retry_backup = retrying.retry
        self.imp_str = 'proliantutils.redfish.connector'

    def test__op(self):
        retrying.retry = mock.MagicMock(return_value=lambda x: x, spec_set=[])
        hpe_connector = importutils.try_import(
            self.imp_str)
        conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', username='user',
            password='pass', verify=True)
        self.assertEqual(id(conn.__class__._op),
                         id(hpe_connector.HPEConnector._op))

    def test__op_retry(self):
        retrying.retry = mock.MagicMock(return_value=lambda x: "Hello",
                                        spec_set=[])
        try:
            sys.modules.pop(self.imp_str)
        except KeyError:
            pass
        hpe_connector = importutils.try_import(
            self.imp_str)
        self.assertEqual("Hello", hpe_connector.HPEConnector._op)

    def tearDown(self):
        super(HPEConnectorTestCase, self).tearDown()
        retrying.retry = self.retry_backup
        try:
            sys.modules.pop(self.imp_str)
        except KeyError:
            pass
