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

from proliantutils.ilo.snmp import snmp_cpqdisk_sizes as snmp
from proliantutils.tests.unit.ilo.snmp import snmp_sample_output


class SnmpTestCase(unittest.TestCase):

    def setUp(self):
        super(SnmpTestCase, self).setUp()

    @mock.patch.object(snmp, '_get_disksize_MiB')
    def test_get_local_gb(self, get_disk_mock):
        iLOIp = 'a.b.c.d'
        snmp_credentials = {'auth_user': 'user',
                            'auth_prot_pp': '1234',
                            'auth_priv_pp': '4321',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': 'true'}
        disk_snmp_data = {'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.0':
                          {'cpqDaPhyDrvSize': '286102'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.1':
                          {'cpqDaPhyDrvSize': '286102'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.2':
                          {'cpqDaPhyDrvSize': '572316'},
                          'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.3':
                          {'cpqDaPhyDrvSize': '286102'}}
        get_disk_mock.return_value = disk_snmp_data
        actual_size = snmp.get_local_gb(iLOIp, snmp_credentials)
        expected_size = (572316/1024)
        self.assertEqual(actual_size, expected_size)
        get_disk_mock.assert_called_once_with(iLOIp, snmp_credentials)

    @mock.patch.object(snmp, '_parse_mibs')
    def test__get_disksize_MiB(self, mib_mock):
        iLOIP = 'a.b.c.d'
        snmp_credentials = {'auth_user': 'user',
                            'auth_prot_pp': '1234',
                            'auth_priv_pp': '4321',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': 'true'}
        mib_mock.return_value = snmp_sample_output.PHY_DRIVE_MIB_OUTPUT
        actual = snmp._get_disksize_MiB(iLOIP, snmp_credentials)
        expected = {'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.0':
                    {'cpqDaPhyDrvSize': '286102'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.1':
                    {'cpqDaPhyDrvSize': '286102'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.2':
                    {'cpqDaPhyDrvSize': '286102'},
                    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.3':
                    {'cpqDaPhyDrvSize': '286102'}}
        self.assertEqual(expected, actual)
