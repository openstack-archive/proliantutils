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

import mock
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.manager import manager


class HPEManagerTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEManagerTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/manager.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.man_inst = manager.HPEManager(
            self.conn, '/redfish/v1/Managers/1',
            redfish_version='1.0.2')

    def test_get_license_uri_action_missing_uri(self):
        self.man_inst.get_license_uri = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'Oem/Hpe/Links/LicenseService uri is missing',
            self.man_inst.get_license_uri)

    def test_get_license_uri_action_validate_uri(self):
        license_uri = '/redfish/v1/Managers/1/LicenseService/'
        test_uri = self.man_inst.get_license_uri()
        self.assertEqual(test_uri, license_uri)

    def test_set_license(self):
        license_uri = '/redfish/v1/Managers/1/LicenseService/'
        self.man_inst.set_license({'License_key': 'testkey'})
        self.man_inst._conn.post.assert_called_once_with(
            license_uri, data={'License_key': 'testkey'})
