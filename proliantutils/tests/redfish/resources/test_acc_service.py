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

import mock
import testtools

from proliantutils.redfish.resources.account_service import account_service


class HPEAccountServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountServiceTestCase, self).setUp()
        self.conn = mock.MagicMock()

        self.acc_inst = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

    def test_update_credentials(self):
        member_uri = '/redfish/v1/AccountService/Accounts/1/'
        password = {'Password': 'fake-password'}
        self.acc_inst.update_credentials(member_uri, password)
        self.acc_inst._conn.patch.assert_called_once_with(
            member_uri, data={'Password': 'fake-password'})
