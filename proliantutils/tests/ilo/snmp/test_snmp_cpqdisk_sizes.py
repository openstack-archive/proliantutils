#!/usr/bin/env python
# Copyright 2017 Hewlett-Packard Enterprise Development Company, L.P.
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
import unittest

import mock
from pysnmp import hlapi

from proliantutils.ilo.snmp import snmp_cpqdisk_sizes
from proliantutils.tests.ilo.snmp import snmp_sample_output


class SnmpTestCase(unittest.TestCase):

    def setUp(self):
        super(SnmpTestCase, self).setUp()

    @mock.patch.object(snmp_cpqdisk_sizes, '_get_disksize_MiB')
    def test_get_local_gb(self, get_disk_mock):
        iLOIp = 'a.b.c.d'
        authUser = 'user'
        authProtValue = '1234'
        privProtValue = '4321'
        authProtocl = 'SHA'
        privProtocol = 'AES'
        disk_snmp_data = {'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.0':
                          {'cpqDaPhyDrvSize': '279'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.1':
                          {'cpqDaPhyDrvSize': '279'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.2':
                          {'cpqDaPhyDrvSize': '558'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.3':
                          {'cpqDaPhyDrvSize': '279'}}
        get_disk_mock.return_value = disk_snmp_data
        actual_size = snmp_cpqdisk_sizes.get_local_gb(iLOIp, authUser,
                                                      authProtValue,
                                                      privProtValue,
                                                      authProtocl,
                                                      privProtocol)
        expected_size = 558
        self.assertEqual(actual_size, expected_size)
        get_disk_mock.assert_called_once_with(iLOIp, authUser,
                                              authProtValue,
                                              privProtValue,
                                              authProtocl,
                                              privProtocol)

    def test__parse_auth_protocol_sha(self):
        authProtocol = 'SHA'
        expected = hlapi.usmHMACSHAAuthProtocol
        actual = snmp_cpqdisk_sizes._parse_auth_protocol(authProtocol)
        self.assertEqual(expected, actual)

    def test__parse_auth_protocol_md5(self):
        authProtocol = 'MD5'
        expected = hlapi.usmHMACMD5AuthProtocol
        actual = snmp_cpqdisk_sizes._parse_auth_protocol(authProtocol)
        self.assertEqual(expected, actual)

    def test__parse_auth_protocol_none(self):
        authProtocol = None
        expected = hlapi.usmNoAuthProtocol
        actual = snmp_cpqdisk_sizes._parse_auth_protocol(authProtocol)
        self.assertEqual(expected, actual)

    def test__parse_privacy_protocol_aes(self):
        privProtocol = 'AES'
        expected = hlapi.usmAesCfb128Protocol
        actual = snmp_cpqdisk_sizes._parse_privacy_protocol(privProtocol)
        self.assertEqual(expected, actual)

    def test__parse_privacy_protocol_des(self):
        privProtocol = 'DES'
        expected = hlapi.usmDESPrivProtocol
        actual = snmp_cpqdisk_sizes._parse_privacy_protocol(privProtocol)
        self.assertEqual(expected, actual)

    def test__parse_privacy_protocol_none(self):
        privProtocol = None
        expected = hlapi.usmNoPrivProtocol
        actual = snmp_cpqdisk_sizes._parse_privacy_protocol(privProtocol)
        self.assertEqual(expected, actual)

    @mock.patch.object(snmp_cpqdisk_sizes, '_parse_auth_protocol')
    @mock.patch.object(snmp_cpqdisk_sizes, '_parse_privacy_protocol')
    @mock.patch.object(snmp_cpqdisk_sizes, '_parse_mibs')
    def test__get_disksize_MiB(self, mib_mock, priv_mock,
                              auth_mock):
        iLOIP = 'a.b.c.d'
        authUser = 'user'
        authProtValue = '1234'
        privProtValue = '4321'
        authProtocol = 'SHA'
        privProtocol = 'AES'
        mib_mock.return_value = snmp_sample_output.PHY_DRIVE_MIB_OUTPUT
        priv_mock.return_value = hlapi.usmAesCfb128Protocol
        auth_mock.return_value = hlapi.usmHMACSHAAuthProtocol
        actual = snmp_cpqdisk_sizes._get_disksize_MiB(iLOIP, authUser,
                                                     authProtValue,
                                                     privProtValue,
                                                     authProtocol,
                                                     privProtocol)
        expected = {'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.0':
                    {'cpqDaPhyDrvSize': '279'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.1':
                    {'cpqDaPhyDrvSize': '279'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.2':
                    {'cpqDaPhyDrvSize': '279'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.3':
                    {'cpqDaPhyDrvSize': '279'}}
        self.assertEqual(expected, actual)
