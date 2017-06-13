# Copyright 2017 Hewlett Packard Enterprise Development LP
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

__author__ = 'HPE'

import json

import mock
from sushy import exceptions
import testtools

from proliantutils.redfish.resources.manager import virtual_media


class VirtualMediaTestCase(testtools.TestCase):

    def setUp(self):
        super(VirtualMediaTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        self.conn.get.return_value.json.return_value = vmedia_json[
            'Vmedia_Not_Inserted']

        self.vmedia_inst = virtual_media.VirtualMedia(
            self.conn, '/redfish/v1/Managers/1/VirtualMedia/2',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.vmedia_inst._parse_attributes()
        self.assertEqual(['CD', 'DVD'], self.vmedia_inst.media_types)
        self.assertEqual(False, self.vmedia_inst.is_vmedia_inserted)

    def test__parse_attributes_missing_actions(self):
        self.vmedia_inst.json.pop('Oem')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Oem/Hpe/Actions',
            self.vmedia_inst._parse_attributes)

    def test_get__insert_action_element(self):
        value = self.vmedia_inst._get_insert_action_element()
        self.assertEqual("/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/"
                         "Hpe/HpeiLOVirtualMedia.InsertVirtualMedia/",
                         value.target_uri)

    def test_get__insert_action_element_missing_reset_action(self):
        self.vmedia_inst._actions.insert_vmedia = None
        self.assertRaisesRegex(
            exceptions.MissingActionError,
            'action #HpeiLOVirtualMedia.InsertVirtualMedia',
            self.vmedia_inst._get_insert_action_element)

    def test_get__eject_action_element(self):
        value = self.vmedia_inst._get_eject_action_element()
        self.assertEqual("/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/"
                         "Hpe/HpeiLOVirtualMedia.EjectVirtualMedia/",
                         value.target_uri)

    def test_get__eject_action_element_missing_reset_action(self):
        self.vmedia_inst._actions.eject_vmedia = None
        self.assertRaisesRegex(
            exceptions.MissingActionError,
            'action #HpeiLOVirtualMedia.EjectVirtualMedia',
            self.vmedia_inst._get_eject_action_element)

    def test_insert_vmedia(self):
        url = "http://1.2.3.4:5678/xyz.iso"
        self.vmedia_inst.insert_vmedia(url)
        self.vmedia_inst._conn.post.assert_called_once_with(
            "/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/Hpe/"
            "HpeiLOVirtualMedia.InsertVirtualMedia/",
            data={'Image': url})

    def test_eject_insert_vmedia(self):
        self.vmedia_inst.eject_vmedia()
        self.vmedia_inst._conn.post.assert_called_once_with(
            "/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/Hpe/"
            "HpeiLOVirtualMedia.EjectVirtualMedia/",
            data={})
