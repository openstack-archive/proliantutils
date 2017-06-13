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
from proliantutils.redfish.resources.manager import virtual_media


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

    def test__get_vmedia_collection_path(self):
        odata = self.man_inst._get_vmedia_collection_path()
        self.assertEqual("/redfish/v1/Managers/1/VirtualMedia/", odata)

    def test__get_vmedia_collection_path_missing_attr(self):
        self.man_inst._json.pop('VirtualMedia')
        self.assertRaisesRegex(
            exception.MissingAttributeError, 'attribute VirtualMedia',
            self.man_inst._get_vmedia_collection_path)

    def test_vmedia_resources(self):
        self.assertIsNone(self.man_inst._vmedia_resources)

        self.conn.get.return_value.json.reset_mock()

        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_vmedia = self.man_inst.vmedia_resources

        self.assertIsInstance(actual_vmedia,
                              virtual_media.VirtualMediaCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()

        self.assertIs(actual_vmedia,
                      self.man_inst.vmedia_resources)
        self.conn.get.return_value.json.assert_not_called()
