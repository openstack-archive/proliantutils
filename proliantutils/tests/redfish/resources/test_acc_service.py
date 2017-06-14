# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__author__ = 'HPE'

import json

import mock
import testtools

from proliantutils.redfish.resources.account_service import account
from proliantutils.redfish.resources.account_service import account_service


class HPEAccountServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountServiceTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.acc_inst = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

    def test_accounts(self):
        self.assertIsNone(self.acc_inst._accounts)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['GET_ACCOUNT_INFO'])
        accounts = self.acc_inst.accounts
        self.assertIsInstance(accounts, account.HPEAccountCollection)
