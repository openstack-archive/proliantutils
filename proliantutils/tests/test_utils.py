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

import hashlib

import mock
import requests
import six
import six.moves.builtins as __builtin__
from six.moves import http_client
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
        get_extractor_mock.side_effect = exception.InvalidInputError
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          utils.process_firmware_image,
                          'invalid_compact_fw_file',
                          self.client)

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_throws_for_failed_extraction(
            self, get_extractor_mock):
        # | GIVEN |
        exc = exception.ImageExtractionFailed(
            image_ref='some_file', reason='God only knows!')
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

    @mock.patch.object(firmware_controller, 'get_fw_extractor',
                       spec_set=True, autospec=True)
    def test_process_firmware_image_asks_to_upload_firmware_file_Gen10(
            self, get_extractor_mock):
        # if fw_version is greater than or equal to 2.0
        # | GIVEN |
        get_extractor_mock.return_value.extract.return_value = (
            'core_fw_file.bin', True)
        self.client.model = 'Gen10'
        # | WHEN |
        raw_fw_file, to_upload, is_extracted = (
            utils.process_firmware_image(self.some_compact_fw_file,
                                         self.client))
        # | THEN |
        self.assertEqual('core_fw_file.bin', raw_fw_file)
        self.assertTrue(to_upload)

    @mock.patch.object(utils, 'hashlib', autospec=True)
    def test__get_hash_object(self, hashlib_mock):
        algorithms_available = ('md5', 'sha1', 'sha224',
                                'sha256', 'sha384', 'sha512')
        hashlib_mock.algorithms_guaranteed = algorithms_available
        hashlib_mock.algorithms = algorithms_available
        # | WHEN |
        utils._get_hash_object('md5')
        utils._get_hash_object('sha1')
        utils._get_hash_object('sha224')
        utils._get_hash_object('sha256')
        utils._get_hash_object('sha384')
        utils._get_hash_object('sha512')
        # | THEN |
        calls = [mock.call.md5(), mock.call.sha1(), mock.call.sha224(),
                 mock.call.sha256(), mock.call.sha384(), mock.call.sha512()]
        hashlib_mock.assert_has_calls(calls)

    def test__get_hash_object_throws_for_invalid_or_unsupported_hash_name(
            self):
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          utils._get_hash_object,
                          'hickory-dickory-dock')

    def test_hash_file_for_md5(self):
        # | GIVEN |
        data = b'Mary had a little lamb, its fleece as white as snow'
        file_like_object = six.BytesIO(data)
        expected = hashlib.md5(data).hexdigest()
        # | WHEN |
        actual = utils.hash_file(file_like_object)  # using default, 'md5'
        # | THEN |
        self.assertEqual(expected, actual)

    def test_hash_file_for_sha1(self):
        # | GIVEN |
        data = b'Mary had a little lamb, its fleece as white as snow'
        file_like_object = six.BytesIO(data)
        expected = hashlib.sha1(data).hexdigest()
        # | WHEN |
        actual = utils.hash_file(file_like_object, 'sha1')
        # | THEN |
        self.assertEqual(expected, actual)

    def test_hash_file_for_sha512(self):
        # | GIVEN |
        data = b'Mary had a little lamb, its fleece as white as snow'
        file_like_object = six.BytesIO(data)
        expected = hashlib.sha512(data).hexdigest()
        # | WHEN |
        actual = utils.hash_file(file_like_object, 'sha512')
        # | THEN |
        self.assertEqual(expected, actual)

    def test_hash_file_throws_for_invalid_or_unsupported_hash(self):
        # | GIVEN |
        data = b'Mary had a little lamb, its fleece as white as snow'
        file_like_object = six.BytesIO(data)
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError, utils.hash_file,
                          file_like_object, 'hickory-dickory-dock')

    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_verify_image_checksum(self, open_mock):
        # | GIVEN |
        data = b'Yankee Doodle went to town riding on a pony;'
        file_like_object = six.BytesIO(data)
        open_mock().__enter__.return_value = file_like_object
        actual_hash = hashlib.md5(data).hexdigest()
        # | WHEN |
        utils.verify_image_checksum(file_like_object, actual_hash)
        # | THEN |
        # no any exception thrown

    def test_verify_image_checksum_throws_for_nonexistent_file(self):
        # | GIVEN |
        invalid_file_path = '/some/invalid/file/path'
        # | WHEN | & | THEN |
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.verify_image_checksum,
                          invalid_file_path, 'hash_xxx')

    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_verify_image_checksum_throws_for_failed_validation(self,
                                                                open_mock):
        # | GIVEN |
        data = b'Yankee Doodle went to town riding on a pony;'
        file_like_object = six.BytesIO(data)
        open_mock().__enter__.return_value = file_like_object
        invalid_hash = 'invalid_hash_value'
        # | WHEN | & | THEN |
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.verify_image_checksum,
                          file_like_object,
                          invalid_hash)

    @mock.patch.object(requests, 'head', autospec=True)
    def test_validate_href(self, head_mock):
        href = 'http://1.2.3.4/abc.iso'
        response = head_mock.return_value
        response.status_code = http_client.OK
        utils.validate_href(href)
        head_mock.assert_called_once_with(href)
        response.status_code = http_client.NO_CONTENT
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.validate_href,
                          href)
        response.status_code = http_client.BAD_REQUEST
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.validate_href, href)

    @mock.patch.object(requests, 'head', autospec=True)
    def test_validate_href_error_code(self, head_mock):
        href = 'http://1.2.3.4/abc.iso'
        head_mock.return_value.status_code = http_client.BAD_REQUEST
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.validate_href, href)
        head_mock.assert_called_once_with(href)

    @mock.patch.object(requests, 'head', autospec=True)
    def test_validate_href_error(self, head_mock):
        href = 'http://1.2.3.4/abc.iso'
        head_mock.side_effect = requests.ConnectionError()
        self.assertRaises(exception.ImageRefValidationFailed,
                          utils.validate_href, href)
        head_mock.assert_called_once_with(href)

    def test_apply_bios_properties_filter(self):
        data = {
            "AdminName": "Administrator",
            "BootMode": "LEGACY",
            "ServerName": "Gen9 server",
            "TimeFormat": "Ist",
            "BootOrderPolicy": "RetryIndefinitely",
            "ChannelInterleaving": "Enabled",
            "CollabPowerControl": "Enabled",
            "ConsistentDevNaming": "LomsOnly",
            "CustomPostMessage": ""
        }
        filter_to_be_applied = {
            "AdminName",
            "BootMode",
            "ServerName",
            "TimeFormat",
            "CustomPostMessage"
        }

        expected = {
            "AdminName": "Administrator",
            "BootMode": "LEGACY",
            "ServerName": "Gen9 server",
            "TimeFormat": "Ist",
            "CustomPostMessage": ""
        }
        actual = utils.apply_bios_properties_filter(
            data, filter_to_be_applied)
        self.assertEqual(expected, actual)

    def test_apply_bios_properties_filter_no_filter(self):
        data = {
            "AdminName": "Administrator",
            "BootMode": "LEGACY",
            "ServerName": "Gen9 server",
            "TimeFormat": "Ist",
            "BootOrderPolicy": "RetryIndefinitely",
            "ChannelInterleaving": "Enabled",
            "CollabPowerControl": "Enabled",
            "ConsistentDevNaming": "LomsOnly",
            "CustomPostMessage": ""
        }
        filter_to_be_applied = None

        expected = {
            "AdminName": "Administrator",
            "BootMode": "LEGACY",
            "ServerName": "Gen9 server",
            "TimeFormat": "Ist",
            "BootOrderPolicy": "RetryIndefinitely",
            "ChannelInterleaving": "Enabled",
            "CollabPowerControl": "Enabled",
            "ConsistentDevNaming": "LomsOnly",
            "CustomPostMessage": ""
        }
        actual = utils.apply_bios_properties_filter(
            data, filter_to_be_applied)
        self.assertEqual(expected, actual)

    def test_apply_bios_properties_filter_no_settings(self):
        data = None
        filter_to_be_applied = {
            "AdminName",
            "BootMode",
            "ServerName",
            "TimeFormat",
            "CustomPostMessage"
        }

        expected = None
        actual = utils.apply_bios_properties_filter(
            data, filter_to_be_applied)
        self.assertEqual(expected, actual)
