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
import time
import unittest
import os
import tempfile
import shutil

import mock
from mock import MagicMock

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo.common import FirmwareProcessor
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

    @mock.patch('proliantutils.ilo.common.os')
    def test_get_fw_processor_will_set_the_compact_fw_file_attribute(self, mock_os):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_scexe_file = 'any_file.scexe'
        def no_op():
            pass
        no_op.splitext = MagicMock(return_value=('any_file', '.scexe'))
        mock_os.path = no_op
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        fw_processor = FirmwareProcessor.get_fw_processor(any_scexe_file)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        self.assertEqual(any_scexe_file, fw_processor.compact_fw_file)

    @mock.patch('proliantutils.ilo.common._extract_scexe_file')
    def test_extract_scexe_file_gets_invoked_when_fw_processor_is_initialized_with_scexe_firmware_file(
        self, mock_extract_scexe_file):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_scexe_file = 'any_file.scexe'
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        fw_processor = FirmwareProcessor.get_fw_processor(any_scexe_file)
        fw_processor._FirmwareProcessor__do_extract('some_target_file', 'some_extract_path')
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        mock_extract_scexe_file.assert_called_once_with(fw_processor, 'some_target_file', 'some_extract_path')

    @mock.patch('proliantutils.ilo.common._extract_rpm_file')
    def test_extract_rpm_file_gets_invoked_when_fw_processor_is_initialized_with_rpm_firmware_file(
        self, mock_extract_rpm_file):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_rpm_file = 'any_file.rpm'
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        fw_processor = FirmwareProcessor.get_fw_processor(any_rpm_file)
        fw_processor._FirmwareProcessor__do_extract('some_target_file', 'some_extract_path')
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        mock_extract_rpm_file.assert_called_once_with(fw_processor, 'some_target_file', 'some_extract_path')

    def test_no_op_extract_gets_invoked_when_fw_processor_is_initialized_with_raw_firmware_file(self):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_raw_file = 'any_file.bin'
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        fw_processor = FirmwareProcessor.get_fw_processor(any_raw_file)
        return_result = fw_processor.extract(fw_processor)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        self.assertEqual(any_raw_file, return_result)

    def test_get_fw_processor_raises_exception_with_invalid_format_firmware_file(self):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_invalid_format_firmware_file = 'any_file.abc'
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        self.assertRaises(RuntimeError, FirmwareProcessor.get_fw_processor, any_invalid_format_firmware_file)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common._get_firmware_file')
    def test_extract_method_calls___do_extract_in_turn(self, mock_get_firmware_file, mock_os):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_valid_format_firmware_file = 'any_file.scexe'
        def no_op():
            pass
        no_op.splitext = MagicMock(return_value=('any_file', '.scexe'))
        no_op.basename = MagicMock()
        no_op.join = MagicMock()
        mock_os.path = no_op
        
        fw_processor = FirmwareProcessor.get_fw_processor(any_valid_format_firmware_file)
        # Now mock the __do_extract method of fw_processor instance
        mock_do_extract = MagicMock()
        fw_processor._FirmwareProcessor__do_extract = mock_do_extract
        
        expected_return_result = 'extracted_firmware_file'
        mock_get_firmware_file.return_value = expected_return_result
        
#         mock_extract_path = MagicMock()
#         mock_os_path_join.return_value = mock_extract_path
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        actual_return_result = fw_processor.extract()
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        mock_do_extract.assert_called_once_with(any_valid_format_firmware_file, mock.ANY)
        self.assertEqual(expected_return_result, actual_return_result)

    @mock.patch('proliantutils.ilo.common.utils')
    def test_extract_scexe_file_issues_command_as(self, mock_utils):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_scexe_firmware_file = 'any_file.scexe'
        any_extract_path = 'any_extract_path'
        
        mock_trycmd = MagicMock()
        mock_trycmd.return_value = ('out', 'err')
        mock_utils.trycmd = mock_trycmd
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        common._extract_scexe_file(None, any_scexe_firmware_file, any_extract_path)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        mock_trycmd.assert_called_once_with(any_scexe_firmware_file, '--unpack=' + any_extract_path)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_creates_dir_if_extract_path_doesnt_exist(self, mock_subprocess, mock_os):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'
        
        def no_op():
            pass
        no_op.exists = MagicMock(return_value=False)
        mock_os.path = no_op
        
        mock_cpio = MagicMock()
        mock_cpio.communicate = lambda: ('out', 'err')
        subsequent_popen_call_returns = [MagicMock(), mock_cpio]
        mock_subprocess.Popen = MagicMock(side_effect=subsequent_popen_call_returns)
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        common._extract_rpm_file(None, any_rpm_firmware_file, any_extract_path)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        mock_os.makedirs.assert_called_once_with(any_extract_path)

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_doesnt_create_dir_if_extract_path_already_present(self, mock_subprocess, mock_os):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'
        
        def no_op():
            pass
        no_op.exists = MagicMock(return_value=True)
        mock_os.path = no_op
        
        mock_cpio = MagicMock()
        mock_cpio.communicate = lambda: ('out', 'err')
        subsequent_popen_call_returns = [MagicMock(), mock_cpio]
        mock_subprocess.Popen = MagicMock(side_effect=subsequent_popen_call_returns)
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        common._extract_rpm_file(None, any_rpm_firmware_file, any_extract_path)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        assert not mock_os.makedirs.called

    @mock.patch('proliantutils.ilo.common.os')
    @mock.patch('proliantutils.ilo.common.subprocess')
    def test_extract_rpm_file_issues_commands_as(self, mock_subprocess, mock_os):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'
        
        def no_op():
            pass
        no_op.exists = MagicMock(return_value=True)
        mock_os.path = no_op
        
        mock_rpm2cpio = MagicMock()
        mock_cpio = MagicMock()
        mock_cpio.communicate = lambda: ('out', 'err')
        subsequent_popen_call_returns = [mock_rpm2cpio, mock_cpio]
        mock_subprocess.Popen = MagicMock(side_effect=subsequent_popen_call_returns)
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        common._extract_rpm_file(None, any_rpm_firmware_file, any_extract_path)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        popen_calls_to_assert = [mock.call.Popen('rpm2cpio ' + any_rpm_firmware_file, shell=True, stdout=mock_subprocess.PIPE), 
                                 mock.call.Popen('cpio -idm', shell=True, stdin=mock_rpm2cpio.stdout)]
        mock_subprocess.assert_has_calls(popen_calls_to_assert)

    def test_get_firmware_file(self):
        #-----------------------------------------------------------------------
        # GIVEN
        #-----------------------------------------------------------------------
        temp_dir_setup = setup_fixture_create_fw_file_extracts_for('scexe')
        #-----------------------------------------------------------------------
        # WHEN
        #-----------------------------------------------------------------------
        return_result = common._get_firmware_file(temp_dir_setup)
        #-----------------------------------------------------------------------
        # THEN
        #-----------------------------------------------------------------------
        assert return_result.endswith('.bin') == True
        teardown_fixture_create_fw_file_extracts_for(temp_dir_setup)


def teardown_fixture_create_fw_file_extracts_for(temp_dir):
    #os.removedirs(temp_dir)
    shutil.rmtree(temp_dir)


def setup_fixture_create_fw_file_extracts_for(format):
    temp_dir = tempfile.mkdtemp()
    fw_file_exts = ['_ilo', '.bin', '.xml', '.TXT', '.hpsetup', '.cpq_package.inc']
    
    if format == 'scexe':
        fw_files_dir = temp_dir
    elif format == 'rpm':
        fw_files_dir = os.path.join(temp_dir + '/please_remove_rpm_file_extracts/usr/lib/i386-linux-gnu/hp-firmware-iloX-xxxx')
    else:
        fw_files_dir = temp_dir
    
    if not os.path.exists(fw_files_dir):
        os.makedirs(fw_files_dir)

    for fw_file_ext in fw_file_exts:
        temp_firmware_file = tempfile.NamedTemporaryFile(suffix=fw_file_ext, dir=fw_files_dir, delete=False)
        #print temp_firmware_file.name

    return temp_dir
