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

"""Test class for RIS Module."""

import unittest

import mock
import ris_sample_outputs as ris_constants

from proliantutils import exception
from proliantutils.ilo import ris


class IloRisTestCase(unittest.TestCase):

    def setUp(self):
        super(IloRisTestCase, self).setUp()
        self.ilo = ris.RISOperations("x.x.x.x", "Administrator", "admin", None)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_get_http_boot_url_uefi(self, _validate_uefi_boot_mode_mock,
                                    get_bios_settings_mock):
        get_bios_settings_mock.return_value = ris_constants.HTTP_BOOT_URL
        _validate_uefi_boot_mode_mock.return_value = True
        result = self.ilo.get_http_boot_url()
        _validate_uefi_boot_mode_mock.assert_called_once_with()
        self.assertEqual(
            'http://10.10.1.30:8081/startup.nsh', result['UefiShellStartupUrl']
            )

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_set_http_boot_url_uefi(self, _validate_uefi_boot_mode_mock,
                                    change_bios_setting_mock):
        _validate_uefi_boot_mode_mock.return_value = True
        self.ilo.set_http_boot_url('http://10.10.1.30:8081/startup.nsh')
        _validate_uefi_boot_mode_mock.assert_called_once_with()
        change_bios_setting_mock.assert_called_once_with({
            "UefiShellStartupUrl": "http://10.10.1.30:8081/startup.nsh"
            })

    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_get_http_boot_url_bios(self, _validate_uefi_boot_mode_mock):
        _validate_uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.ilo.get_http_boot_url)

    @mock.patch.object(ris.RISOperations, '_validate_uefi_boot_mode')
    def test_set_http_boot_url_bios(self, _validate_uefi_boot_mode_mock):
        _validate_uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.ilo.set_http_boot_url,
                          'http://10.10.1.30:8081/startup.nsh')

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__validate_uefi_boot_mode_uefi(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'UEFI'
        result = self.ilo._validate_uefi_boot_mode()
        self.assertTrue(result)

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__validate_uefi_boot_mode_bios(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'LEGACY'
        result = self.ilo._validate_uefi_boot_mode()
        self.assertFalse(result)
