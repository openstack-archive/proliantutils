# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

"""Test class for RIBCL Module."""

import mock

from proliantutils.ilo import ribcl
import constants
import unittest

from proliantutils.ilo import exception

class IloRibclTestCase(unittest.TestCase):

    def setUp(self):
        super(IloRibclTestCase, self).setUp()
        self.ilo = ribcl.RIBCLOperations("x.x.x.x", "admin", "Admin", 60, 443)

    def test__request_ilo_connection_failed(self):
        self.assertRaises(exception.IloConnectionError,
                          self.ilo.get_all_licenses)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_login_fail(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.LOGIN_FAIL_XML
        self.assertRaises(exception.IloError,
                          self.ilo.get_all_licenses)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_hold_pwr_btn(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.HOLD_PWR_BTN_XML
        result = self.ilo.hold_pwr_btn()
        self.assertIn('Host power is already OFF.', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_vm_status_none(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_VM_STATUS_XML
        result = self.ilo.get_vm_status()
        self.assertIsInstance(result, dict)
        self.assertIn('DEVICE', result)
        self.assertIn('WRITE_PROTECT', result)
        self.assertIn('VM_APPLET', result)
        self.assertIn('IMAGE_URL', result)
        self.assertIn('IMAGE_INSERTED', result)
        self.assertIn('BOOT_OPTION', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_vm_status_cdrom(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_VM_STATUS_CDROM_XML
        result = self.ilo.get_vm_status('cdrom')
        self.assertIsInstance(result, dict)
        self.assertIn('DEVICE', result)
        self.assertIn('WRITE_PROTECT', result)
        self.assertIn('VM_APPLET', result)
        self.assertIn('IMAGE_URL', result)
        self.assertIn('IMAGE_INSERTED', result)
        self.assertIn('BOOT_OPTION', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_vm_status_error(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_VM_STATUS_ERROR_XML
        self.assertRaises(
            exception.IloError, self.ilo.get_vm_status)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_all_licenses(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_ALL_LICENSES_XML
        result = self.ilo.get_all_licenses()
        self.assertIsInstance(result, dict)
        self.assertIn('LICENSE_TYPE', result)
        self.assertIn('LICENSE_INSTALL_DATE', result)
        self.assertIn('LICENSE_KEY', result)
        self.assertIn('LICENSE_CLASS', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_one_time_boot(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_ONE_TIME_BOOT_XML
        result = self.ilo.get_one_time_boot()
        self.assertIn('NORMAL', result.upper())

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_power_status(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_POWER_STATUS_XML
        result = self.ilo.get_host_power_status()
        self.assertIn('ON', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_reset_server(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.RESET_SERVER_XML
        result = self.ilo.reset_server()
        self.assertIn('server being reset', result.lower())

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_press_pwr_btn(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.PRESS_POWER_BTN_XML
        result = self.ilo.press_pwr_btn()
        self.assertIsNone(result)
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_set_host_power(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_HOST_POWER_XML
        result = self.ilo.set_host_power('ON')
        self.assertIn('Host power is already ON.', result)
        self.assertRaises(exception.IloInvalidInputError,
                          self.ilo.set_host_power, 'ErrorCase')

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_set_one_time_boot(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_ONE_TIME_BOOT_XML
        self.ilo.set_one_time_boot('NORMAL')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_insert_virtual_media(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.INSERT_VIRTUAL_MEDIA_XML
        result = self.ilo.insert_virtual_media('any_url', 'floppy')
        self.assertIsNone(result)
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_eject_virtual_media(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.EJECT_VIRTUAL_MEDIA_XML
        self.assertRaises(exception.IloError, self.ilo.eject_virtual_media)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_set_vm_status(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_VM_STATUS_XML
        self.ilo.set_vm_status('cdrom', 'boot_once', 'yes')
        self.assertTrue(request_ilo_mock.called)

if __name__ == '__main__':
    unittest.main()
