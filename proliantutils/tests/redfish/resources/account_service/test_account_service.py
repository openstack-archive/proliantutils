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
                  'json_samples/account_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.acc_inst = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

    def test_accounts(self):
        self.assertIsNone(self.acc_inst._accounts)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        accounts = self.acc_inst.accounts
        self.assertIsInstance(accounts, account.HPEAccountCollection)

    def test_accounts_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        accounts = self.acc_inst.accounts
        self.assertIsInstance(accounts, account.HPEAccountCollection)

        with open('proliantutils/tests/redfish/'
                  'json_samples/account_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.acc_inst.invalidate()
        self.acc_inst.refresh(force=False)

        self.assertIsNotNone(self.acc_inst._accounts)
        self.assertTrue(self.acc_inst._accounts._is_stale)

        with open('proliantutils/tests/redfish/'
                  'json_samples/account_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.assertIsInstance(self.acc_inst.accounts,
                              account.HPEAccountCollection)
        self.assertFalse(self.acc_inst._accounts._is_stale)
