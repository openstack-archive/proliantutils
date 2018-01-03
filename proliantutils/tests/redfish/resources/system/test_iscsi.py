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

import json

import ddt
import mock
import testtools

from proliantutils.redfish.resources.system import iscsi
from proliantutils.redfish import utils


@ddt.ddt
class ISCSIResourceTestCase(testtools.TestCase):

    def setUp(self):
        super(ISCSIResourceTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        self.iscsi_inst = iscsi.ISCSIResource(
            self.conn, '/redfish/v1/Systems/1/bios/iscsi',
            redfish_version='1.0.2')

    @ddt.data((['GET', 'PATCH', 'POST', 'HEAD'], True),
              (['GET', 'HEAD'], False))
    @ddt.unpack
    @mock.patch.object(utils, 'get_allowed_operations')
    def test_is_iscsi_boot_supported(self, allowed_method,
                                     expected, get_method_mock):
        get_method_mock.return_value = allowed_method
        ret_val = self.iscsi_inst.is_iscsi_boot_supported()
        self.assertEqual(ret_val, expected)

    def test_iscsi_settings(self):
        self.assertIsNone(self.iscsi_inst._iscsi_settings)

        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi_settings.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])
        actual_settings = self.iscsi_inst.iscsi_settings
        self.assertIsInstance(actual_settings,
                              iscsi.ISCSISettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_settings,
                      self.iscsi_inst.iscsi_settings)
        self.conn.get.return_value.json.assert_not_called()

    def test_iscsi_resource_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi_settings.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])
        actual_settings = self.iscsi_inst.iscsi_settings
        self.assertIsInstance(actual_settings,
                              iscsi.ISCSISettings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))
        self.iscsi_inst.refresh()
        self.assertIsNone(self.iscsi_inst._iscsi_settings)

        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi_settings.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])
        self.assertIsInstance(actual_settings,
                              iscsi.ISCSISettings)


class ISCSISettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(ISCSISettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi_settings.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['Default'])

        self.iscsi_settings_inst = iscsi.ISCSISettings(
            self.conn, '/redfish/v1/Systems/1/bios/iscsi/settings',
            redfish_version='1.0.2')

    def test_update_iscsi_settings(self):
        target_uri = '/redfish/v1/Systems/1/bios/iscsi/settings'
        iscsi_data = {'iSCSITargetName':
                      'iqn.2011-07.com.example.server:test1',
                      'iSCSILUN': '1',
                      'iSCSITargetIpAddress': '10.10.1.30',
                      'iSCSITargetTcpPort': 3260,
                      'iSCSITargetInfoViaDHCP': False,
                      'iSCSIConnection': 'Enabled',
                      'iSCSIAttemptName': 'NicBoot1',
                      'iSCSINicSource': 'NicBoot1',
                      'iSCSIAttemptInstance': 1}

        data = {
            'iSCSISources': iscsi_data
        }
        self.iscsi_settings_inst.update_iscsi_settings(data)
        self.iscsi_settings_inst._conn.patch.assert_called_once_with(
            target_uri, data=data)
