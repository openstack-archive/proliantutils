# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

"""Test class for IPMI Module."""

import subprocess
import unittest

import mock

from proliantutils.ilo import ipmi
from proliantutils.tests.ilo import ipmi_sample_outputs as constants


class IloIpmiTestCase(unittest.TestCase):

    def setUp(self):
        super(IloIpmiTestCase, self).setUp()
        self.info = {'address': "x.x.x.x",
                     'username': "admin",
                     'password': "Admin"}

    @mock.patch.object(ipmi, '_parse_ipmi_nic_capacity')
    @mock.patch.object(ipmi, '_exec_ipmitool')
    def test_get_nic_capacity(self, ipmi_mock, parse_mock):
        ipmi_mock.return_value = constants.NIC_FRU_OUT
        parse_mock.return_value = "1Gb"
        expected_out = "1Gb"
        actual_out = ipmi.get_nic_capacity(self.info)
        self.assertEqual(expected_out, actual_out)

    @mock.patch.object(ipmi, '_parse_ipmi_nic_capacity')
    @mock.patch.object(ipmi, '_exec_ipmitool')
    def test_get_nic_capacity_loop_N_times(self, ipmi_mock, parse_mock):
        ipmi_mock.side_effect = ["Device not present", "Device not present",
                                 "Device not present", "Device not present",
                                 "Device not present", "Device not present",
                                 "Device not present", "Device not present",
                                 constants.NIC_FRU_OUT]
        parse_mock.return_value = "1Gb"
        expected_out = "1Gb"
        actual_out = ipmi.get_nic_capacity(self.info)
        self.assertEqual(ipmi_mock.call_count, 9)
        self.assertEqual(expected_out, actual_out)

    @mock.patch.object(ipmi, '_parse_ipmi_nic_capacity')
    @mock.patch.object(ipmi, '_exec_ipmitool')
    def test_get_nic_capacity_none(self, ipmi_mock, parse_mock):
        ipmi_mock.return_value = constants.NIC_FRU_OUT
        parse_mock.return_value = None
        actual_out = ipmi.get_nic_capacity(self.info)
        self.assertIsNone(actual_out)
        self.assertEqual(ipmi_mock.call_count, 255)

    @mock.patch.object(subprocess, 'check_output')
    def test__exec_ipmitool(self, check_mock):
        check_mock.return_value = constants.NIC_FRU_OUT
        expected_output = constants.NIC_FRU_OUT
        cmd = "fru print 0x64"
        actual_out = ipmi._exec_ipmitool(self.info, cmd)
        self.assertEqual(expected_output, actual_out)

    @mock.patch.object(subprocess, 'check_output')
    def test__exec_ipmitool_none(self, check_mock):
        check_mock.side_effect = Exception
        cmd = "fru print 0x2"
        actual_out = ipmi._exec_ipmitool(self.info, cmd)
        self.assertIsNone(actual_out)

    def test__parse_ipmi_nic_capacity(self):
        exec_output = constants.NIC_FRU_OUT
        expected_output = "1Gb"
        actual_out = ipmi._parse_ipmi_nic_capacity(exec_output)
        self.assertEqual(expected_output, actual_out)

    def test__parse_ipmi_nic_capacity_no_port_details(self):
        exec_output = constants.NIC_FRU_OUT_NO_PORT_DETAILS
        actual_out = ipmi._parse_ipmi_nic_capacity(exec_output)
        self.assertIsNone(actual_out)

    def test__parse_ipmi_nic_capacity_no_product_name(self):
        exec_output = constants.NIC_FRU_OUT_NO_PRODUCT_NAME
        actual_out = ipmi._parse_ipmi_nic_capacity(exec_output)
        self.assertIsNone(actual_out)
