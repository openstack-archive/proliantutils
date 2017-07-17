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

import json

import mock
import testtools

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ris
from proliantutils.tests.ilo import ris_sample_outputs as ris_outputs


class IloRisTestCase(testtools.TestCase):

    def setUp(self):
        super(IloRisTestCase, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "Administrator", "Admin")

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_get_http_boot_url_uefi(self, _uefi_boot_mode_mock,
                                    get_bios_settings_mock):
        get_bios_settings_mock.return_value = ris_outputs.HTTP_BOOT_URL
        _uefi_boot_mode_mock.return_value = True
        result = self.client.get_http_boot_url()
        _uefi_boot_mode_mock.assert_called_once_with()
        self.assertEqual(
            'http://10.10.1.30:8081/startup.nsh', result['UefiShellStartupUrl']
            )

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_set_http_boot_url_uefi(self, _uefi_boot_mode_mock,
                                    change_bios_setting_mock):
        _uefi_boot_mode_mock.return_value = True
        self.client.set_http_boot_url('http://10.10.1.30:8081/startup.nsh')
        _uefi_boot_mode_mock.assert_called_once_with()
        change_bios_setting_mock.assert_called_once_with({
            "UefiShellStartupUrl": "http://10.10.1.30:8081/startup.nsh"
            })

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_get_http_boot_url_bios(self, _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.get_http_boot_url)
        _uefi_boot_mode_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_set_http_boot_url_bios(self, _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.set_http_boot_url,
                          'http://10.10.1.30:8081/startup.nsh')
        _uefi_boot_mode_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_change_iscsi_settings')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_set_iscsi_boot_info_uefi(self, _uefi_boot_mode_mock,
                                      change_iscsi_settings_mock):
        _uefi_boot_mode_mock.return_value = True
        iscsi_variables = {
            'iSCSITargetName': 'iqn.2011-07.com.example.server:test1',
            'iSCSITargetInfoViaDHCP': False,
            'iSCSIBootLUN': '1',
            'iSCSIBootEnable': 'Enabled',
            'iSCSITargetIpAddress': '10.10.1.30',
            'iSCSITargetTcpPort': 3260}
        self.client.set_iscsi_boot_info(
            'C4346BB7EF30',
            'iqn.2011-07.com.example.server:test1',
            '1', '10.10.1.30')
        _uefi_boot_mode_mock.assert_called_once_with()
        change_iscsi_settings_mock.assert_called_once_with('C4346BB7EF30',
                                                           iscsi_variables)

    @mock.patch.object(ris.RISOperations, '_change_iscsi_settings')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_unset_iscsi_boot_info_uefi(self, _uefi_boot_mode_mock,
                                        change_iscsi_settings_mock):
        _uefi_boot_mode_mock.return_value = True
        iscsi_variables = {'iSCSIBootEnable': 'Disabled'}
        self.client.unset_iscsi_boot_info('C4346BB7EF30')
        _uefi_boot_mode_mock.assert_called_once_with()
        change_iscsi_settings_mock.assert_called_once_with('C4346BB7EF30',
                                                           iscsi_variables)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_unset_iscsi_boot_info_bios(self, _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        mac = 'C4346BB7EF30'
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.unset_iscsi_boot_info, mac)
        _uefi_boot_mode_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    def test_set_iscsi_boot_info_bios(self, _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        mac = 'C4346BB7EF30'
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.set_iscsi_boot_info, mac,
                          'iqn.2011-07.com.example.server:test1',
                          '1', '10.10.1.30')
        _uefi_boot_mode_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode(self, get_details_mock, rest_get_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        uri = ris_outputs.REST_GET_SECURE_BOOT['links']['self']['href']
        rest_get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                      ris_outputs.REST_GET_SECURE_BOOT)
        result = self.client.get_secure_boot_mode()
        self.assertFalse(result)
        get_details_mock.assert_called_once_with()
        rest_get_mock.assert_called_once_with(uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode_fail(self, get_details_mock, rest_get_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        uri = ris_outputs.REST_GET_SECURE_BOOT['links']['self']['href']
        rest_get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                      ris_outputs.REST_FAILURE_OUTPUT)
        exc = self.assertRaises(exception.IloError,
                                self.client.get_secure_boot_mode)
        get_details_mock.assert_called_once_with()
        rest_get_mock.assert_called_once_with(uri)
        self.assertIn('FakeFailureMessage', str(exc))

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_secure_boot_mode_not_supported(self, get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        del host_response['Oem']['Hp']['links']['SecureBoot']
        get_details_mock.return_value = host_response
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client.get_secure_boot_mode)
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_host_power_status_ok(self, get_details_mock):
        host_response = ris_outputs.RESPONSE_BODY_FOR_REST_OP
        get_details_mock.return_value = json.loads(host_response)
        result = self.client.get_host_power_status()
        self.assertEqual(result, 'OFF')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(common, 'wait_for_ilo_after_reset')
    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_ok(self, get_mock, post_mock, status_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 manager_data)
        post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_POST_RESPONSE)
        self.client.reset_ilo()
        get_mock.assert_called_once_with(uri)
        post_mock.assert_called_once_with(uri, None, {'Action': 'Reset'})
        status_mock.assert_called_once_with(self.client)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_fail(self, get_mock, post_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.HEADERS_FOR_REST_OP,
                                 manager_data)
        post_mock.return_value = (301, ris_outputs.HEADERS_FOR_REST_OP,
                                  ris_outputs.REST_FAILURE_OUTPUT)
        exc = self.assertRaises(exception.IloError, self.client.reset_ilo)

        get_mock.assert_called_once_with(uri)
        post_mock.assert_called_once_with(uri, None, {'Action': 'Reset'})
        self.assertIn('FakeFailureMessage', str(exc))

    @mock.patch.object(ris.RISOperations, '_get_type')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test_reset_ilo_type_mismatch(self, get_mock, type_mock):
        uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        get_mock.return_value = (200, ris_outputs.HEADERS_FOR_REST_OP,
                                 manager_data)
        type_mock.return_value = 'Manager.x'
        self.assertRaises(exception.IloError, self.client.reset_ilo)
        get_mock.assert_called_once_with(uri)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_reset_secure_boot_keys(self, change_mock,
                                    _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = True
        self.client.reset_secure_boot_keys()
        _uefi_boot_mode_mock.assert_called_once_with()
        change_mock.assert_called_once_with('ResetToDefaultKeys', True)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_reset_secure_boot_keys_bios(self, change_mock,
                                         _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.reset_secure_boot_keys)

        _uefi_boot_mode_mock.assert_called_once_with()
        self.assertFalse(change_mock.called)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_clear_secure_boot_keys(self, change_mock,
                                    _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = True
        self.client.clear_secure_boot_keys()
        _uefi_boot_mode_mock.assert_called_once_with()
        change_mock.assert_called_once_with('ResetAllKeys', True)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_clear_secure_boot_keys_bios(self, change_mock,
                                         _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.clear_secure_boot_keys)

        _uefi_boot_mode_mock.assert_called_once_with()
        self.assertFalse(change_mock.called)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_set_secure_boot_mode(self, change_mock,
                                  _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = True
        self.client.set_secure_boot_mode(True)
        _uefi_boot_mode_mock.assert_called_once_with()
        change_mock.assert_called_once_with('SecureBootEnable', True)

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_change_secure_boot_settings')
    def test_set_secure_boot_mode_bios(self, change_mock,
                                       _uefi_boot_mode_mock):
        _uefi_boot_mode_mock.return_value = False
        self.assertRaises(exception.IloCommandNotSupportedInBiosError,
                          self.client.set_secure_boot_mode, True)

        _uefi_boot_mode_mock.assert_called_once_with()
        self.assertFalse(change_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_product_name(self, get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_response
        result = self.client.get_product_name()
        self.assertEqual(result, 'ProLiant BL460c Gen9')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test_get_current_boot_mode(self, bios_mock):
        bios_mock.return_value = 'LegacyBios'
        result = self.client.get_current_boot_mode()
        self.assertEqual(result, 'LEGACY')

    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test_get_pending_boot_mode(self, check_mock, bios_mock):
        check_mock.return_value = ('fake', 'fake',
                                   json.loads(ris_outputs.GET_BIOS_SETTINGS))
        bios_mock.return_value = ('fake', 'fake',
                                  json.loads(ris_outputs.GET_BIOS_SETTINGS))
        result = self.client.get_pending_boot_mode()
        self.assertEqual(result, 'UEFI')

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    def test_set_pending_boot_mode_legacy(self, change_mock):
        self.client.set_pending_boot_mode('legacy')
        change_mock.assert_called_once_with({'BootMode': 'LegacyBios'})

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    def test_set_pending_boot_mode_uefi(self, change_mock):
        self.client.set_pending_boot_mode('uefi')
        expected_properties = {'BootMode': 'uefi',
                               'UefiOptimizedBoot': 'Enabled'}
        change_mock.assert_called_once_with(expected_properties)

    def test_set_pending_boot_mode_invalid_mode(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client.set_pending_boot_mode, 'invalid')

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential(self, collection_mock, patch_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.reset_ilo_credential('fake-password')
        patch_mock.assert_called_once_with(uri, None,
                                           {'Password': 'fake-password'})

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential_fail(self, collection_mock, patch_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client.reset_ilo_credential,
                          'fake-password')
        patch_mock.assert_called_once_with(uri, None,
                                           {'Password': 'fake-password'})

    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test_reset_ilo_credential_no_account(self, collection_mock):
        uri = '/rest/v1/AccountService/Accounts/1'
        self.client = ris.RISOperations("1.2.3.4", "Admin", "Admin")
        collection_output = json.loads(ris_outputs.COLLECTIONS_SAMPLE)
        item = collection_output['Items'][0]
        collection_mock.return_value = [(200, None, item, uri)]
        self.assertRaises(exception.IloError,
                          self.client.reset_ilo_credential,
                          'fake-password')

    @mock.patch.object(ris.RISOperations, '_validate_if_patch_supported')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_bios_hash_password')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_operation_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test_reset_bios_to_default(self, check_mock, bios_mock, op_mock,
                                   get_mock, passwd_mock, patch_mock,
                                   validate_mock):
        settings_uri = '/rest/v1/systems/1/bios/Settings'
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        base_config = json.loads(ris_outputs.GET_BASE_CONFIG)
        default_config = base_config['BaseConfigs'][0]['default']
        check_mock.return_value = (ris_outputs.GET_HEADERS, 'fake',
                                   json.loads(ris_outputs.GET_BIOS_SETTINGS))
        op_mock.return_value = False
        passwd_mock.return_value = {}
        get_mock.return_value = (200, 'fake', base_config)
        bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                  settings_uri, {})
        patch_mock.return_value = (200, 'fake', 'fake')
        self.client.reset_bios_to_default()
        check_mock.assert_called_once_with()
        bios_mock.assert_called_once_with(settings)
        op_mock.assert_called_once_with(ris_outputs.GET_HEADERS, 'PATCH')
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/BaseConfigs')
        passwd_mock.assert_called_once_with(None)
        patch_mock.assert_called_once_with(settings_uri, {}, default_config)
        validate_mock.assert_called_once_with(ris_outputs.GET_HEADERS,
                                              settings_uri)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_get_nvdimm_n_status')
    @mock.patch.object(ris.RISOperations,
                       '_get_cpu_virtualization')
    @mock.patch.object(ris.RISOperations, '_get_tpm_capability')
    @mock.patch.object(ris.RISOperations,
                       '_get_number_of_gpu_devices_connected')
    @mock.patch.object(ris.RISOperations, 'get_secure_boot_mode')
    @mock.patch.object(ris.RISOperations, '_get_ilo_firmware_version')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_server_capabilities(self, get_details_mock, ilo_firm_mock,
                                     secure_mock, gpu_mock, tpm_mock,
                                     cpu_vt_mock, nvdimm_n_mock,
                                     bios_sriov_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        ilo_firm_mock.return_value = {'ilo_firmware_version': 'iLO 4 v2.20'}
        gpu_mock.return_value = {'pci_gpu_devices': 2}
        cpu_vt_mock.return_value = True
        secure_mock.return_value = False
        nvdimm_n_mock.return_value = True
        tpm_mock.return_value = True
        bios_sriov_mock.return_value = 'Disabled'
        expected_caps = {'secure_boot': 'true',
                         'ilo_firmware_version': 'iLO 4 v2.20',
                         'rom_firmware_version': u'I36 v1.40 (01/28/2015)',
                         'server_model': u'ProLiant BL460c Gen9',
                         'pci_gpu_devices': 2,
                         'trusted_boot': 'true',
                         'cpu_vt': 'true',
                         'nvdimm_n': 'true'}
        capabilities = self.client.get_server_capabilities()
        self.assertEqual(expected_caps, capabilities)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_get_nvdimm_n_status')
    @mock.patch.object(ris.RISOperations,
                       '_get_cpu_virtualization')
    @mock.patch.object(ris.RISOperations, '_get_tpm_capability')
    @mock.patch.object(ris.RISOperations,
                       '_get_number_of_gpu_devices_connected')
    @mock.patch.object(ris.RISOperations, 'get_secure_boot_mode')
    @mock.patch.object(ris.RISOperations, '_get_ilo_firmware_version')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_server_capabilities_tp_absent(self,
                                               get_details_mock,
                                               ilo_firm_mock, secure_mock,
                                               gpu_mock, tpm_mock,
                                               cpu_vt_mock, nvdimm_n_mock,
                                               bios_sriov_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        ilo_firm_mock.return_value = {'ilo_firmware_version': 'iLO 4 v2.20'}
        gpu_mock.return_value = {'pci_gpu_devices': 2}
        secure_mock.return_value = False
        nvdimm_n_mock.return_value = True
        tpm_mock.return_value = False
        cpu_vt_mock.return_value = True
        bios_sriov_mock.return_value = 'Enabled'
        expected_caps = {'secure_boot': 'true',
                         'ilo_firmware_version': 'iLO 4 v2.20',
                         'rom_firmware_version': u'I36 v1.40 (01/28/2015)',
                         'server_model': u'ProLiant BL460c Gen9',
                         'pci_gpu_devices': 2,
                         'cpu_vt': 'true',
                         'nvdimm_n': 'true',
                         'sriov_enabled': 'true'}
        capabilities = self.client.get_server_capabilities()
        self.assertEqual(expected_caps, capabilities)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_get_ilo_firmware_version_as_major_minor(
            self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client.get_ilo_firmware_version_as_major_minor()
        expected_ilo_firm = "2.04"
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_get_ilo_firmware_version_as_major_minor_suggested_min(
            self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS_EQ_SUGGESTED)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client.get_ilo_firmware_version_as_major_minor()
        expected_ilo_firm = "2.30"
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_get_ilo_firmware_version_as_major_minor_gt_suggested_min(
            self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS_GT_SUGGESTED)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client.get_ilo_firmware_version_as_major_minor()
        expected_ilo_firm = "2.54"
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_get_ilo_firmware_version_as_major_minor_no_firmware(
            self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS_NO_FIRMWARE)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client.get_ilo_firmware_version_as_major_minor()
        expected_ilo_firm = None
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test__get_ilo_firmware_version(self, get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        ilo_firm = self.client._get_ilo_firmware_version()
        expected_ilo_firm = {'ilo_firmware_version': 'iLO 4 v2.20'}
        self.assertIn('ilo_firmware_version', ilo_firm)
        self.assertEqual(expected_ilo_firm, ilo_firm)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license(self, get_ilo_details_mock, post_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        license_uri = "/rest/v1/Managers/1/LicenseService"
        get_ilo_details_mock.return_value = (ilo_details, uri)
        post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_POST_RESPONSE)
        self.client.activate_license('testkey')
        get_ilo_details_mock.assert_called_once_with()
        post_mock.assert_called_once_with(license_uri, None,
                                          {'LicenseKey': 'testkey'})

    @mock.patch.object(ris.RISOperations, '_rest_post')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license_IloError(self, get_ilo_details_mock, post_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        uri = '/rest/v1/Managers/1'
        license_uri = "/rest/v1/Managers/1/LicenseService"
        get_ilo_details_mock.return_value = (ilo_details, uri)
        post_mock.return_value = (500, ris_outputs.GET_HEADERS,
                                  ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError, self.client.activate_license,
                          'testkey')
        get_ilo_details_mock.assert_called_once_with()
        post_mock.assert_called_once_with(license_uri, None,
                                          {'LicenseKey': 'testkey'})

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test_activate_license_IloCommandNotSupported(self,
                                                     get_ilo_details_mock):
        ilo_details = json.loads(ris_outputs.GET_MANAGER_DETAILS)
        del ilo_details['Oem']['Hp']['links']['LicenseService']
        uri = '/rest/v1/Managers/1'
        get_ilo_details_mock.return_value = (ilo_details, uri)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client.activate_license, 'testkey')
        get_ilo_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_get_vm_status_floppy_empty(self, get_vm_device_status_mock):
        floppy_resp = json.loads(ris_outputs.RESP_VM_STATUS_FLOPPY_EMPTY)
        device_uri = floppy_resp["links"]["self"]["href"]
        get_vm_device_status_mock.return_value = (floppy_resp, device_uri)
        exp_result = json.loads(ris_outputs.GET_VM_STATUS_FLOPPY_EMPTY)
        result = self.client.get_vm_status('FLOPPY')
        self.assertEqual(result, exp_result)
        get_vm_device_status_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_get_vm_status_floppy_inserted(self, get_vm_device_status_mock):
        floppy_resp = json.loads(ris_outputs.RESP_VM_STATUS_FLOPPY_INSERTED)
        device_uri = floppy_resp["links"]["self"]["href"]
        get_vm_device_status_mock.return_value = (floppy_resp, device_uri)
        exp_result = json.loads(ris_outputs.GET_VM_STATUS_FLOPPY_INSERTED)
        result = self.client.get_vm_status('FLOPPY')
        self.assertEqual(result, exp_result)
        get_vm_device_status_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_get_vm_status_cdrom_empty(self, get_vm_device_status_mock):
        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_EMPTY)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_status_mock.return_value = (cdrom_resp, device_uri)
        exp_result = json.loads(ris_outputs.GET_VM_STATUS_CDROM_EMPTY)
        result = self.client.get_vm_status('CDROM')
        self.assertEqual(result, exp_result)
        get_vm_device_status_mock.assert_called_once_with('CDROM')

    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_get_vm_status_cdrom_inserted(self, get_vm_device_status_mock):
        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_status_mock.return_value = (cdrom_resp, device_uri)
        exp_result = json.loads(ris_outputs.GET_VM_STATUS_CDROM_INSERTED)
        result = self.client.get_vm_status('CDROM')
        self.assertEqual(result, exp_result)
        get_vm_device_status_mock.assert_called_once_with('CDROM')

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test_set_vm_status_cdrom_connect(self, patch_mock):
        self.client.set_vm_status('CDROM', boot_option='CONNECT')
        self.assertFalse(patch_mock.called)

    def test_set_vm_status_cdrom_invalid_arg(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client.set_vm_status,
                          device='CDROM',
                          boot_option='FOO')

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_set_vm_status_cdrom(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = json.loads(ris_outputs.PATCH_VM_CDROM)

        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.set_vm_status(device='CDROM', boot_option='BOOT_ONCE')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_set_vm_status_cdrom_fail(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = json.loads(ris_outputs.PATCH_VM_CDROM)

        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client.set_vm_status,
                          device='CDROM', boot_option='BOOT_ONCE')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_insert_virtual_media(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_EMPTY)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = {'Image': 'http://1.1.1.1/cdrom.iso'}

        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.insert_virtual_media('http://1.1.1.1/cdrom.iso',
                                         device='CDROM')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, 'eject_virtual_media')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_insert_virtual_media_media_attached(self,
                                                 get_vm_device_mock,
                                                 eject_virtual_media_mock,
                                                 patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = {'Image': 'http://1.1.1.1/cdrom.iso'}

        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.insert_virtual_media('http://1.1.1.1/cdrom.iso',
                                         device='CDROM')
        get_vm_device_mock.assert_called_once_with('CDROM')
        eject_virtual_media_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_insert_virtual_media_fail(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_EMPTY)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = {'Image': 'http://1.1.1.1/cdrom.iso'}

        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client.insert_virtual_media,
                          'http://1.1.1.1/cdrom.iso', device='CDROM')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_eject_virtual_media(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = {'Image': None}

        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client.eject_virtual_media(device='CDROM')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_eject_virtual_media_cdrom_empty(
            self, get_vm_device_mock, patch_mock):
        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_EMPTY)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        self.client.eject_virtual_media(device='CDROM')

        get_vm_device_mock.assert_called_once_with('CDROM')
        self.assertFalse(patch_mock.called)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_vm_device_status')
    def test_eject_virtual_media_fail(self, get_vm_device_mock, patch_mock):
        vm_uri = '/rest/v1/Managers/1/VirtualMedia/2'

        cdrom_resp = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_INSERTED)
        device_uri = cdrom_resp["links"]["self"]["href"]
        get_vm_device_mock.return_value = (cdrom_resp, device_uri)

        vm_patch = {'Image': None}

        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client.eject_virtual_media, device='CDROM')
        get_vm_device_mock.assert_called_once_with('CDROM')
        patch_mock.assert_called_once_with(vm_uri, None, vm_patch)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_one_time_boot_not_set(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        ret = self.client.get_one_time_boot()
        get_host_details_mock.assert_called_once_with()
        self.assertEqual(ret, 'Normal')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_one_time_boot_cdrom(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.RESP_BODY_FOR_SYSTEM_WITH_CDROM)
        get_host_details_mock.return_value = system_data
        ret = self.client.get_one_time_boot()
        get_host_details_mock.assert_called_once_with()
        self.assertEqual(ret, 'CDROM')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_one_time_boot_UefiShell(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.RESP_BODY_WITH_UEFI_SHELL)
        get_host_details_mock.return_value = system_data
        ret = self.client.get_one_time_boot()
        get_host_details_mock.assert_called_once_with()
        self.assertEqual(ret, 'UefiShell')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_one_time_boot_exc(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.RESP_BODY_FOR_SYSTEM_WITHOUT_BOOT)
        get_host_details_mock.return_value = system_data
        self.assertRaises(exception.IloError,
                          self.client.get_one_time_boot)
        get_host_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_update_persistent_boot')
    def test_set_one_time_boot_cdrom(self, update_persistent_boot_mock):
        self.client.set_one_time_boot('cdrom')
        update_persistent_boot_mock.assert_called_once_with(
            ['cdrom'], persistent=False, mac=None)

    @mock.patch.object(ris.RISOperations, '_update_persistent_boot')
    def test_set_one_time_boot_iscsi(self, update_persistent_boot_mock):
        self.client.set_one_time_boot('ISCSI', '9cb654797870')
        update_persistent_boot_mock.assert_called_once_with(
            ['ISCSI'], persistent=False, mac='9cb654797870')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_cdrom(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.SYSTEM_WITH_CDROM_CONT)
        get_host_details_mock.return_value = system_data
        ret = self.client.get_persistent_boot_device()
        get_host_details_mock.assert_called_once_with()
        self.assertEqual(ret, 'CDROM')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_UefiShell(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.SYSTEM_WITH_UEFISHELL_CONT)
        get_host_details_mock.return_value = system_data
        ret = self.client.get_persistent_boot_device()
        get_host_details_mock.assert_called_once_with()
        self.assertEqual(ret, 'UefiShell')

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_exc(self, get_host_details_mock):
        system_data = json.loads(ris_outputs.RESP_BODY_FOR_SYSTEM_WITHOUT_BOOT)
        get_host_details_mock.return_value = system_data
        self.assertRaises(exception.IloError,
                          self.client.get_persistent_boot_device)
        get_host_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_bios(self, get_host_details_mock,
                                             _uefi_boot_mode_mock):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        _uefi_boot_mode_mock.return_value = False
        ret = self.client.get_persistent_boot_device()
        get_host_details_mock.assert_called_once_with()
        self.assertIsNone(ret)

    @mock.patch.object(ris.RISOperations, '_get_persistent_boot_devices')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def _test_get_persistent_boot_device_uefi(self, get_host_details_mock,
                                              _uefi_boot_mode_mock,
                                              boot_devices_mock,
                                              boot_devices,
                                              boot_sources,
                                              exp_ret_value=None):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        _uefi_boot_mode_mock.return_value = True
        boot_devices_mock.return_value = boot_sources, boot_devices

        ret = self.client.get_persistent_boot_device()
        get_host_details_mock.assert_called_once_with()
        _uefi_boot_mode_mock.assert_called_once_with()
        boot_devices_mock.assert_called_once_with()
        self.assertEqual(ret, exp_ret_value)

    def test_get_persistent_boot_device_uefi_pxe(self):
        boot_devs = ris_outputs.UEFI_BOOT_DEVICE_ORDER_PXE
        boot_srcs = json.loads(ris_outputs.UEFI_BootSources)

        self._test_get_persistent_boot_device_uefi(boot_devices=boot_devs,
                                                   boot_sources=boot_srcs,
                                                   exp_ret_value='NETWORK')

    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_uefi_cd(self, get_host_details_mock,
                                                _uefi_boot_mode_mock):
        boot_devs = ris_outputs.UEFI_BOOT_DEVICE_ORDER_CD
        boot_srcs = json.loads(ris_outputs.UEFI_BootSources)

        self._test_get_persistent_boot_device_uefi(boot_devices=boot_devs,
                                                   boot_sources=boot_srcs,
                                                   exp_ret_value='CDROM')

    def test_get_persistent_boot_device_uefi_hdd(self):
        boot_devs = ris_outputs.UEFI_BOOT_DEVICE_ORDER_HDD
        boot_srcs = json.loads(ris_outputs.UEFI_BootSources)

        self._test_get_persistent_boot_device_uefi(boot_devices=boot_devs,
                                                   boot_sources=boot_srcs,
                                                   exp_ret_value='HDD')

    def test_get_persistent_boot_device_uefi_none(self):
        boot_devs = ris_outputs.UEFI_BOOT_DEVICE_ORDER_ERR
        boot_srcs = json.loads(ris_outputs.UEFI_BootSources)

        self._test_get_persistent_boot_device_uefi(boot_devices=boot_devs,
                                                   boot_sources=boot_srcs,
                                                   exp_ret_value=None)

    @mock.patch.object(ris.RISOperations, '_get_persistent_boot_devices')
    @mock.patch.object(ris.RISOperations, '_is_boot_mode_uefi')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test_get_persistent_boot_device_uefi_exp(self, get_host_details_mock,
                                                 _uefi_boot_mode_mock,
                                                 boot_devices_mock):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        _uefi_boot_mode_mock.return_value = True
        devices = ris_outputs.UEFI_BOOT_DEVICE_ORDER_HDD
        sources = json.loads(ris_outputs.UEFI_BOOT_SOURCES_ERR)
        boot_devices_mock.return_value = sources, devices

        self.assertRaises(exception.IloError,
                          self.client.get_persistent_boot_device)
        get_host_details_mock.assert_called_once_with()
        _uefi_boot_mode_mock.assert_called_once_with()
        boot_devices_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_update_persistent_boot')
    def test_update_persistent_boot_cdrom(self, update_persistent_boot_mock):
        self.client.update_persistent_boot(['cdrom'])
        update_persistent_boot_mock.assert_called_once_with(
            ['cdrom'], mac=None, persistent=True)

    @mock.patch.object(ris.RISOperations, '_update_persistent_boot')
    def test_update_persistent_boot_iscsi(self, update_persistent_boot_mock):
        self.client.update_persistent_boot(['ISCSI'], '9cb654797870')
        update_persistent_boot_mock.assert_called_once_with(
            ['ISCSI'], mac='9cb654797870', persistent=True)

    @mock.patch.object(ris.RISOperations, '_update_persistent_boot')
    def test_update_persistent_boot_exc(self, update_persistent_boot_mock):
        self.assertRaises(exception.IloError,
                          self.client.update_persistent_boot, ['fake'])
        self.assertFalse(update_persistent_boot_mock.called)

    def test_update_firmware_throws_error_for_invalid_component(self):
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          self.client.update_firmware,
                          'fw_file_url',
                          'invalid_component')

    @mock.patch.object(ris.RISOperations,
                       '_get_firmware_update_service_resource',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, '_rest_post', autospec=True)
    @mock.patch.object(ris.common, 'wait_for_ris_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress',
                       autospec=True)
    def test_update_firmware(
            self, get_firmware_update_progress_mock,
            wait_for_ris_firmware_update_to_complete_mock, _rest_post_mock,
            _get_firmware_update_service_resource_mock):
        # | GIVEN |
        _rest_post_mock.return_value = 200, 'some-headers', 'response'
        get_firmware_update_progress_mock.return_value = 'COMPLETED', 100
        # | WHEN |
        self.client.update_firmware('fw_file_url', 'ilo')
        # | THEN |
        _get_firmware_update_service_resource_mock.assert_called_once_with(
            self.client)
        _rest_post_mock.assert_called_once_with(
            self.client, mock.ANY, None, {'Action': 'InstallFromURI',
                                          'FirmwareURI': 'fw_file_url',
                                          })
        wait_for_ris_firmware_update_to_complete_mock.assert_called_once_with(
            self.client)
        get_firmware_update_progress_mock.assert_called_once_with(
            self.client)

    @mock.patch.object(
        ris.RISOperations, '_get_firmware_update_service_resource',
        autospec=True)
    @mock.patch.object(ris.RISOperations, '_rest_post', autospec=True)
    def test_update_firmware_throws_if_post_operation_fails(
            self, _rest_post_mock, _get_firmware_update_service_resource_mock):
        # | GIVEN |
        _rest_post_mock.return_value = 500, 'some-headers', 'response'
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError,
                          self.client.update_firmware,
                          'fw_file_url',
                          'cpld')

    @mock.patch.object(ris.RISOperations,
                       '_get_firmware_update_service_resource',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, '_rest_post', autospec=True)
    @mock.patch.object(ris.common, 'wait_for_ris_firmware_update_to_complete',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, 'get_firmware_update_progress',
                       autospec=True)
    def test_update_firmware_throws_if_error_occurs_in_update(
            self, get_firmware_update_progress_mock,
            wait_for_ris_firmware_update_to_complete_mock, _rest_post_mock,
            _get_firmware_update_service_resource_mock):
        # | GIVEN |
        _rest_post_mock.return_value = 200, 'some-headers', 'response'
        get_firmware_update_progress_mock.return_value = 'ERROR', 0
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError,
                          self.client.update_firmware,
                          'fw_file_url',
                          'ilo')

    @mock.patch.object(ris.RISOperations,
                       '_get_firmware_update_service_resource',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, '_rest_get', autospec=True)
    def test_get_firmware_update_progress(
            self, _rest_get_mock,
            _get_firmware_update_service_resource_mock):
        # | GIVEN |
        _rest_get_mock.return_value = (200, 'some-headers',
                                       {'State': 'COMPLETED',
                                        'ProgressPercent': 100})
        # | WHEN |
        state, percent = self.client.get_firmware_update_progress()
        # | THEN |
        _get_firmware_update_service_resource_mock.assert_called_once_with(
            self.client)
        _rest_get_mock.assert_called_once_with(self.client, mock.ANY)
        self.assertTupleEqual((state, percent), ('COMPLETED', 100))

    @mock.patch.object(ris.RISOperations,
                       '_get_firmware_update_service_resource',
                       autospec=True)
    @mock.patch.object(ris.RISOperations, '_rest_get', autospec=True)
    def test_get_firmware_update_progress_throws_if_get_operation_fails(
            self, _rest_get_mock, _get_firmware_update_service_resource_mock):
        # | GIVEN |
        _rest_get_mock.return_value = 500, 'some-headers', 'response'
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError,
                          self.client.get_firmware_update_progress)

    @mock.patch.object(ris.RISOperations, 'get_host_power_status')
    def test_set_host_power_no_change(self, host_power_status_mock):
        host_power_status_mock.return_value = 'ON'
        self.client.set_host_power('on')
        self.assertTrue(host_power_status_mock.called)

    @mock.patch.object(ris.RISOperations, 'get_host_power_status')
    def test_set_host_power_exc(self, host_power_status_mock):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client.set_host_power, 'invalid')

    @mock.patch.object(ris.RISOperations, '_perform_power_op')
    @mock.patch.object(ris.RISOperations, 'get_host_power_status')
    def test_set_host_power_change(self, host_power_status_mock,
                                   perform_power_op_mock):
        host_power_status_mock.return_value = 'ON'
        self.client.set_host_power('off')
        host_power_status_mock.assert_called_once_with()
        perform_power_op_mock.assert_called_once_with('ForceOff')

    @mock.patch.object(ris.RISOperations, '_perform_power_op')
    def test_reset_server(self, mock_perform_power):
        self.client.reset_server()
        mock_perform_power.assert_called_once_with("ForceRestart")

    @mock.patch.object(ris.RISOperations, '_press_pwr_btn')
    def test_hold_pwr_btn(self, press_pwr_btn_mock):
        self.client.hold_pwr_btn()
        press_pwr_btn_mock.assert_called_once_with(pushType="PressAndHold")

    @mock.patch.object(ris.RISOperations, '_press_pwr_btn')
    def test_press_pwr_btn(self, press_pwr_btn_mock):
        self.client.hold_pwr_btn()
        press_pwr_btn_mock.assert_called_once_with(pushType="PressAndHold")


class TestRISOperationsPrivateMethods(testtools.TestCase):

    def setUp(self):
        super(TestRISOperationsPrivateMethods, self).setUp()
        self.client = ris.RISOperations("1.2.3.4", "admin", "Admin")

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__is_boot_mode_uefi_uefi(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'UEFI'
        result = self.client._is_boot_mode_uefi()
        self.assertTrue(result)

    @mock.patch.object(ris.RISOperations, 'get_current_boot_mode')
    def test__is_boot_mode_uefi_bios(self, get_current_boot_mode_mock):
        get_current_boot_mode_mock.return_value = 'LEGACY'
        result = self.client._is_boot_mode_uefi()
        self.assertFalse(result)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test___change_bios_setting(self, check_bios_mock, patch_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        properties = {'fake-property': 'fake-value'}
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client._change_bios_setting(properties)
        check_bios_mock.assert_called_once_with(properties.keys())
        patch_mock.assert_called_once_with(bios_uri, {}, properties)

    @mock.patch.object(ris.RISOperations, '_validate_if_patch_supported')
    @mock.patch.object(ris.RISOperations, '_operation_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_settings_resource')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test___change_bios_setting_fail(self, check_bios_mock, patch_mock,
                                        settings_mock, op_mock,
                                        validate_mock):
        bios_uri = '/rest/v1/systems/1/bios/Settings'
        properties = {'fake-property': 'fake-value'}
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        op_mock.return_value = False
        settings_mock.return_value = (ris_outputs.GET_HEADERS,
                                      bios_uri, settings)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client._change_bios_setting,
                          properties)
        check_bios_mock.assert_called_once_with(properties.keys())
        op_mock.assert_called_once_with(ris_outputs.GET_HEADERS, 'PATCH')
        settings_mock.assert_called_once_with(settings)
        patch_mock.assert_called_once_with(bios_uri, {}, properties)

    @mock.patch.object(ris.RISOperations, '_validate_if_patch_supported')
    @mock.patch.object(ris.RISOperations, '_get_iscsi_settings_resource')
    @mock.patch.object(ris.RISOperations, '_operation_allowed')
    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__check_iscsi_rest_patch_allowed(self, check_bios_mock, get_mock,
                                             op_mock, settings_mock,
                                             validate_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        iscsi_uri = '/rest/v1/systems/1/bios/iScsi'
        iscsi_settings = json.loads(ris_outputs.GET_ISCSI_SETTINGS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 iscsi_settings)
        op_mock.return_value = False
        iscsi_settings_uri = '/rest/v1/systems/1/bios/iScsi/Settings'
        settings_mock.return_value = (ris_outputs.GET_HEADERS,
                                      iscsi_settings_uri, iscsi_settings)
        self.client._check_iscsi_rest_patch_allowed()
        check_bios_mock.assert_called_once_with()
        get_mock.assert_called_once_with(iscsi_uri)
        op_mock.assert_called_once_with(ris_outputs.GET_HEADERS, 'PATCH')
        settings_mock.assert_called_once_with(iscsi_settings)
        validate_mock.assert_called_once_with(ris_outputs.GET_HEADERS,
                                              iscsi_settings_uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__check_iscsi_rest_patch_allowed_fail(self, check_bios_mock,
                                                  get_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        iscsi_uri = '/rest/v1/systems/1/bios/iScsi'
        iscsi_settings = json.loads(ris_outputs.GET_ISCSI_SETTINGS)
        get_mock.return_value = (202, ris_outputs.GET_HEADERS,
                                 iscsi_settings)
        self.assertRaises(exception.IloError,
                          self.client._check_iscsi_rest_patch_allowed)
        check_bios_mock.assert_called_once_with()
        get_mock.assert_called_once_with(iscsi_uri)

    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__check_iscsi_rest_patch_allowed_not_found(self, check_bios_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        settings = json.loads(ris_outputs.GET_BASE_CONFIG)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, settings)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._check_iscsi_rest_patch_allowed)
        check_bios_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_iscsi_rest_patch_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_mappings_resource')
    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__change_iscsi_settings(self, check_bios_mock, boot_mock,
                                    mappings_mock, check_iscsi_mock,
                                    patch_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        mappings_mock.return_value = map_settings
        iscsi_uri = '/rest/v1/systems/1/bios/iScsi/Settings'
        properties = {'iSCSITargetName':
                      'iqn.2011-07.com.example.server:test1',
                      'iSCSIBootLUN': '1',
                      'iSCSITargetIpAddress': '10.10.1.30',
                      'iSCSITargetTcpPort': 3260}
        settings = json.loads(ris_outputs.GET_ISCSI_PATCH)
        check_iscsi_mock.return_value = iscsi_uri
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client._change_iscsi_settings('C4346BB7EF30', properties)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        mappings_mock.assert_called_once_with(bios_settings)
        check_iscsi_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(iscsi_uri, None, settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_mappings_resource')
    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__change_iscsi_settings_invalid_mac(self, check_bios_mock,
                                                boot_mock,
                                                mappings_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        mappings_mock.return_value = map_settings
        self.assertRaises(exception.IloInvalidInputError,
                          self.client._change_iscsi_settings, 'C456', {})
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        mappings_mock.assert_called_once_with(bios_settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_mappings_resource')
    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__change_iscsi_settings_invalid_mapping(self, check_bios_mock,
                                                    boot_mock,
                                                    mappings_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        mappings_mock.return_value = map_settings
        self.assertRaises(exception.IloError,
                          self.client._change_iscsi_settings,
                          'C4346BB7EF31', {})
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        mappings_mock.assert_called_once_with(bios_settings)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_check_iscsi_rest_patch_allowed')
    @mock.patch.object(ris.RISOperations, '_get_bios_mappings_resource')
    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__change_iscsi_settings_fail(self, check_bios_mock, boot_mock,
                                         mappings_mock, check_iscsi_mock,
                                         patch_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        mappings_mock.return_value = map_settings
        iscsi_uri = '/rest/v1/systems/1/bios/iScsi/Settings'
        properties = {'iSCSITargetName':
                      'iqn.2011-07.com.example.server:test1',
                      'iSCSIBootLUN': '1',
                      'iSCSITargetIpAddress': '10.10.1.30',
                      'iSCSITargetTcpPort': 3260}
        settings = json.loads(ris_outputs.GET_ISCSI_PATCH)
        check_iscsi_mock.return_value = iscsi_uri
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client._change_iscsi_settings,
                          'C4346BB7EF30', properties)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        mappings_mock.assert_called_once_with(bios_settings)
        check_iscsi_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(iscsi_uri, None, settings)

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings(self, get_details_mock, patch_mock,
                                           get_bios_mock, change_bios_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        get_bios_mock.return_value = "test"
        secure_boot_uri = '/rest/v1/Systems/1/SecureBoot'
        bios_dict = {'CustomPostMessage': 'test '}
        patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_POST_RESPONSE)
        self.client._change_secure_boot_settings('fake-property',
                                                 'fake-value')
        get_details_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(secure_boot_uri, None,
                                           {'fake-property': 'fake-value'})
        get_bios_mock.assert_called_once_with('CustomPostMessage')
        change_bios_mock.assert_called_once_with(bios_dict)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings_not_supported(self,
                                                         get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        del host_response['Oem']['Hp']['links']['SecureBoot']
        get_details_mock.return_value = host_response
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._change_secure_boot_settings,
                          'fake-property', 'fake-value')
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test___change_secure_boot_settings_fail(self, get_details_mock,
                                                patch_mock):
        host_details = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_details_mock.return_value = host_details
        secure_boot_uri = '/rest/v1/Systems/1/SecureBoot'
        patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                   ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client._change_secure_boot_settings,
                          'fake-property', 'fake-value')
        get_details_mock.assert_called_once_with()
        patch_mock.assert_called_once_with(secure_boot_uri, None,
                                           {'fake-property': 'fake-value'})

    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__get_bios_setting(self, bios_mock):
        bios_mock.return_value = ('fake', 'fake',
                                  json.loads(ris_outputs.GET_BIOS_SETTINGS))
        result = self.client._get_bios_setting('BootMode')
        bios_mock.assert_called_once_with(['BootMode'])
        self.assertEqual(result, 'Uefi')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 settings)
        self.client._get_bios_settings_resource(settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Settings')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource_key_error(self, get_mock):
        settings = json.loads(ris_outputs.GET_BASE_CONFIG)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_settings_resource,
                          settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_settings_resource_fail(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        settings_uri = '/rest/v1/systems/1/bios/Settings'
        get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                 settings)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_settings_resource,
                          settings)
        get_mock.assert_called_once_with(settings_uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_boot_resource(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 boot_settings)
        self.client._get_bios_boot_resource(settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Boot')

    def test__get_bios_boot_resource_key_error(self):
        settings = json.loads(ris_outputs.GET_BASE_CONFIG)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_bios_boot_resource,
                          settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_boot_resource_fail(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        get_mock.return_value = (201, ris_outputs.GET_HEADERS,
                                 boot_settings)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_boot_resource,
                          settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Boot')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_mappings_resource(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 map_settings)
        self.client._get_bios_mappings_resource(settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Mappings')

    def test__get_bios_mappings_resource_key_error(self):
        settings = json.loads(ris_outputs.GET_BASE_CONFIG)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_bios_mappings_resource,
                          settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_bios_mappings_resource_fail(self, get_mock):
        settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        map_settings = json.loads(ris_outputs.GET_BIOS_MAPPINGS)
        get_mock.return_value = (201, ris_outputs.GET_HEADERS,
                                 map_settings)
        self.assertRaises(exception.IloError,
                          self.client._get_bios_mappings_resource,
                          settings)
        get_mock.assert_called_once_with('/rest/v1/systems/1/bios/Mappings')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_iscsi_settings_resource(self, get_mock):
        settings = json.loads(ris_outputs.GET_ISCSI_SETTINGS)
        get_mock.return_value = (200, ris_outputs.GET_HEADERS, settings)
        self.client._get_iscsi_settings_resource(settings)
        get_mock.assert_called_once_with(
            '/rest/v1/systems/1/bios/iScsi/Settings')

    def test__get_iscsi_settings_resource_key_error(self):
        settings = json.loads(ris_outputs.GET_ISCSI_PATCH)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_iscsi_settings_resource,
                          settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    def test__get_iscsi_settings_resource_fail(self, get_mock):
        settings = json.loads(ris_outputs.GET_ISCSI_SETTINGS)
        get_mock.return_value = (201, ris_outputs.GET_HEADERS, settings)
        self.assertRaises(exception.IloError,
                          self.client._get_iscsi_settings_resource,
                          settings)
        get_mock.assert_called_once_with(
            '/rest/v1/systems/1/bios/iScsi/Settings')

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test__get_vm_device_status(self,
                                   collection_mock,
                                   ilo_details_mock,
                                   get_mock):
        manager_uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)

        ilo_details_mock.return_value = (manager_data, manager_uri)

        collection_item = json.loads(ris_outputs.RESP_VM_STATUS_FLOPPY_EMPTY)
        vmedia_uri = '/rest/v1/Managers/1/VirtualMedia'
        member_uri = '/rest/v1/Managers/1/VirtualMedia/1'
        collection_mock.return_value = [(200, None, collection_item,
                                         member_uri)]
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 collection_item)
        self.client._get_vm_device_status('FLOPPY')
        ilo_details_mock.assert_called_once_with()
        collection_mock.assert_called_once_with(vmedia_uri)
        get_mock.assert_called_once_with(member_uri)

    def test__get_vm_device_status_invalid_device(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client._get_vm_device_status, device='FOO')

    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    def test__get_vm_device_status_vmedia_not_supported(self,
                                                        ilo_details_mock):
        manager_uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS_NO_VMEDIA)

        ilo_details_mock.return_value = (manager_data, manager_uri)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_vm_device_status, device='FLOPPY')

        ilo_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test__get_vm_device_status_fail(self,
                                        collection_mock,
                                        ilo_details_mock,
                                        get_mock):
        manager_uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)

        ilo_details_mock.return_value = (manager_data, manager_uri)

        collection_item = json.loads(ris_outputs.RESP_VM_STATUS_FLOPPY_EMPTY)
        vmedia_uri = '/rest/v1/Managers/1/VirtualMedia'
        member_uri = '/rest/v1/Managers/1/VirtualMedia/1'
        collection_mock.return_value = [(200, None, collection_item,
                                         member_uri)]
        get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                 ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client._get_vm_device_status, device='FLOPPY')
        ilo_details_mock.assert_called_once_with()
        collection_mock.assert_called_once_with(vmedia_uri)
        get_mock.assert_called_once_with(member_uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_ilo_details')
    @mock.patch.object(ris.RISOperations, '_get_collection')
    def test__get_vm_device_status_device_missing(self,
                                                  collection_mock,
                                                  ilo_details_mock,
                                                  get_mock):
        manager_uri = '/rest/v1/Managers/1'
        manager_data = json.loads(ris_outputs.GET_MANAGER_DETAILS)

        ilo_details_mock.return_value = (manager_data, manager_uri)

        collection_item = json.loads(ris_outputs.RESP_VM_STATUS_CDROM_MISSING)
        vmedia_uri = '/rest/v1/Managers/1/VirtualMedia'
        member_uri = '/rest/v1/Managers/1/VirtualMedia/2'
        collection_mock.return_value = [(200, None, collection_item,
                                         member_uri)]
        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 collection_item)
        self.assertRaises(exception.IloError,
                          self.client._get_vm_device_status, device='CDROM')
        ilo_details_mock.assert_called_once_with()
        collection_mock.assert_called_once_with(vmedia_uri)
        get_mock.assert_called_once_with(member_uri)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test__update_persistent_boot_once(self, rest_patch_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': 'Once',
                                     'BootSourceOverrideTarget': 'Cd'}
        rest_patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                        ris_outputs.REST_POST_RESPONSE)
        self.client._update_persistent_boot(['cdrom'], mac=None,
                                            persistent=False)
        rest_patch_mock.assert_called_once_with(systems_uri, None,
                                                new_boot_settings)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test__update_persistent_boot_for_continuous(self, rest_patch_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': 'Continuous',
                                     'BootSourceOverrideTarget': 'Cd'}
        rest_patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                        ris_outputs.REST_POST_RESPONSE)
        self.client._update_persistent_boot(['cdrom'], mac=None,
                                            persistent=True)
        rest_patch_mock.assert_called_once_with(systems_uri, None,
                                                new_boot_settings)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test__update_persistent_boot_for_UefiShell(self, rest_patch_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': 'Continuous',
                                     'BootSourceOverrideTarget': 'UefiShell'}
        rest_patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                        ris_outputs.REST_POST_RESPONSE)
        self.client._update_persistent_boot(['UefiShell'], mac=None,
                                            persistent=True)
        rest_patch_mock.assert_called_once_with(systems_uri, None,
                                                new_boot_settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test__update_persistent_boot_for_iscsi_mac_valid(self, rest_patch_mock,
                                                         check_bios_mock,
                                                         boot_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        systems_uri = '/rest/v1/Systems/1'
        new1_boot_settings = {}
        new1_boot_settings['Boot'] = {'UefiTargetBootSourceOverride':
                                      u'NIC.LOM.1.1.iSCSI'}
        new2_boot_settings = {}
        new2_boot_settings['Boot'] = {'BootSourceOverrideEnabled':
                                      'Continuous', 'BootSourceOverrideTarget':
                                      'UefiTarget'}

        rest_patch_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                        ris_outputs.REST_POST_RESPONSE)
        calls = [mock.call(systems_uri, None, new1_boot_settings),
                 mock.call(systems_uri, None, new2_boot_settings)]
        self.client._update_persistent_boot(['ISCSI'], mac='C4346BB7EF30',
                                            persistent=True)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        rest_patch_mock.assert_has_calls(calls)

    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__update_persistent_boot_for_iscsi_mac_invalid(self,
                                                           check_bios_mock,
                                                           boot_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        self.assertRaises(exception.IloInvalidInputError,
                          self.client._update_persistent_boot, ['ISCSI'],
                          mac='234343553', persistent=True)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)

    def test__update_persistent_boot_for_iscsi_mac_none(self):
        self.assertRaises(exception.IloInvalidInputError,
                          self.client._update_persistent_boot, ['ISCSI'],
                          mac=None, persistent=True)

    @mock.patch.object(ris.RISOperations, '_rest_patch')
    def test__update_persistent_boot_fail(self, rest_patch_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': 'Continuous',
                                     'BootSourceOverrideTarget': 'FakeDevice'}
        rest_patch_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                        ris_outputs.REST_POST_RESPONSE)
        self.assertRaises(exception.IloError,
                          self.client._update_persistent_boot,
                          ['FakeDevice'], mac=None, persistent=True)
        rest_patch_mock.assert_called_once_with(systems_uri, None,
                                                new_boot_settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__get_persistent_boot_devices_no_boot_order(self,
                                                        check_bios_mock,
                                                        boot_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.BOOT_PERS_DEV_ORDER_MISSING)
        boot_mock.return_value = boot_settings
        self.assertRaises(exception.IloError,
                          self.client._get_persistent_boot_devices)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__get_persistent_boot_devices(self, check_bios_mock, boot_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.GET_BIOS_BOOT)
        boot_mock.return_value = boot_settings
        exp_boot_src = json.loads(ris_outputs.UEFI_BootSources)
        exp_boot_order = ris_outputs.UEFI_PERS_BOOT_DEVICES
        boot_src, boot_order = self.client._get_persistent_boot_devices()
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)
        self.assertEqual(boot_src, exp_boot_src)
        self.assertEqual(boot_order, exp_boot_order)

    @mock.patch.object(ris.RISOperations, '_get_bios_boot_resource')
    @mock.patch.object(ris.RISOperations, '_check_bios_resource')
    def test__get_persistent_boot_devices_no_bootsources(self,
                                                         check_bios_mock,
                                                         boot_mock):
        bios_uri = '/rest/v1/systems/1/bios'
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        check_bios_mock.return_value = (ris_outputs.GET_HEADERS,
                                        bios_uri, bios_settings)
        boot_settings = json.loads(ris_outputs.UEFI_BOOTSOURCES_MISSING)
        boot_mock.return_value = boot_settings
        self.assertRaises(exception.IloError,
                          self.client._get_persistent_boot_devices)
        check_bios_mock.assert_called_once_with()
        boot_mock.assert_called_once_with(bios_settings)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test__get_pci_devices(self, get_host_details_mock, get_mock):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        pci_uri = '/rest/v1/Systems/1/PCIDevices'
        pci_device_list = json.loads(ris_outputs.PCI_DEVICE_DETAILS)

        get_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                 pci_device_list)
        self.client._get_pci_devices()
        get_mock.assert_called_once_with(pci_uri)

    @mock.patch.object(ris.RISOperations, '_rest_get')
    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test__get_pci_devices_fail(self, get_host_details_mock,
                                   get_mock):
        system_data = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        get_host_details_mock.return_value = system_data
        pci_uri = '/rest/v1/Systems/1/PCIDevices'
        pci_device_list = json.loads(ris_outputs.PCI_DEVICE_DETAILS)
        get_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                 pci_device_list)
        self.assertRaises(exception.IloError,
                          self.client._get_pci_devices)
        get_mock.assert_called_once_with(pci_uri)

    @mock.patch.object(ris.RISOperations, '_get_host_details')
    def test__get_pci_devices_not_supported(self, get_details_mock):
        host_response = json.loads(ris_outputs.RESPONSE_BODY_FOR_REST_OP)
        del host_response['Oem']['Hp']['links']['PCIDevices']
        get_details_mock.return_value = host_response
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_pci_devices)
        get_details_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, '_get_pci_devices')
    def test__get_gpu_pci_devices(self, pci_mock):
        pci_mock.return_value = json.loads(ris_outputs.PCI_DEVICE_DETAILS)
        pci_gpu_list = self.client._get_gpu_pci_devices()
        self.assertEqual(pci_gpu_list, json.loads(ris_outputs.PCI_GPU_LIST))
        self.assertTrue(pci_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_pci_devices')
    def test__get_gpu_pci_devices_returns_empty(self, pci_mock):
        pci_response = json.loads(ris_outputs.PCI_DEVICE_DETAILS_NO_GPU)
        pci_mock.return_value = pci_response
        pci_gpu_list = self.client._get_gpu_pci_devices()
        self.assertEqual(len(pci_gpu_list), 0)
        self.assertTrue(pci_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_pci_devices')
    def test__get_gpu_pci_devices_fail_not_supported_error(self, pci_mock):
        msg = ('links/PCIDevices section in ComputerSystem/Oem/Hp'
               ' does not exist')
        pci_mock.side_effect = exception.IloCommandNotSupportedError(msg)
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_gpu_pci_devices)
        self.assertTrue(pci_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_gpu_pci_devices')
    def test__get_number_of_gpu_devices_connected(self, gpu_list_mock):
        gpu_list_mock.return_value = json.loads(ris_outputs.PCI_GPU_LIST)
        expected_gpu_count = {'pci_gpu_devices': 1}
        gpu_count_returned = self.client._get_number_of_gpu_devices_connected()
        self.assertEqual(gpu_count_returned, expected_gpu_count)
        self.assertTrue(gpu_list_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_cpu_virtualization_enabled(self, bios_mock):
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        bios_mock.return_value = bios_settings['ProcVirtualization']
        expected_cpu_vt = True
        cpu_vt_return = self.client._get_cpu_virtualization()
        self.assertEqual(cpu_vt_return, expected_cpu_vt)
        self.assertTrue(bios_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_cpu_virtualization_disabled(self, bios_mock):
        bios_mock.return_value = 'Disable'
        expected_cpu_vt = False
        cpu_vt_return = self.client._get_cpu_virtualization()
        self.assertEqual(cpu_vt_return, expected_cpu_vt)
        self.assertTrue(bios_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_cpu_virtualization_not_supported_error(self, bios_mock):
        msg = ("BIOS Property 'ProcVirtualization' is not supported on this"
               " system")
        bios_mock.side_effect = exception.IloCommandNotSupportedError(msg)
        expected_cpu_vt = False
        cpu_vt_return = self.client._get_cpu_virtualization()
        self.assertEqual(cpu_vt_return, expected_cpu_vt)
        self.assertTrue(bios_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_ilo_details', autospec=True)
    def test__get_firmware_update_service_resource_traverses_manager_as(
            self, _get_ilo_details_mock):
        # | GIVEN |
        manager_mock = mock.MagicMock(spec=dict, autospec=True)
        _get_ilo_details_mock.return_value = (manager_mock, 'some_uri')
        # | WHEN |
        self.client._get_firmware_update_service_resource()
        # | THEN |
        manager_mock.__getitem__.assert_called_once_with('Oem')
        manager_mock.__getitem__().__getitem__.assert_called_once_with('Hp')
        (manager_mock.__getitem__().__getitem__().__getitem__.
         assert_called_once_with('links'))
        (manager_mock.__getitem__().__getitem__().__getitem__().
         __getitem__.assert_called_once_with('UpdateService'))
        (manager_mock.__getitem__().__getitem__().__getitem__().
         __getitem__().__getitem__.assert_called_once_with('href'))

    @mock.patch.object(ris.RISOperations, '_get_ilo_details', autospec=True)
    def test__get_firmware_update_service_resource_throws_if_not_found(
            self, _get_ilo_details_mock):
        # | GIVEN |
        manager_mock = mock.MagicMock(spec=dict)
        _get_ilo_details_mock.return_value = (manager_mock, 'some_uri')
        manager_mock.__getitem__.side_effect = KeyError('not found')
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloCommandNotSupportedError,
                          self.client._get_firmware_update_service_resource)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    def test_press_pwr_btn(self, rest_post_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_pow_settings = {"Action": "PowerButton",
                            "Target": "/Oem/Hp",
                            "PushType": "Press"}
        rest_post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                       ris_outputs.REST_POST_RESPONSE)
        self.client._press_pwr_btn()
        rest_post_mock.assert_called_once_with(systems_uri, None,
                                               new_pow_settings)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    def test_press_pwr_btn_patch_fail(self, rest_post_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_pow_settings = {"Action": "PowerButton",
                            "Target": "/Oem/Hp",
                            "PushType": "Press"}
        rest_post_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                       ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client._press_pwr_btn, 'Press')
        rest_post_mock.assert_called_once_with(systems_uri, None,
                                               new_pow_settings)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    def test_perform_power_op(self, rest_post_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_pow_settings = {"Action": "Reset", "ResetType": "ForceRestart"}
        rest_post_mock.return_value = (200, ris_outputs.GET_HEADERS,
                                       ris_outputs.REST_POST_RESPONSE)
        self.client.reset_server()
        rest_post_mock.assert_called_once_with(systems_uri, None,
                                               new_pow_settings)

    @mock.patch.object(ris.RISOperations, '_rest_post')
    def test_perform_power_op_fail(self, rest_post_mock):
        systems_uri = "/rest/v1/Systems/1"
        new_pow_settings = {"Action": "Reset", "ResetType": "ForceRestart"}
        rest_post_mock.return_value = (301, ris_outputs.GET_HEADERS,
                                       ris_outputs.REST_FAILURE_OUTPUT)
        self.assertRaises(exception.IloError,
                          self.client.reset_server)
        rest_post_mock.assert_called_once_with(systems_uri, None,
                                               new_pow_settings)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test__get_tpm_capability_notpresent(self, bios_mock):
        bios_mock.return_value = 'NotPresent'
        expected_out = False
        status = self.client._get_tpm_capability()
        self.assertEqual(expected_out, status)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test__get_tpm_capability_presentdisabled(self, bios_mock):
        bios_mock.return_value = 'PresentDisabled'
        expected_out = True
        status = self.client._get_tpm_capability()
        self.assertEqual(expected_out, status)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test__get_tpm_capability_presentenabled(self, bios_mock):
        bios_mock.return_value = 'PresentEnabled'
        expected_out = True
        status = self.client._get_tpm_capability()
        self.assertEqual(expected_out, status)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test__get_tpm_capability_resource_notpresent(self, bios_mock):
        msg = 'BIOS Property TpmState is not supported on this system.'
        bios_mock.side_effect = exception.IloCommandNotSupportedError(msg)
        expected_out = False
        status = self.client._get_tpm_capability()
        self.assertEqual(expected_out, status)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_nvdimm_n_status_enabled(self, bios_mock):
        bios_settings = json.loads(ris_outputs.GET_BIOS_SETTINGS)
        bios_mock.return_value = bios_settings['NvDimmNMemFunctionality']
        expected_nvdimm_n_status = True
        nvdimm_n_status_return = self.client._get_nvdimm_n_status()
        self.assertEqual(nvdimm_n_status_return, expected_nvdimm_n_status)
        self.assertTrue(bios_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_nvdimm_n_status_disabled(self, bios_mock):
        bios_mock.return_value = 'Disabled'
        expected_nvdimm_n_status = False
        nvdimm_n_status_return = self.client._get_nvdimm_n_status()
        self.assertEqual(nvdimm_n_status_return, expected_nvdimm_n_status)
        self.assertTrue(bios_mock.called)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test___get_nvdimm_n_status_not_supported_error(self, bios_mock):
        msg = ("BIOS Property 'NvDimmNMemFunctionality' is not supported on"
               " this system")
        bios_mock.side_effect = exception.IloCommandNotSupportedError(msg)
        expected_nvdimm_n_status = False
        nvdimm_n_status_return = self.client._get_nvdimm_n_status()
        self.assertEqual(nvdimm_n_status_return, expected_nvdimm_n_status)
        self.assertTrue(bios_mock.called)
