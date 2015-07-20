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

import mock

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ribcl
from proliantutils.tests.ilo import ribcl_sample_outputs as ribcl_output


class IloCommonModuleTestCase(unittest.TestCase):

    def setUp(self):
        super(IloCommonModuleTestCase, self).setUp()
        self.ribcl = ribcl.RIBCLOperations("x.x.x.x", "admin", "Admin",
                                           60, 443)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_ribcl_ok(self, name_mock):
        name_mock.return_value = ribcl_output.GET_PRODUCT_NAME
        common.wait_for_ilo_after_reset(self.ribcl)
        name_mock.assert_called_once_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_retry(self, name_mock, sleep_mock):
        exc = exception.IloError('error')
        name_mock.side_effect = [exc, ribcl_output.GET_PRODUCT_NAME]
        common.wait_for_ilo_after_reset(self.ribcl)
        self.assertEqual(2, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_fail(self, name_mock, time_mock):
        exc = exception.IloError('error')
        name_mock.side_effect = exc
        self.assertRaises(exception.IloConnectionError,
                          common.wait_for_ilo_after_reset,
                          self.ribcl)
        self.assertEqual(common.RETRY_COUNT, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch('proliantutils.ilo.common.utils.trycmd')
    def test_extract_scexe_file_issues_command_as(self, mock_utils_trycmd):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_scexe_firmware_file = 'any_file.scexe'
        any_extract_path = 'any_extract_path'
        mock_utils_trycmd.return_value = ('out', 'err')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        common._extract_scexe_file(None,
                                   any_scexe_firmware_file,
                                   any_extract_path)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        mock_utils_trycmd.assert_called_once_with(
            any_scexe_firmware_file, '--unpack=' + any_extract_path)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_creates_dir_if_extract_path_doesnt_exist(
            self, mock_subprocess, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = False
        mock_cpio = mock.MagicMock()
        mock_cpio.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [mock.MagicMock(), mock_cpio]
        mock_subprocess.Popen = mock.MagicMock(
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

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_doesnt_create_dir_if_extract_path_present(
            self, mock_subprocess, os_mock):
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
        mock_subprocess.Popen = mock.MagicMock(
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

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_issues_commands_as(self,
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

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_raises_exception_if_it_fails(self,
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

    def test_get_firmware_file(self):
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


class FirmwareImageProcessorTestCase(unittest.TestCase):

    def setUp(self):
        # -----------------------------------------------------------------------
        # GIVEN - FOR_EACH
        # -----------------------------------------------------------------------
        def no_op():
            pass
        self.no_op = no_op
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'

    @mock.patch('proliantutils.ilo.common.os')
    def test_get_processor_will_set_the_compact_fw_file_attribute(
            self, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            self.any_scexe_file)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(self.any_scexe_file, fw_img_processor.compact_fw_file)

    @mock.patch('proliantutils.ilo.common._extract_scexe_file')
    def test_extract_scexe_file_gets_invoked_for_scexe_firmware_file(
            self, _extract_scexe_file_mock):
        # extract_scexe_file gets invoked when fw_img_processor is initialized
        # with scexe firmware file
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            self.any_scexe_file)
        fw_img_processor._FirmwareImageProcessor__do_extract(
            'some_target_file', 'some_extract_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _extract_scexe_file_mock.assert_called_once_with(
            fw_img_processor, 'some_target_file', 'some_extract_path')

    @mock.patch('proliantutils.ilo.common._extract_rpm_file')
    def test_extract_rpm_file_gets_invoked_for_rpm_firmware_file(
            self, _extract_rpm_file_mock):
        # extract_rpm_file gets invoked when fw_img_processor is initialized
        # with rpm firmware file
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            self.any_rpm_file)
        fw_img_processor._FirmwareImageProcessor__do_extract(
            'some_target_file', 'some_extract_path')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        _extract_rpm_file_mock.assert_called_once_with(
            fw_img_processor, 'some_target_file', 'some_extract_path')

    def test_no_op_extract_gets_invoked_for_raw_firmware_file(self):
        # no_op extract when fw_img_processor is initialized
        # with raw firmware file
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_raw_file = 'any_file.bin'
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            any_raw_file)
        return_result = fw_img_processor.extract()
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertEqual(any_raw_file, return_result)

    def test_get_processor_raises_exception_with_unknown_firmware_file(
            self):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        any_invalid_format_firmware_file = 'any_file.abc'
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.IloInvalidInputError,
                          common.FirmwareImageProcessor.get_processor,
                          any_invalid_format_firmware_file)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common._get_firmware_file')
    def test_extract_method_calls__do_extract_in_turn(
            self, _get_firmware_file_mock, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')

        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            self.any_scexe_file)
        # Now mock the __do_extract method of fw_img_processor instance
        __do_extract_mock = mock.MagicMock()
        fw_img_processor._FirmwareImageProcessor__do_extract = (
            __do_extract_mock)

        expected_return_result = 'extracted_firmware_file'
        _get_firmware_file_mock.return_value = expected_return_result
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        actual_return_result = fw_img_processor.extract()
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        __do_extract_mock.assert_called_once_with(self.any_scexe_file,
                                                  mock.ANY)
        self.assertEqual(expected_return_result, actual_return_result)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common._extract_scexe_file')
    @mock.patch('proliantutils.ilo.common.add_exec_permission_to')
    @mock.patch('proliantutils.ilo.common._get_firmware_file')
    def test_extract_method_raises_exception_if_raw_fw_file_not_found(
            self, _get_firmware_file_mock, add_exec_permission_to_mock,
            _extract_scexe_mock, os_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        os_mock.path.splitext.return_value = ('any_file', '.scexe')
        _get_firmware_file_mock.return_value = None
        fw_img_processor = common.FirmwareImageProcessor.get_processor(
            self.any_scexe_file)
        # -----------------------------------------------------------------------
        # WHEN & THEN
        # -----------------------------------------------------------------------
        self.assertRaises(exception.RawFirmwareFileNotFoundError,
                          fw_img_processor.extract)

    @mock.patch('proliantutils.ilo.common.add_exec_permission_to')
    @mock.patch('proliantutils.ilo.common._get_firmware_file')
    @mock.patch('proliantutils.ilo.common._extract_scexe_file')
    @mock.patch('proliantutils.ilo.common._extract_rpm_file')
    def test_successive_calls_to_extract_method(self,
                                                _extract_rpm_mock,
                                                _extract_scexe_mock,
                                                _get_firmware_file_mock,
                                                add_exec_permission_to_mock):
        """This is more of an Integration test of the extract method

        """
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        firmware_files = ['any_file.scexe', 'any_file.bin', 'any_file.rpm']
        actual_raw_fw_files = []
        expected_raw_fw_files = [
            'extracted_file_from_scexe',
            'any_file.bin',
            'extracted_file_from_rpm',
        ]
        _get_firmware_file_mock.side_effect = [
            'extracted_file_from_scexe',
            'extracted_file_from_rpm',
        ]
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        for fw_file in firmware_files:
            fw_img_processor = common.FirmwareImageProcessor.get_processor(
                fw_file)
            raw_fw_file = fw_img_processor.extract()
            actual_raw_fw_files.append(raw_fw_file)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertSequenceEqual(actual_raw_fw_files, expected_raw_fw_files)
