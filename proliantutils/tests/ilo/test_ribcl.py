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

import json
import re
import unittest
import xml.etree.ElementTree as ET

import ddt
import mock
import requests
from requests.packages import urllib3
from requests.packages.urllib3 import exceptions as urllib3_exceptions

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import constants as cons
from proliantutils.ilo import ribcl
from proliantutils.tests.ilo import ribcl_sample_outputs as constants


class MaskedRequestDataTestCase(unittest.TestCase):

    def setUp(self):
        super(MaskedRequestDataTestCase, self).setUp()
        self.maskedRequestData = ribcl.MaskedRequestData({})

    def test___str__with_user_credential_present(self):
        xml_data = (
            '<RIBCL VERSION="2.0">'
            '<LOGIN PASSWORD="password" USER_LOGIN="admin">'
            '<RIB_INFO MODE="read">')
        masked_xml_data = (
            '\'<RIBCL VERSION="2.0">'
            '<LOGIN PASSWORD="*****" USER_LOGIN="*****">'
            '<RIB_INFO MODE="read">\'')
        self.maskedRequestData.request_data = {'headers': 'some-headers',
                                               'data': xml_data,
                                               'verify': False}
        self.assertIn(masked_xml_data, str(self.maskedRequestData))

    def test___str__with_user_credential_not_present(self):
        xml_data = (
            '<RIBCL VERSION="2.0">'
            '<RIB_INFO MODE="read">')
        self.maskedRequestData.request_data = {'headers': 'some-headers',
                                               'data': xml_data,
                                               'verify': True}
        self.assertIn(xml_data, str(self.maskedRequestData))


@mock.patch.object(ribcl.RIBCLOperations, 'get_product_name',
                   lambda x: 'ProLiant DL580 Gen8')
class IloRibclTestCaseInitTestCase(unittest.TestCase):

    @mock.patch.object(urllib3, 'disable_warnings')
    def test_init(self, disable_warning_mock):
        ribcl_client = ribcl.RIBCLOperations(
            "x.x.x.x", "admin", "Admin", 60, 443, cacert='/somepath')

        self.assertEqual(ribcl_client.host, "x.x.x.x")
        self.assertEqual(ribcl_client.login, "admin")
        self.assertEqual(ribcl_client.password, "Admin")
        self.assertEqual(ribcl_client.timeout, 60)
        self.assertEqual(ribcl_client.port, 443)
        self.assertEqual(ribcl_client.cacert, '/somepath')

    @mock.patch.object(urllib3, 'disable_warnings')
    def test_init_without_cacert(self, disable_warning_mock):
        ribcl_client = ribcl.RIBCLOperations(
            "x.x.x.x", "admin", "Admin", 60, 443)

        self.assertEqual(ribcl_client.host, "x.x.x.x")
        self.assertEqual(ribcl_client.login, "admin")
        self.assertEqual(ribcl_client.password, "Admin")
        self.assertEqual(ribcl_client.timeout, 60)
        self.assertEqual(ribcl_client.port, 443)
        self.assertIsNone(ribcl_client.cacert)
        disable_warning_mock.assert_called_once_with(
            urllib3_exceptions.InsecureRequestWarning)


@ddt.ddt
class IloRibclTestCase(unittest.TestCase):

    def setUp(self):
        super(IloRibclTestCase, self).setUp()
        self.ilo = ribcl.RIBCLOperations("x.x.x.x", "admin",
                                         "Admin", 60, 443)
        self.ilo.init_model_based_tags('ProLiant DL580 Gen8')

    def test_init_model_based_tags_gen7(self):
        self.ilo.init_model_based_tags('Proliant DL380 G7')
        self.assertEqual(self.ilo.MEMORY_SIZE_TAG, "MEMORY_SIZE")
        self.assertEqual(self.ilo.MEMORY_SIZE_NOT_PRESENT_TAG, "Not Installed")
        self.assertEqual(self.ilo.NIC_INFORMATION_TAG, "NIC_INFOMATION")

    def test_init_model_based_tags(self):
        self.ilo.init_model_based_tags('ProLiant DL580 Gen8')
        self.assertEqual(self.ilo.MEMORY_SIZE_TAG, "TOTAL_MEMORY_SIZE")
        self.assertEqual(self.ilo.MEMORY_SIZE_NOT_PRESENT_TAG, "N/A")
        self.assertEqual(self.ilo.NIC_INFORMATION_TAG, "NIC_INFORMATION")

    @mock.patch.object(ribcl.RIBCLOperations, '_serialize_xml')
    @mock.patch.object(requests, 'post')
    def test__request_ilo_without_verify(self, post_mock, serialize_mock):
        response_mock = mock.MagicMock(text='returned-text')
        serialize_mock.return_value = 'serialized-xml'
        post_mock.return_value = response_mock

        retval = self.ilo._request_ilo('xml-obj')

        post_mock.assert_called_once_with(
            'https://x.x.x.x:443/ribcl',
            headers={"Content-length": '14'},
            data='serialized-xml',
            verify=False)
        response_mock.raise_for_status.assert_called_once_with()
        self.assertEqual('returned-text', retval)

    @mock.patch.object(ribcl.RIBCLOperations, '_serialize_xml')
    @mock.patch.object(requests, 'post')
    def test__request_ilo_with_verify(self, post_mock, serialize_mock):
        self.ilo = ribcl.RIBCLOperations(
            "x.x.x.x", "admin", "Admin", 60, 443,
            cacert='/somepath')
        response_mock = mock.MagicMock(text='returned-text')
        serialize_mock.return_value = 'serialized-xml'
        post_mock.return_value = response_mock

        retval = self.ilo._request_ilo('xml-obj')

        post_mock.assert_called_once_with(
            'https://x.x.x.x:443/ribcl',
            headers={"Content-length": '14'},
            data='serialized-xml',
            verify='/somepath')
        response_mock.raise_for_status.assert_called_once_with()
        self.assertEqual('returned-text', retval)

    @mock.patch.object(ribcl.RIBCLOperations, '_serialize_xml')
    @mock.patch.object(requests, 'post')
    def test__request_ilo_raises(self, post_mock, serialize_mock):
        serialize_mock.return_value = 'serialized-xml'
        post_mock.side_effect = Exception

        self.assertRaises(exception.IloConnectionError,
                          self.ilo._request_ilo,
                          'xml-obj')

        post_mock.assert_called_once_with(
            'https://x.x.x.x:443/ribcl',
            headers={"Content-length": '14'},
            data='serialized-xml',
            verify=False)

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

    def test_get_http_boot_url(self):
        self.assertRaises(
            exception.IloCommandNotSupportedError,
            self.ilo.get_http_boot_url
            )

    def test_set_http_boot_url(self):
        self.assertRaises(
            exception.IloCommandNotSupportedError,
            self.ilo.set_http_boot_url,
            'http://10.10.1.30:8081/startup.nsh'
            )

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

    @mock.patch.object(ribcl.RIBCLOperations, 'get_vm_status')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_eject_virtual_media_no_media(
            self, request_ilo_mock, get_vm_status_mock):
        """Ensure we don't try to eject media when no media is present."""
        get_vm_status_mock.return_value = {'IMAGE_INSERTED': 'NO'}
        self.ilo.eject_virtual_media(device='FLOPPY')
        get_vm_status_mock.assert_called_once_with(device='FLOPPY')
        self.assertFalse(request_ilo_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_vm_status')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_eject_virtual_media(
            self, request_ilo_mock, get_vm_status_mock):
        """Ensure we try to eject media when media is present."""
        get_vm_status_mock.return_value = {'IMAGE_INSERTED': 'YES'}
        request_ilo_mock.return_value = constants.EJECT_VIRTUAL_MEDIA_XML
        self.ilo.eject_virtual_media(device='CDROM')
        get_vm_status_mock.assert_called_once_with(device='CDROM')
        request_ilo_mock.assert_called_once_with(mock.ANY)

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

    @ddt.data(('LEGACY_ONLY', cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY),
              ('UEFI_ONLY', cons.SUPPORTED_BOOT_MODE_UEFI_ONLY),
              ('LEGACY_UEFI', cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI))
    @ddt.unpack
    @mock.patch.object(
        ribcl.RIBCLOperations, '_execute_command', autospec=True)
    def test_get_supported_boot_mode(
            self, raw_boot_mode_value, expected_boot_mode_value,
            _execute_command_mock):
        # | GIVEN |
        ret_val = {'GET_SUPPORTED_BOOT_MODE':
                   {'SUPPORTED_BOOT_MODE':
                    {'VALUE': raw_boot_mode_value}}}
        _execute_command_mock.return_value = ret_val
        # | WHEN |
        actual_val = self.ilo.get_supported_boot_mode()
        # | THEN |
        self.assertEqual(expected_boot_mode_value, actual_val)

    @mock.patch.object(common, 'wait_for_ilo_after_reset')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_reset_ilo(self, request_ilo_mock, status_mock):
        request_ilo_mock.return_value = constants.RESET_ILO_XML
        self.ilo.reset_ilo()
        self.assertTrue(request_ilo_mock.called)
        status_mock.assert_called_once_with(self.ilo)

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

    @mock.patch.object(ribcl.RIBCLOperations, '_set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_cdrom(self,
                                               request_ilo_mock,
                                               set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_NIC_UEFI_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["CDROM"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['Boot000B'])

    @mock.patch.object(ribcl.RIBCLOperations, '_set_persistent_boot')
    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_update_persistent_boot_uefi_hdd(self,
                                             request_ilo_mock,
                                             set_persist_boot_mock):
        xml = constants.GET_PERSISTENT_BOOT_DEVICE_CDROM_UEFI_XML
        request_ilo_mock.return_value = xml
        self.ilo.update_persistent_boot(["HDD"])
        self.assertTrue(request_ilo_mock.called)
        set_persist_boot_mock.assert_called_once_with(['Boot0007'])

    @mock.patch.object(ribcl.RIBCLOperations, '_set_persistent_boot')
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

    @mock.patch.object(ribcl.RIBCLOperations, '_set_persistent_boot')
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

    @mock.patch.object(requests, 'get')
    def test__request_host_with_verify(self, request_mock):
        self.ilo = ribcl.RIBCLOperations(
            "x.x.x.x", "admin", "Admin", 60, 443,
            cacert='/somepath')
        response_mock = mock.MagicMock(text='foo')
        request_mock.return_value = response_mock

        retval = self.ilo._request_host()

        request_mock.assert_called_once_with(
            "https://x.x.x.x/xmldata?item=all", verify='/somepath')
        response_mock.raise_for_status.assert_called_once_with()
        self.assertEqual('foo', retval)

    @mock.patch.object(requests, 'get')
    def test__request_host_without_verify(self, request_mock):
        response_mock = mock.MagicMock(text='foo')
        request_mock.return_value = response_mock

        retval = self.ilo._request_host()

        request_mock.assert_called_once_with(
            "https://x.x.x.x/xmldata?item=all", verify=False)
        response_mock.raise_for_status.assert_called_once_with()
        self.assertEqual('foo', retval)

    @mock.patch.object(requests, 'get')
    def test__request_host_raises(self, request_mock):
        request_mock.side_effect = Exception

        self.assertRaises(exception.IloConnectionError,
                          self.ilo._request_host)

        request_mock.assert_called_once_with(
            "https://x.x.x.x/xmldata?item=all", verify=False)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_host')
    def test_get_host_uuid(self, request_host_mock):
        request_host_mock.return_value = constants.GET_HOST_UUID
        name, uuid = self.ilo.get_host_uuid()
        self.assertIn('ProLiant ML110 G7', name)
        self.assertIn('37363536-3636-4D32-3232-303130324A41', uuid)

    def test__parse_processor_embedded_health(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        cpus, cpu_arch = self.ilo._parse_processor_embedded_health(json_data)
        self.assertEqual('32', str(cpus))
        self.assertEqual('x86_64', cpu_arch)
        self.assertTrue(type(cpus), int)

    def test__parse_processor_embedded_health_missing(self):
        data = constants.GET_EMBEDDED_HEALTH_PROCESSORS_DATA_MISSING
        json_data = json.loads(data)
        self.assertRaises(exception.IloError,
                          self.ilo._parse_processor_embedded_health,
                          json_data)

    def test__parse_memory_embedded_health(self):
        self.ilo.init_model_based_tags('Proliant DL580 Gen8')
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        memory_mb = self.ilo._parse_memory_embedded_health(json_data)
        self.assertEqual('32768', str(memory_mb))
        self.assertTrue(type(memory_mb), int)

    def test__parse_memory_embedded_health_gen7(self):
        self.ilo.model = 'Proliant DL380 G7'
        self.ilo.init_model_based_tags('Proliant DL380 G7')
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_GEN7
        json_data = json.loads(data)
        memory_mb = self.ilo._parse_memory_embedded_health(json_data)
        self.assertEqual('32768', str(memory_mb))
        self.assertTrue(type(memory_mb), int)

    def test__parse_nics_embedded_health_gen7(self):
        self.ilo.model = 'Proliant DL380 G7'
        self.ilo.init_model_based_tags('Proliant DL380 G7')
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_GEN7
        json_data = json.loads(data)
        expected_output = {u'Port 4': u'78:ac:c0:fe:49:66',
                           u'Port 3': u'78:ac:c0:fe:49:64',
                           u'Port 2': u'78:ac:c0:fe:49:62',
                           u'Port 1': u'78:ac:c0:fe:49:60'}
        nic_data = self.ilo._parse_nics_embedded_health(json_data)
        self.assertIsInstance(nic_data, dict)
        for key, val in nic_data.items():
            self.assertIn("Port", key)
        self.assertEqual(expected_output, nic_data)

    def test__parse_nics_embedded_health(self):
        self.ilo.init_model_based_tags('Proliant DL580 Gen8')
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        expected_output = {u'Port 4': u'40:a8:f0:1e:86:77',
                           u'Port 3': u'40:a8:f0:1e:86:76',
                           u'Port 2': u'40:a8:f0:1e:86:75',
                           u'Port 1': u'40:a8:f0:1e:86:74'}
        nic_data = self.ilo._parse_nics_embedded_health(json_data)
        self.assertIsInstance(nic_data, dict)
        for key, val in nic_data.items():
            self.assertIn("Port", key)
        self.assertEqual(expected_output, nic_data)

    def test__parse_storage_embedded_health(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        local_gb = self.ilo._parse_storage_embedded_health(json_data)
        self.assertTrue(type(local_gb), int)
        self.assertEqual("98", str(local_gb))

    def test__parse_storage_embedded_health_controller_list(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_LIST_STORAGE
        json_data = json.loads(data)
        local_gb = self.ilo._parse_storage_embedded_health(json_data)
        self.assertTrue(type(local_gb), int)
        self.assertEqual("98", str(local_gb))

    def test__parse_storage_embedded_health_no_logical_drive(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_NO_LOGICAL_DRIVE
        json_data = json.loads(data)
        local_gb = self.ilo._parse_storage_embedded_health(json_data)
        self.assertTrue(type(local_gb), int)
        self.assertEqual("0", str(local_gb))

    def test__parse_storage_embedded_health_no_controller(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_NO_CONTROLLER
        json_data = json.loads(data)
        local_gb = self.ilo._parse_storage_embedded_health(json_data)
        self.assertTrue(type(local_gb), int)
        self.assertEqual("0", str(local_gb))

    def test__get_firmware_embedded_health(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        firmware_dict = self.ilo._get_firmware_embedded_health(json_data)
        self.assertIsInstance(firmware_dict, dict)

    def test__get_rom_firmware_version(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        expected_rom = {'rom_firmware_version': "11/26/2014"}
        rom_firmware = self.ilo._get_rom_firmware_version(json_data)
        self.assertIsInstance(rom_firmware, dict)
        self.assertEqual(expected_rom, rom_firmware)

    def test__get_ilo_firmware_version(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        expected_ilo = {'ilo_firmware_version': "2.02 Sep 05 2014"}
        ilo_firmware = self.ilo._get_ilo_firmware_version(json_data)
        self.assertIsInstance(ilo_firmware, dict)
        self.assertEqual(expected_ilo, ilo_firmware)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_ilo_firmware_version_as_major_minor(self, mock_health_data):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        mock_health_data.return_value = json.loads(data)
        expected_ilo = '2.02'
        ilo_firmware = self.ilo.get_ilo_firmware_version_as_major_minor()
        self.assertEqual(expected_ilo, ilo_firmware)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_ilo_firmware_version_as_major_minor_eq_suggested(
            self, mock_health_data):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_EQ_SUGGESTED
        mock_health_data.return_value = json.loads(data)
        expected_ilo = '2.30'
        ilo_firmware = self.ilo.get_ilo_firmware_version_as_major_minor()
        self.assertEqual(expected_ilo, ilo_firmware)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_ilo_firmware_version_as_major_minor_gt_suggested(
            self, mock_health_data):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_GT_SUGGESTED
        mock_health_data.return_value = json.loads(data)
        expected_ilo = '2.54'
        ilo_firmware = self.ilo.get_ilo_firmware_version_as_major_minor()
        self.assertEqual(expected_ilo, ilo_firmware)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_ilo_firmware_version_as_major_minor_unexpected(
            self, mock_health_data):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_UNEXPECTED_FORMAT
        mock_health_data.return_value = json.loads(data)
        expected_ilo = None
        ilo_firmware = self.ilo.get_ilo_firmware_version_as_major_minor()
        self.assertEqual(expected_ilo, ilo_firmware)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_ilo_firmware_version_as_major_minor_no_firmware(
            self, mock_health_data):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_NO_FIRMWARE
        mock_health_data.return_value = json.loads(data)
        expected_ilo = None
        ilo_firmware = self.ilo.get_ilo_firmware_version_as_major_minor()
        self.assertEqual(expected_ilo, ilo_firmware)

    def test__get_number_of_gpu_devices_connected(self):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        gpu_cnt = self.ilo._get_number_of_gpu_devices_connected(json_data)
        self.assertIsInstance(gpu_cnt, dict)
        self.assertIn('pci_gpu_devices', gpu_cnt)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    def test_get_essential_properties(self, health_data_mock):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        health_data_mock.return_value = json_data
        expected_properties = {'macs': {
                               u'Port 4': u'40:a8:f0:1e:86:77',
                               u'Port 3': u'40:a8:f0:1e:86:76',
                               u'Port 2': u'40:a8:f0:1e:86:75',
                               u'Port 1': u'40:a8:f0:1e:86:74'
                               },
                               'properties': {
                               'memory_mb': 32768,
                               'cpu_arch': 'x86_64',
                               'local_gb': 98,
                               'cpus': 32}
                               }
        properties = self.ilo.get_essential_properties()
        self.assertIsInstance(properties, dict)
        self.assertIn('macs', properties)
        self.assertIn('properties', properties)
        self.assertEqual(expected_properties, properties)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_supported_boot_mode')
    def test_get_server_capabilities_gen8(
            self, boot_mode_mock, health_data_mock, server_mock):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        health_data_mock.return_value = json_data
        server_mock.return_value = 'ProLiant DL580 Gen8'
        boot_mode_mock.return_value = (
            cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI)

        capabilities = self.ilo.get_server_capabilities()

        self.assertIsInstance(capabilities, dict)
        self.assertIn('ilo_firmware_version', capabilities)
        self.assertIn('rom_firmware_version', capabilities)
        self.assertIn('server_model', capabilities)
        self.assertIn('pci_gpu_devices', capabilities)
        self.assertIn('boot_mode_bios', capabilities)
        self.assertIn('boot_mode_uefi', capabilities)
        self.assertEqual('true', capabilities['boot_mode_bios'])
        self.assertEqual('true', capabilities['boot_mode_uefi'])
        self.assertNotIn('secure_boot', capabilities)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    @mock.patch.object(ribcl.RIBCLOperations, '_get_ilo_firmware_version')
    @mock.patch.object(ribcl.RIBCLOperations, '_get_rom_firmware_version')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_supported_boot_mode')
    def test_get_server_capabilities_gen8_no_firmware(
            self, boot_mode_mock, rom_mock, ilo_mock, health_data_mock,
            server_mock):
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        json_data = json.loads(data)
        health_data_mock.return_value = json_data
        server_mock.return_value = 'ProLiant DL580 Gen8'
        ilo_mock.return_value = None
        rom_mock.return_value = None
        boot_mode_mock.return_value = cons.SUPPORTED_BOOT_MODE_UEFI_ONLY

        capabilities = self.ilo.get_server_capabilities()

        self.assertIsInstance(capabilities, dict)
        self.assertNotIn('ilo_firmware_version', capabilities)
        self.assertNotIn('rom_firmware_version', capabilities)
        self.assertIn('server_model', capabilities)
        self.assertIn('pci_gpu_devices', capabilities)
        self.assertIn('boot_mode_bios', capabilities)
        self.assertIn('boot_mode_uefi', capabilities)
        print(capabilities)
        self.assertEqual('false', capabilities['boot_mode_bios'])
        self.assertEqual('true', capabilities['boot_mode_uefi'])
        self.assertNotIn('secure_boot', capabilities)

    def test__get_nic_boot_devices(self):
        data = json.loads(constants.GET_NIC_DATA)
        expected = ["Boot0003", "Boot0001", "Boot0004"]
        result = self.ilo._get_nic_boot_devices(data)
        self.assertEqual(result, expected)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_activate_license_ok(self, request_mock):
        request_mock.return_value = constants.ACTIVATE_LICENSE_XML
        self.ilo.activate_license("testkey")
        self.assertTrue(request_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, '_request_ilo')
    def test_activate_license_invalid(self, request_mock):
        request_mock.return_value = constants.ACTIVATE_LICENSE_FAIL_XML
        self.assertRaises(exception.IloError, self.ilo.activate_license, 'key')
        self.assertTrue(request_mock.called)

    @mock.patch.object(
        ribcl.firmware_controller.FirmwareImageUploader, 'upload_file_to')
    @mock.patch.object(ribcl, 'os', autospec=True)
    @mock.patch.object(ribcl.IloClient, '_request_ilo', autospec=True)
    @mock.patch.object(ribcl.IloClient, '_parse_output', autospec=True)
    @mock.patch.object(common, 'wait_for_ribcl_firmware_update_to_complete',
                       lambda x: None)
    def test_update_ilo_firmware(self, _parse_output_mock, _request_ilo_mock,
                                 os_mock, upload_file_to_mock):
        # | GIVEN |
        upload_file_to_mock.return_value = 'hickory-dickory-dock'
        os_mock.path.getsize.return_value = 12345
        # | WHEN |
        self.ilo.update_firmware('raw_fw_file.bin', 'ilo')
        # | THEN |
        upload_file_to_mock.assert_called_once_with(
            (self.ilo.host, self.ilo.port), self.ilo.timeout)

        root_xml_string = constants.UPDATE_ILO_FIRMWARE_INPUT_XML % (
            self.ilo.password, self.ilo.login, 12345, 'raw_fw_file.bin')
        root_xml_string = re.sub('\n\s*', '', root_xml_string)

        ((ribcl_obj, xml_elem), the_ext_header_dict) = (
            _request_ilo_mock.call_args)

        self.assertEqual(root_xml_string,
                         ET.tostring(xml_elem).decode('latin-1'))
        self.assertDictEqual(the_ext_header_dict['extra_headers'],
                             {'Cookie': 'hickory-dickory-dock'})

        _parse_output_mock.assert_called_once_with(
            self.ilo, _request_ilo_mock.return_value)

    @mock.patch.object(
        ribcl.firmware_controller.FirmwareImageUploader, 'upload_file_to')
    @mock.patch.object(ribcl, 'os', autospec=True)
    @mock.patch.object(ribcl.IloClient, '_request_ilo', autospec=True)
    @mock.patch.object(ribcl.IloClient, '_parse_output', autospec=True)
    @mock.patch.object(common, 'wait_for_ribcl_firmware_update_to_complete',
                       lambda x: None)
    def test_update_other_component_firmware(self, _parse_output_mock,
                                             _request_ilo_mock, os_mock,
                                             upload_file_to_mock):
        # | GIVEN |
        upload_file_to_mock.return_value = 'hickory-dickory-dock'
        os_mock.path.getsize.return_value = 12345
        # | WHEN |
        self.ilo.update_firmware('raw_fw_file.bin', 'power_pic')
        # | THEN |
        upload_file_to_mock.assert_called_once_with(
            (self.ilo.host, self.ilo.port), self.ilo.timeout)

        root_xml_string = constants.UPDATE_NONILO_FIRMWARE_INPUT_XML % (
            self.ilo.password, self.ilo.login, 12345, 'raw_fw_file.bin')
        root_xml_string = re.sub('\n\s*', '', root_xml_string)

        ((ribcl_obj, xml_elem), the_ext_header_dict) = (
            _request_ilo_mock.call_args)

        self.assertEqual(root_xml_string,
                         ET.tostring(xml_elem).decode('latin-1'))
        self.assertDictEqual(the_ext_header_dict['extra_headers'],
                             {'Cookie': 'hickory-dickory-dock'})

        _parse_output_mock.assert_called_once_with(
            self.ilo, _request_ilo_mock.return_value)

    def test_update_firmware_throws_error_for_invalid_component(self):
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          self.ilo.update_firmware,
                          'raw_fw_file.bin',
                          'invalid_component')

    def test__get_memory_details_value_based_on_model_gen7(self):
        self.ilo.model = 'Proliant DL380 G7'
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT_GEN7
        self.assertIn('MEMORY_COMPONENTS', data)
        self.assertIn('MEMORY_COMPONENT', data)

    def test__get_memory_details_value_based_on_model(self):
        self.ilo.model = 'ProLiant DL580 Gen8'
        data = constants.GET_EMBEDDED_HEALTH_OUTPUT
        self.assertIn('MEMORY_DETAILS_SUMMARY', data)

    def test__update_nic_data_from_nic_info_based_on_model_gen7(self):
        self.ilo.model = 'Proliant DL380 G7'
        nic_dict = {}
        item = {'NETWORK_PORT': {'VALUE': 'Port 1'},
                'MAC_ADDRESS': {'VALUE': '78:ac:c0:fe:49:60'}}
        port = 'Port 1'
        mac = '78:ac:c0:fe:49:60'
        expected_result = {'Port 1': '78:ac:c0:fe:49:60'}
        self.ilo._update_nic_data_from_nic_info_based_on_model(
            nic_dict, item, port, mac)
        self.assertEqual(expected_result, nic_dict)

    def test__update_nic_data_from_nic_info_based_on_model(self):
        self.ilo.model = 'ProLiant DL580 Gen8'
        nic_dict = {}
        item = {'NETWORK_PORT': {'VALUE': 'Port 1'},
                'STATUS': {'VALUE': 'Unknown'},
                'PORT_DESCRIPTION': {'VALUE': 'N/A'},
                'LOCATION': {'VALUE': 'Embedded'},
                'MAC_ADDRESS': {'VALUE': '40:a8:f0:1e:86:74'},
                'IP_ADDRESS': {'VALUE': 'N/A'}}
        port = 'Port 1'
        mac = '40:a8:f0:1e:86:74'
        expected_result = {'Port 1': '40:a8:f0:1e:86:74'}
        self.ilo._update_nic_data_from_nic_info_based_on_model(
            nic_dict, item, port, mac)
        self.assertEqual(expected_result, nic_dict)


class IloRibclTestCaseBeforeRisSupport(unittest.TestCase):

    def setUp(self):
        super(IloRibclTestCaseBeforeRisSupport, self).setUp()
        self.ilo = ribcl.IloClient("x.x.x.x", "admin", "Admin", 60, 443)

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

    @mock.patch.object(ribcl.RIBCLOperations, 'get_vm_status')
    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_eject_virtual_media(self, request_ilo_mock, get_vm_status_mock):
        get_vm_status_mock.return_value = {'IMAGE_INSERTED': 'YES'}
        request_ilo_mock.return_value = constants.EJECT_VIRTUAL_MEDIA_XML
        self.assertIsNone(self.ilo.eject_virtual_media(device='CDROM'))
        get_vm_status_mock.assert_called_once_with(device='CDROM')
        request_ilo_mock.assert_called_once_with(mock.ANY)

    @mock.patch.object(ribcl.IloClient, '_request_ilo')
    def test_set_vm_status(self, request_ilo_mock):
        request_ilo_mock.return_value = constants.SET_VM_STATUS_XML
        self.ilo.set_vm_status('cdrom', 'boot_once', 'yes')
        self.assertTrue(request_ilo_mock.called)


if __name__ == '__main__':
    unittest.main()
