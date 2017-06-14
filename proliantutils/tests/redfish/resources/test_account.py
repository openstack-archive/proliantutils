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


class HPEAccountCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountCollectionTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['GET_ACCOUNT_INFO'])

        self.account_obj = account.HPEAccountCollection(
            self.conn, '/redfish/v1/AccountService/Accounts',
            redfish_version='1.0.2')

    def test_get_member_uri(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['GET_ACCOUNT_DETAILS'])

        obj = self.account_obj.get_member_details('foo')
        self.assertIsInstance(obj, account.HPEAccount)


class HPEAccountTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            account_data_json = json.loads(f.read())

        self.conn.get.return_value.json.return_value = account_data_json[
            'GET_ACCOUNT_DETAILS']

        self.acc_inst = account.HPEAccount(
            self.conn, '/redfish/v1/AccountService/Accounts/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.acc_inst._parse_attributes()
        self.assertEqual('foo', self.acc_inst.username)
