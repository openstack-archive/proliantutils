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
class ISCSISettingsTestCase(testtools.TestCase):

    def setUp(self):
        super(ISCSISettingsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/iscsi.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        self.iscsi_inst = iscsi.ISCSISettings(
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
