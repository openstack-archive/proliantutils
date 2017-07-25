# Copyright 2017 Hewlett Packard Enterprise Development LP
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

from proliantutils.redfish.resources.system.storage import drive


class DriveTestCase(testtools.TestCase):

    def setUp(self):
        super(DriveTestCase, self).setUp()
        self.conn = mock.Mock()
        drive_file = 'proliantutils/tests/redfish/json_samples/drive1.json'
        with open(drive_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        drive_path = ("/redfish/v1/Systems/437XR1138R2/Storage/1/"
                      "Drives/35D38F11ACEF7BD3")
        self.sys_drive = drive.Drive(
            self.conn, drive_path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_drive._parse_attributes()
        self.assertEqual('1.0.2', self.sys_drive.redfish_version)
        self.assertEqual(None, self.sys_drive.identity)
