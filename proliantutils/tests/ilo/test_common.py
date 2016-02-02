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

import ddt
import mock

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.tests.ilo import ribcl_sample_outputs as ribcl_output


@ddt.ddt
class IloCommonModuleTestCase(unittest.TestCase):

    def setUp(self):
        # | BEFORE_EACH |
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
        # | GIVEN |
        name_mock.return_value = ribcl_output.GET_PRODUCT_NAME
        # | WHEN |
        common.wait_for_ilo_after_reset(self.ribcl)
        # | THEN |
        name_mock.assert_called_once_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_retry(self, name_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        name_mock.side_effect = [exc, ribcl_output.GET_PRODUCT_NAME]
        # | WHEN |
        common.wait_for_ilo_after_reset(self.ribcl)
        # | THEN |
        self.assertEqual(2, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_wait_for_ilo_after_reset_fail(self, name_mock, time_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        name_mock.side_effect = exc
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError,
                          common.wait_for_ilo_after_reset,
                          self.ribcl)
        self.assertEqual(10, name_mock.call_count)
        name_mock.assert_called_with()

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_ris_firmware_update_to_complete_ok(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        get_firmware_update_progress_mock.side_effect = [('PROGRESSING', 25),
                                                         ('COMPLETED', 100)]
        # | WHEN |
        common.wait_for_ris_firmware_update_to_complete(self.ris)
        # | THEN |
        self.assertEqual(2, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_ris_firmware_update_to_complete_retry_on_exception(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        get_firmware_update_progress_mock.side_effect = [('PROGRESSING', 25),
                                                         exc,
                                                         ('COMPLETED', 100)]
        # | WHEN |
        common.wait_for_ris_firmware_update_to_complete(self.ris)
        # | THEN |
        self.assertEqual(3, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_ris_firmware_update_to_complete_multiple_retries(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        get_firmware_update_progress_mock.side_effect = [('IDLE', 0),
                                                         ('PROGRESSING', 25),
                                                         ('PROGRESSING', 50),
                                                         ('PROGRESSING', 75),
                                                         ('ERROR', 0)]
        # | WHEN |
        common.wait_for_ris_firmware_update_to_complete(self.ris)
        #  | THEN |
        self.assertEqual(5, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress')
    def test_wait_for_ris_firmware_update_to_complete_fail(
            self, get_firmware_update_progress_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        get_firmware_update_progress_mock.side_effect = exc
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError,
                          common.wait_for_ris_firmware_update_to_complete,
                          self.ris)
        self.assertEqual(10, get_firmware_update_progress_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_ribcl_firmware_update_to_complete_retries_till_exception(
            self, get_product_name_mock, sleep_mock):
        # | GIVEN |
        exc = exception.IloError('error')
        get_product_name_mock.side_effect = ['Rap metal',
                                             'Death metal',
                                             exc]
        # | WHEN |
        common.wait_for_ribcl_firmware_update_to_complete(self.ribcl)
        # | THEN |
        self.assertEqual(3, get_product_name_mock.call_count)

    @mock.patch.object(time, 'sleep')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(common, 'wait_for_ilo_after_reset', lambda x: None)
    def test_wait_for_ribcl_firmware_update_silent_if_reset_exc_not_captured(
            self, get_product_name_mock, sleep_mock):
        # | GIVEN |
        get_product_name_mock.side_effect = [
            'Rap metal', 'Death metal', 'Black metal', 'Extreme metal',
            'Folk metal', 'Gothic metal', 'Power metal', 'War metal',
            'Thrash metal', 'Groove metal']
        # | WHEN |
        common.wait_for_ribcl_firmware_update_to_complete(self.ribcl)
        # | THEN |
        self.assertEqual(10, get_product_name_mock.call_count)

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
        # | WHEN |
        actual_file_name, actual_file_ext = (
            common.get_filename_and_extension_of(input_file_path))
        # | THEN |
        self.assertEqual(actual_file_name, expected_file_name)
        self.assertEqual(actual_file_ext, expected_file_ext)

    @mock.patch.object(common, 'os', autospec=True)
    @mock.patch.object(common, 'stat', autospec=True)
    def test_add_exec_permission_to(self, stat_mock, os_mock):
        # | GIVEN |
        any_file = 'any_file'
        # | WHEN |
        common.add_exec_permission_to(any_file)
        # | THEN |
        os_mock.stat.assert_called_once_with(any_file)
        os_mock.chmod.assert_called_once_with(
            any_file, os_mock.stat().st_mode | stat_mock.S_IXUSR)

    def test_get_major_minor_lt_suggested_min(self):
        ver_str = "iLO 4 v2.05"
        actual = "2.05"
        expected = common.get_major_minor(ver_str)
        self.assertEqual(actual, expected)

    def test_get_major_minor_eq_suggested_min(self):
        ver_str = "iLO 4 v2.30"
        actual = "2.30"
        expected = common.get_major_minor(ver_str)
        self.assertEqual(actual, expected)

    def test_get_major_minor_gt_suggested_min(self):
        ver_str = "iLO 4 v2.5"
        actual = "2.5"
        expected = common.get_major_minor(ver_str)
        self.assertEqual(actual, expected)

    def test_get_major_minor_unexpected(self):
        ver_str = "iLO 4 v"
        actual = None
        expected = common.get_major_minor(ver_str)
        self.assertEqual(actual, expected)

    @ddt.data((ribcl.RIBCLOperations.SUPPORTED_BOOT_MODE.LEGACY_BIOS_ONLY,
               {'boot_mode_bios': True, 'boot_mode_uefi': False}),
              (ribcl.RIBCLOperations.SUPPORTED_BOOT_MODE.UEFI_ONLY,
               {'boot_mode_bios': False, 'boot_mode_uefi': True}),
              (ribcl.RIBCLOperations.SUPPORTED_BOOT_MODE.LEGACY_BIOS_AND_UEFI,
               {'boot_mode_bios': True, 'boot_mode_uefi': True}))
    @ddt.unpack
    @mock.patch.object(ribcl.RIBCLOperations, 'get_supported_boot_mode',
                       autospec=True)
    def test_get_server_supported_boot_modes_for_ribcl_object(
            self, returned_boot_mode_value, expected_boot_modes,
            get_supported_boot_mode_mock):
        # | GIVEN |
        the_operation_object = self.ribcl
        get_supported_boot_mode_mock.return_value = returned_boot_mode_value
        # | WHEN |
        actual_boot_modes = (
            common.get_server_supported_boot_modes(the_operation_object))
        # | THEN |
        self.assertDictEqual(expected_boot_modes, actual_boot_modes)

    @ddt.data((ris.RISOperations.SUPPORTED_BOOT_MODE.LEGACY_BIOS_ONLY,
               {'boot_mode_bios': True, 'boot_mode_uefi': False}),
              (ris.RISOperations.SUPPORTED_BOOT_MODE.UEFI_ONLY,
               {'boot_mode_bios': False, 'boot_mode_uefi': True}),
              (ris.RISOperations.SUPPORTED_BOOT_MODE.LEGACY_BIOS_AND_UEFI,
               {'boot_mode_bios': True, 'boot_mode_uefi': True}))
    @ddt.unpack
    @mock.patch.object(ris.RISOperations, 'get_supported_boot_mode',
                       autospec=True)
    def test_get_server_supported_boot_modes_for_ris_object(
            self, returned_boot_mode_value, expected_boot_modes,
            get_supported_boot_mode_mock):
        # | GIVEN |
        the_operation_object = self.ris
        get_supported_boot_mode_mock.return_value = returned_boot_mode_value
        # | WHEN |
        actual_boot_modes = (
            common.get_server_supported_boot_modes(the_operation_object))
        # | THEN |
        self.assertDictEqual(expected_boot_modes, actual_boot_modes)
