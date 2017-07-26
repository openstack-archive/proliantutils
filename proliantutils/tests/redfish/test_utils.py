# Copyright 2016 Hewlett Packard Enterprise Company, L.P.
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

"""Test class for Utils Module."""

import json

import ddt
import mock
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import system
from proliantutils.redfish import utils


@ddt.ddt
class UtilsTestCase(testtools.TestCase):

    def setUp(self):
        super(UtilsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = system_json['default']

        self.sys_inst = system.HPESystem(self.conn, '/redfish/v1/Systems/1',
                                         redfish_version='1.0.2')

    @ddt.data(('SecureBoot', '/redfish/v1/Systems/1/SecureBoot/'),
              (['Oem', 'Hpe', 'Links', 'NetworkAdapters'],
               '/redfish/v1/Systems/1/NetworkAdapters/'),
              )
    @ddt.unpack
    def test_get_subresource_path_by(self, subresource_path, expected_result):
        value = utils.get_subresource_path_by(self.sys_inst,
                                              subresource_path)
        self.assertEqual(expected_result, value)

    @ddt.data(('NonSecureBoot', 'attribute NonSecureBoot is missing'),
              (['Links', 'Chassis'],
               'attribute Links/Chassis/@odata.id is missing'),
              )
    @ddt.unpack
    def test_get_subresource_path_by_when_fails(
            self, subresource_path, expected_exception_string_subset):
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            expected_exception_string_subset,
            utils.get_subresource_path_by,
            self.sys_inst, subresource_path)

    def test_get_subresource_path_by_fails_with_empty_path(self):
        self.assertRaisesRegex(
            ValueError,
            '"subresource_path" cannot be empty',
            utils.get_subresource_path_by,
            self.sys_inst, [])

    @ddt.data((sys_cons.SUPPORTED_LEGACY_BIOS_ONLY,
               ('true', 'false')),
              (sys_cons.SUPPORTED_UEFI_ONLY,
               ('false', 'true')),
              (sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI,
               ('true', 'true')))
    @ddt.unpack
    def test_get_supported_boot_modes(self, boot_mode,
                                      expected_boot_modes):
        actual_boot_modes = utils.get_supported_boot_mode(boot_mode)
        self.assertEqual(expected_boot_modes, actual_boot_modes)

    @ddt.data(('SecureBoot', ['HEAD', 'GET', 'PATCH', 'POST']),
              ('Bios', ['GET', 'HEAD']))
    @ddt.unpack
    def test_get_allowed_operations(self, subresource_path, expected):
        response_mock = mock.MagicMock()
        response_mock.headers = {'Allow': expected}
        self.conn.get.return_value = response_mock
        ret_val = utils.get_allowed_operations(self.sys_inst, subresource_path)
        self.assertEqual(ret_val, expected)
