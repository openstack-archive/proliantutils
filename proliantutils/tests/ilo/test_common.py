# Copyright 2015 Hewlett-Packard Development Company, L.P.
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
"""Test Class for Common Operations."""
import os
import shutil
import tempfile
import time
import unittest

import ddt
import mock
from six.moves import builtins as __builtin__

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.tests.ilo import ribcl_sample_outputs as ribcl_output


@ddt.ddt
class IloCommonModuleTestCase(unittest.TestCase):

    def setUp(self):
        # -----------------------------------------------------------------------
        # GIVEN - FOR_EACH
        # -----------------------------------------------------------------------
        super(IloCommonModuleTestCase, self).setUp()
        self.ribcl = ribcl.RIBCLOperations("x.x.x.x", "admin", "Admin",
                                           60, 443)
        self.ris = ris.RISOperations("x.x.x.x", "admin", "Admin",
                                     60, 443)
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'

    @mock.patch.object(time, 'sleep', lambda x: None)
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_ribcl_ok(self, name_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        name_mock.return_value = ribcl_output.GET_PRODUCT_NAME
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common.wait_for_ilo_after_reset(self.ribcl)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        name_mock.assert_called_once_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_retry(self, name_mock, sleep_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        exc = exception.IloError('error')
        name_mock.side_effect = [exc, ribcl_output.GET_PRODUCT_NAME]
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common.wait_for_ilo_after_reset(self.ribcl)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(2, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_fail(self, name_mock, time_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        exc = exception.IloError('error')
        name_mock.side_effect = exc
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloError,
                          common.wait_for_ilo_after_reset,
                          self.ribcl)
        self.assertEqual(10, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    def test_wait_for_firmware_update_to_complete_ok(
            self, get_firmware_update_progress_mock, sleep_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        get_firmware_update_progress_mock.return_value = ('COMPLETED', 100)
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common.wait_for_firmware_update_to_complete(self.ris)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        get_firmware_update_progress_mock.assert_called_once_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    def test_wait_for_firmware_update_to_complete_retry(
            self, get_firmware_update_progress_mock, sleep_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        exc = exception.IloError('error')
        get_firmware_update_progress_mock.side_effect = [exc,
                                                         ('COMPLETED', 100)]
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common.wait_for_firmware_update_to_complete(self.ris)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(2, get_firmware_update_progress_mock.call_count)
        get_firmware_update_progress_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    def test_wait_for_firmware_update_to_complete_fail(
            self, get_firmware_update_progress_mock, sleep_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        get_firmware_update_progress_mock.return_value = ('IDLE', 100)
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloError,
                          common.wait_for_firmware_update_to_complete,
                          self.ris)
        self.assertEqual(10, get_firmware_update_progress_mock.call_count)
        get_firmware_update_progress_mock.assert_called_with()

    @ddt.data(('/path/to/file.scexe', 'file', '.scexe'),
              ('/path/to/.hidden', '.hidden', ''),
              ('filename', 'filename', ''),
              ('filename.txt.bk', 'filename.txt', '.bk'),
              ('//filename.txt', 'filename', '.txt'),
              ('.filename.txt.bk', '.filename.txt', '.bk'),
              ('/', '', ''),
              ('.', '.', ''),)
    @ddt.unpack
    def test_get_filename_and_extension_of(
            self, input_file_path, expected_file_name, expected_file_ext):
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        actual_file_name, actual_file_ext = (
            common.get_filename_and_extension_of(input_file_path))
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(actual_file_name, expected_file_name)
        self.assertEqual(actual_file_ext, expected_file_ext)

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'stat', autospec=True)
    def test_add_exec_permission_to(self, stat_mock, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_file = 'any_file'
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common.add_exec_permission_to(any_file)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        os_mock.stat.assert_called_once_with(any_file)
        os_mock.chmod.assert_called_once_with(
            any_file, os_mock.stat().st_mode | stat_mock.S_IXUSR)

    # @mock.patch.object(common, 'os', autospec=True)
    def test_get_fw_extractor_will_set_the_fw_file_attribute(self):
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_extractor = common.get_fw_extractor(self.any_scexe_file)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(self.any_scexe_file, fw_img_extractor.fw_file)

    @mock.patch.object(common, '_extract_scexe_file', autospec=True)
    def test__extract_scexe_file_gets_invoked_for_scexe_firmware_file(
            self, _extract_scexe_file_mock):
        # _extract_scexe_file gets invoked when fw_img_extractor is initialized
        # with scexe firmware file
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_extractor = common.get_fw_extractor(self.any_scexe_file)
        fw_img_extractor._do_extract('some_target_file', 'some_extract_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _extract_scexe_file_mock.assert_called_once_with(
            fw_img_extractor, 'some_target_file', 'some_extract_path')

    @mock.patch.object(common, '_extract_rpm_file', autospec=True)
    def test__extract_rpm_file_gets_invoked_for_rpm_firmware_file(
            self, _extract_rpm_file_mock):
        # _extract_rpm_file gets invoked when fw_img_extractor is initialized
        # with rpm firmware file
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_extractor = common.get_fw_extractor(self.any_rpm_file)
        fw_img_extractor._do_extract('some_target_file', 'some_extract_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _extract_rpm_file_mock.assert_called_once_with(
            fw_img_extractor, 'some_target_file', 'some_extract_path')

    def test_no_op_extract_gets_invoked_for_raw_firmware_file(self):
        # no_op extract when fw_img_extractor is initialized
        # with raw firmware file
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_raw_file = 'any_file.bin'
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_extractor = common.get_fw_extractor(any_raw_file)
        return_result = fw_img_extractor.extract()
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(any_raw_file, return_result)

    def test_get_fw_extractor_raises_exception_with_unknown_firmware_file(
            self):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_invalid_format_firmware_file = 'any_file.abc'
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloInvalidInputError,
                          common.get_fw_extractor,
                          any_invalid_format_firmware_file)

    @mock.patch.object(common.utils, 'trycmd', autospec=True)
    def test__extract_scexe_file_issues_command_as(self, utils_trycmd_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_scexe_firmware_file = 'any_file.scexe'
        any_extract_path = 'any_extract_path'
        utils_trycmd_mock.return_value = ('out', 'err')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common._extract_scexe_file(None,
                                   any_scexe_firmware_file,
                                   any_extract_path)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        utils_trycmd_mock.assert_called_once_with(
            any_scexe_firmware_file, '--unpack=' + any_extract_path)

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'subprocess', autospec=True)
    def test__extract_rpm_file_creates_dir_if_extract_path_doesnt_exist(
            self, subprocess_mock, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = False
        mock_cpio = mock.MagicMock()
        mock_cpio.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [mock.MagicMock(), mock_cpio]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common._extract_rpm_file(None,
                                 any_rpm_firmware_file,
                                 any_extract_path)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        os_mock.makedirs.assert_called_once_with(any_extract_path)

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'subprocess', autospec=True)
    def test__extract_rpm_file_doesnt_create_dir_if_extract_path_present(
            self, subprocess_mock, os_mock):
        # extract_rpm_file doesn't create dir if extract path
        # is already present
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = True
        mock_cpio = mock.MagicMock()
        mock_cpio.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [mock.MagicMock(), mock_cpio]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common._extract_rpm_file(None,
                                 any_rpm_firmware_file,
                                 any_extract_path)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertFalse(os_mock.makedirs.called)

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'subprocess', autospec=True)
    def test__extract_rpm_file_issues_commands_as(self,
                                                  subprocess_mock,
                                                  os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = True
        rpm2cpio_mock = mock.MagicMock()
        cpio_mock = mock.MagicMock()
        cpio_mock.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [rpm2cpio_mock, cpio_mock]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common._extract_rpm_file(None,
                                 any_rpm_firmware_file,
                                 any_extract_path)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        popen_calls_to_assert = [
            mock.call.Popen('rpm2cpio ' + any_rpm_firmware_file,
                            shell=True,
                            stdout=subprocess_mock.PIPE),
            mock.call.Popen('cpio -idm',
                            shell=True,
                            stdin=rpm2cpio_mock.stdout),
        ]
        subprocess_mock.assert_has_calls(popen_calls_to_assert)
        cpio_mock.communicate.assert_called_once_with()

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'subprocess', autospec=True)
    def test__extract_rpm_file_raises_exception_if_it_fails(self,
                                                            subprocess_mock,
                                                            os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        rpm2cpio_mock = mock.MagicMock()
        cpio_mock = mock.MagicMock()
        cpio_mock.communicate.side_effect = Exception('foo')
        subsequent_popen_call_returns = [rpm2cpio_mock, cpio_mock]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloError, common._extract_rpm_file,
                          None, any_rpm_firmware_file, any_extract_path)

    def test__get_firmware_file(self):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        temp_dir_setup = setup_fixture_create_fw_file_extracts_for('scexe')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        return_result = common._get_firmware_file(temp_dir_setup)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertTrue(return_result.endswith('.bin'))
        teardown_fixture_create_fw_file_extracts_for(temp_dir_setup)

    @mock.patch.object(common, '_get_firmware_file', autospec=True)
    @mock.patch.object(common, 'get_filename_and_extension_of', autospec=True)
    @mock.patch.object(common, 'tempfile', autospec=True)
    @mock.patch.object(common.uuid, 'uuid4', autospec=True)
    @mock.patch.object(common.os, 'link', autospec=True)
    def test__get_firmware_file_in_new_path(
            self, os_link_mock, uuid4_mock, tempfile_mock,
            get_filename_and_extension_of_mock, _get_firmware_file_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        _get_firmware_file_mock.return_value = 'some_raw_fw_file.bin'
        get_filename_and_extension_of_mock.return_value = ('some_raw_fw_file',
                                                           '.bin')
        tempfile_mock.gettempdir.return_value = '/tmp'
        uuid4_mock.return_value = 12345
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        new_fw_file_path = common._get_firmware_file_in_new_path('any_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _get_firmware_file_mock.assert_called_once_with('any_path')
        # tests the hard linking of the raw fw file so found
        os_link_mock.assert_called_once_with(
            'some_raw_fw_file.bin', '/tmp/12345_some_raw_fw_file.bin')
        self.assertEqual(new_fw_file_path, '/tmp/12345_some_raw_fw_file.bin')

    @mock.patch.object(common, '_get_firmware_file', autospec=True)
    def test__get_firmware_file_in_new_path_returns_none_for_file_not_found(
            self, _get_firmware_file_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        _get_firmware_file_mock.return_value = None
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        actual_result = common._get_firmware_file_in_new_path('any_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertIsNone(actual_result)


def teardown_fixture_create_fw_file_extracts_for(temp_dir):
    # os.removedirs(temp_dir)
    shutil.rmtree(temp_dir)


def setup_fixture_create_fw_file_extracts_for(format):
    temp_dir = tempfile.mkdtemp()
    fw_file_exts = [
        '_ilo', '.bin', '.xml', '.TXT', '.hpsetup', '.cpq_package.inc'
    ]

    if format == 'scexe':
        fw_files_dir = temp_dir
    elif format == 'rpm':
        fw_files_dir = os.path.join(
            temp_dir +
            '/please_remove_rpm_file_extracts/usr/lib/i386-linux-gnu/' +
            'hp-firmware-iloX-xxxx'
        )
    else:
        fw_files_dir = temp_dir

    if not os.path.exists(fw_files_dir):
        os.makedirs(fw_files_dir)

    for fw_file_ext in fw_file_exts:
        tempfile.NamedTemporaryFile(suffix=fw_file_ext,
                                    dir=fw_files_dir,
                                    delete=False)

    return temp_dir


@ddt.ddt
class FirmwareImageProcessorTestCase(unittest.TestCase):

    def setUp(self):
        # -----------------------------------------------------------------------
        # GIVEN - FOR_EACH
        # -----------------------------------------------------------------------
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(common, 'tempfile', autospec=True)
    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, '_get_firmware_file_in_new_path', autospec=True)
    @mock.patch.object(common, 'shutil', autospec=True)
    def test_extract_method_calls__do_extract_in_turn(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            os_mock, tempfile_mock, add_exec_permission_to_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')

        fw_img_extractor = common.get_fw_extractor(self.any_scexe_file)
        # Now mock the _do_extract method of fw_img_extractor instance
        _do_extract_mock = mock.MagicMock()
        fw_img_extractor._do_extract = _do_extract_mock

        expected_return_result = 'extracted_firmware_file'
        _get_firmware_file_in_new_path_mock.return_value = (
            expected_return_result)
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        actual_return_result = fw_img_extractor.extract()
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _do_extract_mock.assert_called_once_with(self.any_scexe_file, mock.ANY)
        self.assertEqual(expected_return_result, actual_return_result)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(common, 'tempfile', autospec=True)
    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, '_get_firmware_file_in_new_path', autospec=True)
    @mock.patch.object(common, 'shutil', autospec=True)
    def test_extract_deletes_temp_extracted_folder_before_raising_exception(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            os_mock, tempfile_mock, add_exec_permission_to_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')

        fw_img_extractor = common.get_fw_extractor(self.any_scexe_file)
        # Now mock the _do_extract method of fw_img_extractor instance
        _do_extract_mock = mock.MagicMock(side_effect=exception.IloError('!'))
        fw_img_extractor._do_extract = _do_extract_mock
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloError,
                          fw_img_extractor.extract)
        shutil_mock.rmtree.assert_called_once_with(
            tempfile_mock.mkdtemp.return_value, ignore_errors=True)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(common, 'tempfile', autospec=True)
    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, '_extract_scexe_file', autospec=True)
    @mock.patch.object(common, '_get_firmware_file_in_new_path', autospec=True)
    @mock.patch.object(common, 'shutil', autospec=True)
    def test_extract_method_raises_exception_if_raw_fw_file_not_found(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            _extract_scexe_mock, os_mock, tempfile_mock,
            add_exec_permission_to_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')
        _get_firmware_file_in_new_path_mock.return_value = None
        fw_img_extractor = common.get_fw_extractor(self.any_scexe_file)
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloInvalidInputError,
                          fw_img_extractor.extract)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(common, 'tempfile', autospec=True)
    @mock.patch.object(common, '_extract_scexe_file', autospec=True)
    @mock.patch.object(common, '_extract_rpm_file', autospec=True)
    # don't use autospec=True here(below one), setting side_effect
    # causes issue. refer https://bugs.python.org/issue17826
    @mock.patch.object(common, '_get_firmware_file_in_new_path')
    @mock.patch.object(common, 'shutil', autospec=True)
    def test_successive_calls_to_extract_method(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            _extract_rpm_mock, _extract_scexe_mock, tempfile_mock,
            add_exec_permission_to_mock):
        """This is more of an integration test of the extract method

        """
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        firmware_files = [
            self.any_scexe_file,
            'any_file.bin',
            self.any_rpm_file,
        ]
        actual_raw_fw_files = []
        expected_raw_fw_files = [
            'extracted_file_from_scexe',
            'any_file.bin',
            'extracted_file_from_rpm',
        ]
        _get_firmware_file_in_new_path_mock.side_effect = [
            'extracted_file_from_scexe',
            'extracted_file_from_rpm',
        ]
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        for fw_file in firmware_files:
            fw_img_extractor = common.get_fw_extractor(fw_file)
            raw_fw_file = fw_img_extractor.extract()
            actual_raw_fw_files.append(raw_fw_file)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertSequenceEqual(actual_raw_fw_files, expected_raw_fw_files)

    @mock.patch.object(
        common.FirmwareImageProcessor, '_get_socket', autospec=True)
    @mock.patch.object(common, 'socket')
    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_upload_file_to_returns_cookie_after_successful_upload(
            self, open_mock, socket_mock, _get_socket_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        sock_mock = _get_socket_mock.return_value
        sock_mock.read.side_effect = [b'data returned from socket with ',
                                      b'Set-Cookie: blah_blah_cookie',
                                      b'']
        fw_img_processor = common.FirmwareImageProcessor('any_raw_file')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        cookie = fw_img_processor.upload_file_to(('host', 'port'), 60)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual('blah_blah_cookie', cookie)

    @mock.patch.object(
        common.FirmwareImageProcessor, '_get_socket', autospec=True)
    @mock.patch.object(common, 'socket')
    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_upload_file_to_throws_exception_when_cookie_not_returned(
            self, open_mock, socket_mock, _get_socket_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        sock_mock = _get_socket_mock.return_value
        sock_mock.read.side_effect = [b'data returned from socket with ',
                                      b'No-Cookie',
                                      b'']
        fw_img_processor = common.FirmwareImageProcessor('any_raw_file')
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloError, fw_img_processor.upload_file_to,
                          ('host', 'port'), 60)

    @mock.patch.object(common, 'socket')
    @mock.patch.object(common, 'ssl')
    def test__get_socket_returns_ssl_wrapped_socket_if_all_goes_well(
            self, ssl_mock, socket_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        socket_mock.getaddrinfo().__iter__.return_value = [
            # (family, socktype, proto, canonname, sockaddr),
            (10, 1, 6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
            (2, 1, 6, '', ('0.0.0.0-some-address', 80)),
        ]
        fw_img_processor = common.FirmwareImageProcessor('any_raw_file')
        fw_img_processor.hostname = 'host'
        fw_img_processor.port = 443
        fw_img_processor.timeout = 'timeout'
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        returned_sock = fw_img_processor._get_socket()
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        socket_mock.socket.assert_has_calls([
            mock.call(10, 1, 6),
            mock.call().settimeout('timeout'),
            mock.call().connect(
                ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),

            mock.call(2, 1, 6),
            mock.call().settimeout('timeout'),
            mock.call().connect(('0.0.0.0-some-address', 80)),
        ])
        self.assertTrue(ssl_mock.wrap_socket.called)
        self.assertEqual(returned_sock, ssl_mock.wrap_socket())

    @ddt.data(('foo.bar.com', exception.IloConnectionError),
              ('1.1.1.1', exception.IloConnectionError),
              ('any_kind_of_address', exception.IloConnectionError),)
    @ddt.unpack
    def test__get_socket_throws_exception_in_case_of_failed_connection(
            self, input_hostname, expected_exception_type):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        fw_img_processor = common.FirmwareImageProcessor('any_raw_file')
        # fw_img_processor.hostname = 'foo.bar.com'
        fw_img_processor.hostname = input_hostname
        fw_img_processor.port = 443
        fw_img_processor.timeout = 1
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(
            expected_exception_type, fw_img_processor._get_socket)
