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
"""Test class for Client Module."""

import mock
import testtools

from proliantutils.ilo import client
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris


class IloClientTestCase(testtools.TestCase):

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def setUp(self, product_mock):
        super(IloClientTestCase, self).setUp()
        product_mock.return_value = 'Gen8'
        self.client = client.IloClient("1.2.3.4", "admin", "Admin")

    @mock.patch.object(ribcl.RIBCLOperations, 'get_all_licenses')
    def test__call_method_ribcl(self, license_mock):
        self.client._call_method('get_all_licenses')
        license_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, 'get_host_power_status')
    def test__call_method_ris(self, power_mock):
        self.client.model = 'Gen9'
        self.client._call_method('get_host_power_status')
        power_mock.assert_called_once_with()