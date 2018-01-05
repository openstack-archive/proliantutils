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

from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.manager import virtual_media


class HPEManagerTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEManagerTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/manager.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.mgr_inst = manager.HPEManager(
            self.conn, '/redfish/v1/Managers/1',
            redfish_version='1.0.2')

    def test_set_license(self):
        self.mgr_inst.set_license('testkey')
        self.mgr_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Managers/1/LicenseService/',
            data={'LicenseKey': 'testkey'})

    def test_virtual_media(self):
        self.assertIsNone(self.mgr_inst._virtual_media)

        self.conn.get.return_value.json.reset_mock()

        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_vmedia = self.mgr_inst.virtual_media

        self.assertIsInstance(actual_vmedia,
                              virtual_media.VirtualMediaCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()

        self.assertIs(actual_vmedia,
                      self.mgr_inst.virtual_media)
        self.conn.get.return_value.json.assert_not_called()

    def test_virtual_media_on_refresh(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_vmedia = self.mgr_inst.virtual_media

        self.assertIsInstance(actual_vmedia,
                              virtual_media.VirtualMediaCollection)

        with open('proliantutils/tests/redfish/'
                  'json_samples/manager.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.mgr_inst.invalidate()
        self.mgr_inst.refresh(force=False)

        self.assertIsNotNone(self.mgr_inst._virtual_media)
        self.assertTrue(self.mgr_inst._virtual_media._is_stale)

        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.assertIsInstance(self.mgr_inst.virtual_media,
                              virtual_media.VirtualMediaCollection)
        self.assertFalse(self.mgr_inst._virtual_media._is_stale)
