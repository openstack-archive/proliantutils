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

    def test_get_vm_device(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['Vmedia_Not_Inserted']]

        obj = self.man_inst._get_vm_device('CDROM')

        self.assertIsInstance(obj, virtual_media.VirtualMedia)

    def test__get_vm_device_invalid(self):
        msg = "Invalid device. Valid devices: FLOPPY or CDROM."
        self.assertRaisesRegex(
            exception.IloInvalidInputError, msg,
            self.man_inst._get_vm_device, 'XXXX')

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_vmedia(self, eject_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        eject_mock.return_value = mock.MagicMock(status_code=201)
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['Vmedia_Inserted']]

        self.man_inst.eject_vmedia('CDROM')

        eject_mock.assert_called_once_with()

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    def test_eject_vmedia_not_inserted(self, eject_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        eject_mock.return_value = mock.MagicMock(status_code=201)
        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['Vmedia_Not_Inserted']]

        self.man_inst.eject_vmedia('CDROM')

        self.assertFalse(eject_mock.called)

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_vmedia(self, insert_mock, eject_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['Vmedia_Not_Inserted']]
        url = 'http://1.2.3.4:5678/xyz.iso'
        insert_mock.return_value = mock.MagicMock(status_code=201)

        self.man_inst.insert_vmedia(url, 'CDROM')

        self.assertFalse(eject_mock.called)
        insert_mock.assert_called_once_with(url)

    @mock.patch.object(virtual_media.VirtualMedia, 'eject_vmedia')
    @mock.patch.object(virtual_media.VirtualMedia, 'insert_vmedia')
    def test_insert_vmedia_inserted(self, insert_mock, eject_mock):
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia_collection.json', 'r') as f:
            vmedia_collection_json = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/vmedia.json', 'r') as f:
            vmedia_json = json.loads(f.read())

        self.conn.get.return_value.json.side_effect = [
            vmedia_collection_json, vmedia_json['Vmedia_Inserted']]
        url = 'http://1.2.3.4:5678/xyz.iso'
        insert_mock.return_value = mock.MagicMock(status_code=201)

        self.man_inst.insert_vmedia(url, 'CDROM')

        eject_mock.assert_called_once_with()
        insert_mock.assert_called_once_with(url)
