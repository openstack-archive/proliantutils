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

import mock
import testtools

from proliantutils import exception
from proliantutils.ilo import client
from proliantutils.ilo import firmware_controller
from proliantutils.ilo import ribcl
from proliantutils import utils


class UtilsTestCase(testtools.TestCase):

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def setUp(self, product_mock):
        super(UtilsTestCase, self).setUp()
        product_mock.return_value = 'Gen8'
        self.some_compact_fw_file = 'some_compact_fw_file.scexe'
        self.client = client.IloClient("1.2.3.4", "admin", "Admin")

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_throws_for_unknown_firmware_file_format(
            self, get_extractor_mock):
        # | GIVEN |
        exc = exception.InvalidInputError(reason='unknown firmware error')
        get_extractor_mock.side_effect = exc
        # | WHEN | & | THEN |
        ex = self.assertRaises(exception.InvalidInputError,
                               utils.process_firmware_image,
                               'invalid_compact_fw_file',
                               self.client)
        self.assertIn('Invalid Input: unknown firmware error', str(ex))

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_throws_for_failed_extraction(
            self, get_extractor_mock):
        # | GIVEN |
        exc = exception.ImageExtractionFailed(
            image_ref='some_file', reason='unknown firmware error')
        get_extractor_mock.return_value.extract.side_effect = exc
        # | WHEN | & | THEN |
        self.assertRaises(exception.ImageExtractionFailed,
                          utils.process_firmware_image,
                          self.some_compact_fw_file,
                          self.client)

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_calls_extract_of_fw_extractor_object(
            self, get_extractor_mock):
        # process_firmware_image calls extract on the firmware_extractor
        # instance
        # | GIVEN |
        get_extractor_mock.return_value.extract.return_value = (
            'core_fw_file.bin', True)
        # | WHEN |
        raw_fw_file, to_upload, is_extracted = (
            utils.process_firmware_image(self.some_compact_fw_file,
                                         self.client))
        # | THEN |
        get_extractor_mock.assert_called_once_with(self.some_compact_fw_file)
        get_extractor_mock.return_value.extract.assert_called_once_with()

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_asks_not_to_upload_firmware_file(
            self, get_extractor_mock):
        # | GIVEN |
        get_extractor_mock.return_value.extract.return_value = (
            'core_fw_file.bin', True)
        self.client.model = 'Gen8'
        # | WHEN |
        raw_fw_file, to_upload, is_extracted = (
            utils.process_firmware_image(self.some_compact_fw_file,
                                         self.client))
        # | THEN |
        self.assertEqual('core_fw_file.bin', raw_fw_file)
        self.assertFalse(to_upload)

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_asks_to_upload_firmware_file(
            self, get_extractor_mock):
        # if fw_version is greater than or equal to 2.0
        # | GIVEN |
        get_extractor_mock.return_value.extract.return_value = (
            'core_fw_file.bin', True)
        self.client.model = 'Gen9'
        # | WHEN |
        raw_fw_file, to_upload, is_extracted = (
            utils.process_firmware_image(self.some_compact_fw_file,
                                         self.client))
        # | THEN |
        self.assertEqual('core_fw_file.bin', raw_fw_file)
        self.assertTrue(to_upload)
