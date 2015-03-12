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

import unittest

import constants
import mock

from proliantutils import exception
from proliantutils.ilo import ribcl


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

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_pending_boot_mode_feature_not_supported(self,
                                                         request_ilo_mock):
        request_ilo_mock.side_effect = [constants.BOOT_MODE_NOT_SUPPORTED,
                                        constants.GET_PRODUCT_NAME]
        try:
            self.ilo.get_pending_boot_mode()
        except exception.IloCommandNotSupportedError as e:
            self.assertIn('ProLiant DL380 G7', str(e))

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_reset_ilo(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.RESET_ILO_XML
        self.ilo.reset_ilo()
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_reset_ilo_credential(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.RESET_ILO_CREDENTIAL_XML
        self.ilo.reset_ilo_credential("fakepassword")
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_reset_ilo_credential_fail(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.RESET_ILO_CREDENTIAL_FAIL_XML
        self.assertRaises(exception.IloError,
                          self.ilo.reset_ilo_credential, "fake")
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_persistent_boot_device_hdd_uefi(self, request_ilo_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_HDD_UEFI_XML
        request_ilo_mock.return_value = xml
        result = self.ilo.get_persistent_boot_device()
        self.assertEqual(result, 'HDD')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_persistent_boot_device_nic_uefi(self, request_ilo_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_NIC_UEFI_XML
        request_ilo_mock.return_value = xml
        result = self.ilo.get_persistent_boot_device()
        self.assertEqual(result, 'NETWORK')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_persistent_boot_device_cdrom_uefi(self, request_ilo_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_CDROM_UEFI_XML
        request_ilo_mock.return_value = xml
        result = self.ilo.get_persistent_boot_device()
        self.assertEqual(result, 'CDROM')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_persistent_boot_device_bios(self, request_ilo_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_BIOS_XML
        request_ilo_mock.return_value = xml
        result = self.ilo.get_persistent_boot_device()
        self.assertEqual(result, 'CDROM')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, 'set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_cdrom(self,
                                               request_ilo_mock,
                                               set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_NIC_UEFI_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["CDROM"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['Boot000B'])

    @mock.patch.object(ribcl.RIBCLOperations, 'set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_hdd(self,
                                             request_ilo_mock,
                                             set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_CDROM_UEFI_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["HDD"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['Boot0007'])

    @mock.patch.object(ribcl.RIBCLOperations, 'set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_nic(self,
                                             request_ilo_mock,
                                             set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_CDROM_UEFI_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["NETWORK"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['Boot0009',
                                                       'Boot0008'])

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_missing_cdrom(self,
                                                       request_ilo_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_CDROM_MISSING_UEFI_XML
        prod_name = constants.GET_PRODUCT_NAME
        request_ilo_mock.side_effect = [xml, prod_name]
        with self.assertRaises(exception.IloInvalidInputError) as cm:
            self.ilo.update_persistent_boot(['CDROM'])
        exp = cm.exception
        self.assertIn('ProLiant DL380 G7', str(exp))

    def test_update_persistent_boot_other(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.ilo.update_persistent_boot, ['Other'])

    @mock.patch.object(ribcl.RIBCLOperations, 'set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_bios(self,
                                         request_ilo_mock,
                                         set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_BIOS_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["CDROM"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['CDROM'])

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_health_data(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_HEALTH_DATA
        result = self.ilo.get_host_health_data()
        self.assertIn('GET_EMBEDDED_HEALTH_DATA', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_health_present_power_reading(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_HEALTH_DATA
        for i in (None, self.ilo.get_host_health_data(), "Bad Input"):
            result = self.ilo.get_host_health_present_power_reading(i)
            self.assertIn('37 Watts', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_health_power_supplies(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_HEALTH_DATA
        for i in (None, self.ilo.get_host_health_data(), "Bad Input"):
            result = self.ilo.get_host_health_power_supplies()
            self.assertIsInstance(result, list)
            for power in result:
                self.assertIn('STATUS', power)
                self.assertIn('LABEL', power)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_temperature_sensors(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_HEALTH_DATA
        for i in (None, self.ilo.get_host_health_data(), "Bad Input"):
            result = self.ilo.get_host_health_temperature_sensors()
            self.assertIsInstance(result, list)
            for temp in result:
                self.assertIn('STATUS', temp)
                self.assertIn('CURRENTREADING', temp)
                self.assertIn('CRITICAL', temp)
                self.assertIn('CAUTION', temp)
                self.assertIn('LOCATION', temp)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_fan_sensors(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_HEALTH_DATA
        for i in (None, self.ilo.get_host_health_data(), "Bad Input"):
            result = self.ilo.get_host_health_fan_sensors()
            self.assertIsInstance(result, list)
            for fan in result:
                self.assertIn('STATUS', fan)
                self.assertIn('SPEED', fan)
                self.assertIn('ZONE', fan)
                self.assertIn('LABEL', fan)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_get_host_power_readings(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_POWER_READINGS
        for i in (None, self.ilo.get_host_health_data(), "Bad Input"):
            result = self.ilo.get_host_power_readings()
            self.assertIn('PRESENT_POWER_READING', result)
            self.assertIn('MAXIMUM_POWER_READING', result)
            self.assertIn('MINIMUM_POWER_READING', result)
            self.assertIn('AVERAGE_POWER_READING', result)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_host')
    def test_get_host_uuid(self, request_host_mock):
        request_host_mock.return_value = constants.GET_HOST_UUID
        name, uuid = self.ilo.get_host_uuid()
        self.assertIn('ProLiant ML110 G7', name)
        self.assertIn('37363536-3636-4D32-3232-303130324A41', uuid)


class IloRibclTestCaseBeforeRisSupport(unittest.TestCase):

    def setUp(self):
        super(IloRibclTestCaseBeforeRisSupport, self).setUp()
        self.ilo = ribcl.IloClient("x.x.x.x", "admin", "Admin", 60, 443)

    def test__request_ilo_connection_failed(self):
        self.assertRaises(ribcl.IloConnectionError,
                          self.ilo.get_all_licenses)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_login_fail(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.LOGIN_FAIL_XML
        self.assertRaises(ribcl.IloError,
                          self.ilo.get_all_licenses)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_hold_pwr_btn(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.HOLD_PWR_BTN_XML
        result = self.ilo.hold_pwr_btn()
        self.assertIn('Host power is already OFF.', result)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
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

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
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

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_get_vm_status_error(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_VM_STATUS_ERROR_XML
        self.assertRaises(
            ribcl.IloError, self.ilo.get_vm_status)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_get_all_licenses(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_ALL_LICENSES_XML
        result = self.ilo.get_all_licenses()
        self.assertIsInstance(result, dict)
        self.assertIn('LICENSE_TYPE', result)
        self.assertIn('LICENSE_INSTALL_DATE', result)
        self.assertIn('LICENSE_KEY', result)
        self.assertIn('LICENSE_CLASS', result)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_get_one_time_boot(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_ONE_TIME_BOOT_XML
        result = self.ilo.get_one_time_boot()
        self.assertIn('NORMAL', result.upper())

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_get_host_power_status(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.GET_HOST_POWER_STATUS_XML
        result = self.ilo.get_host_power_status()
        self.assertIn('ON', result)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_reset_server(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.RESET_SERVER_XML
        result = self.ilo.reset_server()
        self.assertIn('server being reset', result.lower())

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_press_pwr_btn(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.PRESS_POWER_BTN_XML
        result = self.ilo.press_pwr_btn()
        self.assertIsNone(result)
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_set_host_power(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_HOST_POWER_XML
        result = self.ilo.set_host_power('ON')
        self.assertIn('Host power is already ON.', result)
        self.assertRaises(ribcl.IloInvalidInputError,
                          self.ilo.set_host_power, 'ErrorCase')

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_set_one_time_boot(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_ONE_TIME_BOOT_XML
        self.ilo.set_one_time_boot('NORMAL')
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_insert_virtual_media(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.INSERT_VIRTUAL_MEDIA_XML
        result = self.ilo.insert_virtual_media('any_url', 'floppy')
        self.assertIsNone(result)
        self.assertTrue(request_ilo_mock.called)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_eject_virtual_media(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.EJECT_VIRTUAL_MEDIA_XML
        self.assertRaises(ribcl.IloError, self.ilo.eject_virtual_media)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_set_vm_status(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_VM_STATUS_XML
        self.ilo.set_vm_status('cdrom', 'boot_once', 'yes')
        self.assertTrue(request_ilo_mock.called)


if __name__ == '__main__':
    unittest.main()
