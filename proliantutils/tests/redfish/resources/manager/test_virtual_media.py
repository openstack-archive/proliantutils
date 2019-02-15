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
import testtools

from sushy import exceptions

from proliantutils import exception
from proliantutils.redfish.resources.manager import constants
from proliantutils.redfish.resources.manager import virtual_media


class VirtualMediaCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(VirtualMediaCollectionTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        self.vmedia_coll_inst = virtual_media.VirtualMediaCollection(
            self.conn, '/redfish/v1/Managers/1/VirtualMedia',
            redfish_version='1.0.2')

    def test_get_member_device(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        obj = self.vmedia_coll_inst.get_member_device(
            constants.VIRTUAL_MEDIA_CD)

        self.assertIsInstance(obj, virtual_media.VirtualMedia)


class VirtualMediaTestCase(testtools.TestCase):

    def setUp(self):
        super(VirtualMediaTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        self.conn.get.return_value.json.return_value = vmedia_json[
            'default']

        self.vmedia_inst = virtual_media.VirtualMedia(
            self.conn, '/redfish/v1/Managers/1/VirtualMedia/2',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.vmedia_inst._parse_attributes()
        self.assertEqual(['cd', 'dvd'], self.vmedia_inst.media_types)
        self.assertEqual(False, self.vmedia_inst.inserted)

    def test__parse_attributes_missing_actions(self):
        self.vmedia_inst.json.pop('Oem')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Oem/Hpe/Actions',
            self.vmedia_inst._parse_attributes)

    def test__get_action_element_insert(self):
        value = self.vmedia_inst._get_action_element('insert')
        self.assertEqual("/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/"
                         "Hpe/HpeiLOVirtualMedia.InsertVirtualMedia/",
                         value.target_uri)

    def test__get_action_element_missing_insert_action(self):
        self.vmedia_inst._hpe_actions.insert_vmedia = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'attribute #HpeiLOVirtualMedia.InsertVirtualMedia',
            self.vmedia_inst._get_action_element, 'insert')

    def test__get_action_element_eject(self):
        value = self.vmedia_inst._get_action_element('eject')
        self.assertEqual("/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/"
                         "Hpe/HpeiLOVirtualMedia.EjectVirtualMedia/",
                         value.target_uri)

    def test__get__action_element_missing_eject_action(self):
        self.vmedia_inst._hpe_actions.eject_vmedia = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'attribute #HpeiLOVirtualMedia.EjectVirtualMedia',
            self.vmedia_inst._get_action_element, 'eject')

    @mock.patch.object(virtual_media.VirtualMedia, 'insert_media')
    def test_insert_media_sushy(self, insert_mock):
        insert_mock.return_value = None
        url = "http://1.2.3.4:5678/xyz.iso"
        self.vmedia_inst.insert_vmedia_device(url)
        self.vmedia_inst.insert_media.assert_called_once_with(
            url, write_protected=True)

    @mock.patch.object(virtual_media.VirtualMedia, 'insert_media')
    def test_insert_vmedia(self, insert_mock):
        url = "http://1.2.3.4:5678/xyz.iso"
        insert_mock.side_effect = exceptions.SushyError
        self.vmedia_inst.insert_vmedia_device(url)
        self.vmedia_inst._conn.post.assert_called_once_with(
            "/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/Hpe/"
            "HpeiLOVirtualMedia.InsertVirtualMedia/",
            data={'Image': url})

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_media')
    def test_eject_media_sushy(self, eject_mock):
        eject_mock.return_value = None
        self.vmedia_inst.eject_vmedia_device()
        self.vmedia_inst.eject_media.assert_called_once()

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_media')
    def test_eject_vmedia(self, eject_mock):
        eject_mock.side_effect = exceptions.SushyError
        self.vmedia_inst.eject_vmedia_device()
        self.vmedia_inst._conn.post.assert_called_once_with(
            "/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/Hpe/"
            "HpeiLOVirtualMedia.EjectVirtualMedia/",
            data={})

    def test_set_vm_status(self):
        value = {'Oem': {'Hpe': {'BootOnNextServerReset': True}}}
        self.vmedia_inst.set_vm_status(True)
        self.vmedia_inst._conn.patch.assert_called_once_with(
            "/redfish/v1/Managers/1/VirtualMedia/2",
            data=value)
