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

import mock
import testtools

from oslo_utils import importutils
from sushy import connector


class HPEConnectorTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEConnectorTestCase, self).setUp()
        self.retry_backup = retrying.retry
        retrying.retry = mock.MagicMock(return_value=lambda x: x, spec_set=[])
        hpe_connector = importutils.try_import(
            'proliantutils.redfish.connector')
        self.conn = hpe_connector.HPEConnector(
            'http://foo.bar:1234', username='user',
            password='pass', verify=True)

    def test__op(self):
        self.assertEqual(id(self.conn._op), id(connector.Connector._op))

    def tearDown(self):
        super(HPEConnectorTestCase, self).tearDown()
        retrying.retry = self.retry_backup
