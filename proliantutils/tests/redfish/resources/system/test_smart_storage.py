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

from proliantutils.redfish.resources.system import array_controller
from proliantutils.redfish.resources.system import smart_storage


class SmartStorageTestCase(testtools.TestCase):

    def setUp(self):
        super(SmartStorageTestCase, self).setUp()
        self.conn = mock.Mock()
        storage_file = ('proliantutils/tests/redfish/json_samples'
                        '/smart_storage.json')
        with open(storage_file, 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        path = ("/redfish/v1/Systems/1/SmartStorage")
        self.sys_stor = smart_storage.SmartStorage(
            self.conn, path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_stor._parse_attributes()
        self.assertEqual('1.0.2', self.sys_stor.redfish_version)

    def test_array_controllers(self):
        self.conn.get.return_value.json.reset_mock()
        coll = None
        value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'array_controller_collection.json')
        with open(path, 'r') as f:
            coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'array_controller.json', 'r') as f:
            value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [coll, value]
        self.assertIsNone(self.sys_stor._array_controllers)
        self.sys_stor.array_controllers
        self.assertIsInstance(self.sys_stor._array_controllers,
                              array_controller.ArrayControllerCollection)
