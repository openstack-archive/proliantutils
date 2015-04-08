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
"""Test Class for Common Operations."""

import time
import unittest

import mock

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ribcl
from proliantutils.tests.ilo import ribcl_sample_outputs as ribcl_output


class IloCommonModuleTestCase(unittest.TestCase):

    def setUp(self):
        super(IloCommonModuleTestCase, self).setUp()
        self.ribcl = ribcl.RIBCLOperations("x.x.x.x", "admin", "Admin",
                                           60, 443)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_ribcl_ok(self, name_mock):
        name_mock.return_value = ribcl_output.GET_PRODUCT_NAME
        common.wait_for_ilo_after_reset(self.ribcl)
        name_mock.assert_called_once_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_retry(self, name_mock, sleep_mock):
        exc = exception.IloError('error')
        name_mock.side_effect = [exc, ribcl_output.GET_PRODUCT_NAME]
        common.wait_for_ilo_after_reset(self.ribcl)
        self.assertEqual(2, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_fail(self, name_mock, time_mock):
        exc = exception.IloError('error')
        name_mock.side_effect = exc
        self.assertRaises(exception.IloConnectionError,
                          common.wait_for_ilo_after_reset,
                          self.ribcl)
        self.assertEqual(common.RETRY_COUNT, name_mock.call_count)
        name_mock.assert_called_with()
