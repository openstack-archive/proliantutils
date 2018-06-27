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
"""Test class for Client Module."""

import mock
import testtools

from proliantutils import exception
from proliantutils.ilo import client
from proliantutils.ilo import ipmi
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.ilo.snmp import snmp_cpqdisk_sizes
from proliantutils.redfish import redfish


class IloClientInitTestCase(testtools.TestCase):

    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(ris, 'RISOperations')
    def test_init(self, ris_mock, ribcl_mock):
        ribcl_obj_mock = mock.MagicMock()
        ribcl_mock.return_value = ribcl_obj_mock
        ribcl_obj_mock.get_product_name.return_value = 'product'

        c = client.IloClient("1.2.3.4", "admin", "Admin",
                             timeout=120,  port=4430,
                             bios_password='foo',
                             cacert='/somewhere')

        ris_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        self.assertEqual(
            {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"},
            c.info)
        self.assertEqual('product', c.model)

    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test_init_for_redfish_with_ribcl_enabled(
            self, redfish_mock, ribcl_mock):
        ribcl_obj_mock = mock.MagicMock()
        ribcl_mock.return_value = ribcl_obj_mock
        ribcl_obj_mock.get_product_name.return_value = 'ProLiant DL180 Gen10'

        c = client.IloClient("1.2.3.4", "admin", "Admin",
                             timeout=120,  port=4430,
                             bios_password='foo',
                             cacert='/somewhere')

        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        redfish_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        self.assertEqual(
            {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"},
            c.info)
        self.assertEqual('ProLiant DL180 Gen10', c.model)
        self.assertIsNotNone(c.redfish)
        self.assertTrue(c.is_ribcl_enabled)
        self.assertFalse(hasattr(c, 'ris'))

    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test_init_for_redfish_with_ribcl_disabled(
            self, redfish_mock, ribcl_mock):
        ribcl_obj_mock = mock.MagicMock()
        ribcl_mock.return_value = ribcl_obj_mock
        ribcl_obj_mock.get_product_name.side_effect = (
            exception.IloError('RIBCL is disabled'))

        c = client.IloClient("1.2.3.4", "admin", "Admin",
                             timeout=120,  port=4430,
                             bios_password='foo',
                             cacert='/somewhere')

        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        redfish_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        self.assertEqual(
            {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"},
            c.info)
        self.assertIsNotNone(c.model)
        self.assertIsNotNone(c.redfish)
        self.assertFalse(c.is_ribcl_enabled)
        self.assertFalse(hasattr(c, 'ris'))

    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test_init_with_use_redfish_only_set(
            self, redfish_mock, ribcl_mock):
        c = client.IloClient("1.2.3.4", "admin", "Admin",
                             timeout=120,  port=4430,
                             bios_password='foo', cacert='/somewhere',
                             use_redfish_only=True)

        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        redfish_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        self.assertEqual(
            {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"},
            c.info)
        self.assertIsNotNone(c.model)
        self.assertIsNotNone(c.redfish)
        self.assertIsNone(c.is_ribcl_enabled)
        self.assertFalse(hasattr(c, 'ris'))
        self.assertTrue(c.use_redfish_only)

    @mock.patch.object(client.IloClient, '_validate_snmp')
    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(ris, 'RISOperations')
    def test_init_snmp(self, ris_mock, ribcl_mock, snmp_mock):
        ribcl_obj_mock = mock.MagicMock()
        ribcl_mock.return_value = ribcl_obj_mock
        ribcl_obj_mock.get_product_name.return_value = 'product'
        snmp_credentials = {'auth_user': 'user',
                            'auth_protocol': 'SHA',
                            'auth_prot_pp': '1234',
                            'priv_protocol': 'AES',
                            'auth_priv_pp': '4321',
                            'snmp_inspection': 'true'}
        c = client.IloClient("1.2.3.4", "admin", "Admin",
                             timeout=120,  port=4430,
                             bios_password='foo',
                             cacert='/somewhere',
                             snmp_credentials=snmp_credentials)

        ris_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        self.assertEqual(
            {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"},
            c.info)
        self.assertEqual('product', c.model)
        self.assertTrue(snmp_mock.called)

    @mock.patch.object(client.IloClient, '_validate_snmp')
    @mock.patch.object(ribcl, 'RIBCLOperations')
    @mock.patch.object(ris, 'RISOperations')
    def test_init_snmp_raises(self, ris_mock, ribcl_mock, snmp_mock):
        ribcl_obj_mock = mock.MagicMock()
        ribcl_mock.return_value = ribcl_obj_mock
        ribcl_obj_mock.get_product_name.return_value = 'product'
        snmp_mock.side_effect = exception.IloInvalidInputError("msg")
        snmp_credentials = {'auth_user': 'user',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': 'true'}
        self.assertRaises(exception.IloInvalidInputError, client.IloClient,
                          "1.2.3.4", "admin", "Admin",
                          timeout=120,  port=4430,
                          bios_password='foo',
                          cacert='/somewhere',
                          snmp_credentials=snmp_credentials)

        ris_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", bios_password='foo',
            cacert='/somewhere')
        ribcl_mock.assert_called_once_with(
            "1.2.3.4", "admin", "Admin", 120, 4430, cacert='/somewhere')
        self.assertTrue(snmp_mock.called)


class IloClientSNMPValidateTestCase(testtools.TestCase):

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_validate_snmp(self, product_mock):
        cred = {'auth_user': 'user',
                'auth_protocol': 'SHA',
                'priv_protocol': 'AES',
                'auth_prot_pp': '1234',
                'auth_priv_pp': '4321',
                'snmp_inspection': True}
        self.snmp_credentials = cred
        self.client = client.IloClient("1.2.3.4", "admin", "Admin",
                                       snmp_credentials=cred)
        self.assertEqual(self.client.snmp_credentials, cred)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_validate_snmp_fail_auth_priv_pp_missing(self, product_mock):
        cred = {'auth_user': 'user',
                'auth_protocol': 'SHA',
                'priv_protocol': 'AES',
                'auth_prot_pp': '1234',
                'snmp_inspection': True}
        self.assertRaises(exception.IloInvalidInputError,
                          client.IloClient,
                          "1.2.3.4", "admin", "Admin",
                          snmp_credentials=cred)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_validate_snmp_auth_prot_pp_missing(self, product_mock):
        cred = {'auth_user': 'user',
                'auth_protocol': 'SHA',
                'priv_protocol': 'AES',
                'auth_priv_pp': '4321',
                'snmp_inspection': True}
        self.assertRaises(exception.IloInvalidInputError,
                          client.IloClient,
                          "1.2.3.4", "admin", "Admin",
                          snmp_credentials=cred)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_validate_snmp_auth_prot_priv_prot_missing(self, product_mock):
        cred = {'auth_user': 'user',
                'auth_prot_pp': '1234',
                'auth_priv_pp': '4321',
                'snmp_inspection': True}
        self.client = client.IloClient("1.2.3.4", "admin", "Admin",
                                       snmp_credentials=cred)
        self.assertEqual(self.client.snmp_credentials, cred)

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_validate_snmp_auth_user_missing(self, product_mock):
        cred = {'auth_protocol': 'SHA',
                'priv_protocol': 'AES',
                'auth_priv_pp': '4321',
                'auth_prot_pp': '1234',
                'snmp_inspection': True}
        self.assertRaises(exception.IloInvalidInputError,
                          client.IloClient,
                          "1.2.3.4", "admin", "Admin",
                          snmp_credentials=cred)


class IloClientTestCase(testtools.TestCase):

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def setUp(self, product_mock):
        super(IloClientTestCase, self).setUp()
        product_mock.return_value = 'Gen8'
        self.client = client.IloClient("1.2.3.4", "admin", "Admin")

    @mock.patch.object(ribcl.RIBCLOperations, 'get_all_licenses')
    def test__call_method_ribcl(self, license_mock):
        self.client._call_method('get_all_licenses')
        license_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, 'get_host_power_status')
    def test__call_method_ris(self, power_mock):
        self.client.model = 'Gen9'
        self.client._call_method('get_host_power_status')
        power_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'reset_ilo')
    def test__call_method_gen9_ribcl(self, ilo_mock):
        self.client.model = 'Gen9'
        self.client._call_method('reset_ilo')
        ilo_mock.assert_called_once_with()

    """
    Testing ``_call_method`` with Redfish support.

    Testing the redfish methods based on the following scenarios,
    which are depicted in this table::

      redfish  |  ribcl   | method implemented | name of test method
    supported? | enabled? |    on redfish?     |
    ===========|==========|====================|=============================
       true    |   true   |      true          | test__call_method_redfish_1
       true    |   true   |      false         | test__call_method_redfish_2
       true    |   false  |      true          | test__call_method_redfish_3
       true    |   false  |      false         | test__call_method_redfish_4
    ===========|==========|====================|=============================
    """
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test__call_method_redfish_1(self, redfish_mock,
                                    ribcl_product_name_mock):
        ribcl_product_name_mock.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "admin", "secret")
        redfish_get_host_power_mock = (redfish.RedfishOperations.return_value.
                                       get_host_power_status)

        self.client._call_method('get_host_power_status')
        redfish_get_host_power_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(redfish, 'RedfishOperations')
    @mock.patch.object(ribcl.RIBCLOperations, 'reset_ilo')
    def test__call_method_redfish_2(self, ribcl_reset_ilo_mock,
                                    redfish_mock, ribcl_product_name_mock):
        ribcl_product_name_mock.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "admin", "secret")

        self.client._call_method('reset_ilo')
        ribcl_reset_ilo_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test__call_method_redfish_3(self, redfish_mock,
                                    ribcl_product_name_mock):
        ribcl_product_name_mock.side_effect = (
            exception.IloError('RIBCL is disabled'))
        redfish_mock.return_value.get_product_name.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "admin", "secret")
        redfish_get_host_power_mock = (redfish.RedfishOperations.return_value.
                                       get_host_power_status)

        self.client._call_method('get_host_power_status')
        redfish_get_host_power_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(redfish, 'RedfishOperations')
    def test__call_method_redfish_4(self, redfish_mock,
                                    ribcl_product_name_mock):
        ribcl_product_name_mock.side_effect = (
            exception.IloError('RIBCL is disabled'))
        redfish_mock.return_value.get_product_name.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "admin", "secret")

        self.assertRaises(NotImplementedError,
                          self.client._call_method, 'reset_ilo')

    @mock.patch.object(redfish, 'RedfishOperations',
                       spec_set=True, autospec=True)
    def test__call_method_with_use_redfish_only_set(self, redfish_mock):
        self.client = client.IloClient("1.2.3.4", "admin", "secret",
                                       use_redfish_only=True)
        redfish_get_host_power_mock = (
            redfish.RedfishOperations.return_value.get_host_power_status)

        self.client._call_method('get_host_power_status')
        redfish_get_host_power_mock.assert_called_once_with()

    @mock.patch.object(redfish, 'RedfishOperations',
                       spec_set=True, autospec=True)
    def test__call_method_use_redfish_only_set_but_not_implemented(
            self, redfish_mock):
        self.client = client.IloClient("1.2.3.4", "admin", "secret",
                                       use_redfish_only=True)

        self.assertRaises(NotImplementedError,
                          self.client._call_method, 'reset_ilo')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_http_boot_url(self, call_mock):
        self.client.set_http_boot_url('fake-url')
        call_mock.assert_called_once_with('set_http_boot_url', 'fake-url')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_iscsi_info(self, call_mock):
        self.client.set_iscsi_info('iqn.2011-07.com:example:123',
                                   '1', '10.10.1.23', '3260', 'CHAP',
                                   'user', 'password')
        call_mock.assert_called_once_with('set_iscsi_info',
                                          'iqn.2011-07.com:example:123',
                                          '1', '10.10.1.23', '3260',
                                          'CHAP', 'user', 'password')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_iscsi_boot_info(self, call_mock):
        self.client.set_iscsi_boot_info('aa:bb:cc:dd:ee:ff',
                                        'iqn.2011-07.com:example:123',
                                        '1', '10.10.1.23', '3260', 'CHAP',
                                        'user', 'password')
        call_mock.assert_called_once_with('set_iscsi_info',
                                          'iqn.2011-07.com:example:123',
                                          '1', '10.10.1.23', '3260',
                                          'CHAP', 'user', 'password')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_iscsi_initiator_info(self, call_mock):
        self.client.get_iscsi_initiator_info()
        call_mock.assert_called_once_with('get_iscsi_initiator_info')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_unset_iscsi_info(self, call_mock):
        self.client.unset_iscsi_info()
        call_mock.assert_called_once_with('unset_iscsi_info')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_unset_iscsi_boot_info(self, call_mock):
        self.client.unset_iscsi_boot_info("aa:bb:cc:dd:ee:ff")
        call_mock.assert_called_once_with('unset_iscsi_info')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_iscsi_initiator_info(self, call_mock):
        self.client.set_iscsi_initiator_info('iqn.2011-07.com:example:123')
        call_mock.assert_called_once_with('set_iscsi_initiator_info',
                                          'iqn.2011-07.com:example:123')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_product_name(self, call_mock):
        self.client.get_product_name()
        call_mock.assert_called_once_with('get_product_name')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_all_licenses(self, call_mock):
        self.client.get_all_licenses()
        call_mock.assert_called_once_with('get_all_licenses')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_power_status(self, call_mock):
        self.client.get_host_power_status()
        call_mock.assert_called_once_with('get_host_power_status')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_http_boot_url(self, call_mock):
        self.client.get_http_boot_url()
        call_mock.assert_called_once_with('get_http_boot_url')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_one_time_boot(self, call_mock):
        self.client.get_one_time_boot()
        call_mock.assert_called_once_with('get_one_time_boot')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_vm_status(self, call_mock):
        self.client.get_vm_status('CDROM')
        call_mock.assert_called_once_with('get_vm_status', 'CDROM')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_press_pwr_btn(self, call_mock):
        self.client.press_pwr_btn()
        call_mock.assert_called_once_with('press_pwr_btn')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_reset_server(self, call_mock):
        self.client.reset_server()
        call_mock.assert_called_once_with('reset_server')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_hold_pwr_btn(self, call_mock):
        self.client.hold_pwr_btn()
        call_mock.assert_called_once_with('hold_pwr_btn')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_host_power(self, call_mock):
        self.client.set_host_power('ON')
        call_mock.assert_called_once_with('set_host_power', 'ON')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_one_time_boot(self, call_mock):
        self.client.set_one_time_boot('CDROM')
        call_mock.assert_called_once_with('set_one_time_boot', 'CDROM')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_insert_virtual_media(self, call_mock):
        self.client.insert_virtual_media(url='fake-url', device='FLOPPY')
        call_mock.assert_called_once_with('insert_virtual_media', 'fake-url',
                                          'FLOPPY')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_eject_virtual_media(self, call_mock):
        self.client.eject_virtual_media(device='FLOPPY')
        call_mock.assert_called_once_with('eject_virtual_media', 'FLOPPY')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_vm_status(self, call_mock):
        self.client.set_vm_status(device='FLOPPY', boot_option='BOOT_ONCE',
                                  write_protect='YES')
        call_mock.assert_called_once_with('set_vm_status', 'FLOPPY',
                                          'BOOT_ONCE', 'YES')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_current_boot_mode(self, call_mock):
        self.client.get_current_boot_mode()
        call_mock.assert_called_once_with('get_current_boot_mode')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_pending_boot_mode(self, call_mock):
        self.client.get_pending_boot_mode()
        call_mock.assert_called_once_with('get_pending_boot_mode')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_supported_boot_mode(self, call_mock):
        self.client.get_supported_boot_mode()
        call_mock.assert_called_once_with('get_supported_boot_mode')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_pending_boot_mode(self, call_mock):
        self.client.set_pending_boot_mode('UEFI')
        call_mock.assert_called_once_with('set_pending_boot_mode', 'UEFI')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_persistent_boot_device(self, call_mock):
        self.client.get_persistent_boot_device()
        call_mock.assert_called_once_with('get_persistent_boot_device')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_update_persistent_boot(self, call_mock):
        self.client.update_persistent_boot(['HDD'])
        call_mock.assert_called_once_with('update_persistent_boot', ['HDD'])

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_secure_boot_mode(self, call_mock):
        self.client.get_secure_boot_mode()
        call_mock.assert_called_once_with('get_secure_boot_mode')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_set_secure_boot_mode(self, call_mock):
        self.client.set_secure_boot_mode(True)
        call_mock.assert_called_once_with('set_secure_boot_mode', True)

    @mock.patch.object(client.IloClient, '_call_method')
    def test_reset_secure_boot_keys(self, call_mock):
        self.client.reset_secure_boot_keys()
        call_mock.assert_called_once_with('reset_secure_boot_keys')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_clear_secure_boot_keys(self, call_mock):
        self.client.clear_secure_boot_keys()
        call_mock.assert_called_once_with('clear_secure_boot_keys')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_reset_ilo_credential(self, call_mock):
        self.client.reset_ilo_credential('password')
        call_mock.assert_called_once_with('reset_ilo_credential', 'password')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_reset_ilo(self, call_mock):
        self.client.reset_ilo()
        call_mock.assert_called_once_with('reset_ilo')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_reset_bios_to_default(self, call_mock):
        self.client.reset_bios_to_default()
        call_mock.assert_called_once_with('reset_bios_to_default')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_uuid(self, call_mock):
        self.client.get_host_uuid()
        call_mock.assert_called_once_with('get_host_uuid')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_data(self, call_mock):
        self.client.get_host_health_data('fake-data')
        call_mock.assert_called_once_with('get_host_health_data', 'fake-data')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_present_power_reading(self, call_mock):
        self.client.get_host_health_present_power_reading('fake-data')
        call_mock.assert_called_once_with(
            'get_host_health_present_power_reading', 'fake-data')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_power_supplies(self, call_mock):
        self.client.get_host_health_power_supplies('fake-data')
        call_mock.assert_called_once_with('get_host_health_power_supplies',
                                          'fake-data')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_fan_sensors(self, call_mock):
        self.client.get_host_health_fan_sensors('fake-data')
        call_mock.assert_called_once_with('get_host_health_fan_sensors',
                                          'fake-data')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_temperature_sensors(self, call_mock):
        self.client.get_host_health_temperature_sensors('fake-data')
        call_mock.assert_called_once_with(
            'get_host_health_temperature_sensors', 'fake-data')

    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_host_health_at_a_glance(self, call_mock):
        self.client.get_host_health_at_a_glance('fake-data')
        call_mock.assert_called_once_with('get_host_health_at_a_glance',
                                          'fake-data')

    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ribcl.RIBCLOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_server_capabilities')
    def test_get_server_capabilities(self, cap_mock, maj_min_mock, nic_mock):
        info = {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"}
        str_val = maj_min_mock.return_value = "2.10"
        nic_mock.return_value = '10Gb'
        cap_mock.return_value = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        capabilities = self.client.get_server_capabilities()
        expected_capabilities = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2',
                                 'nic_capacity': '10Gb'}
        cap_mock.assert_called_once_with()
        nic_mock.assert_called_once_with(self.client.info, str_val)
        self.assertEqual(expected_capabilities, capabilities)
        self.assertEqual(info, self.client.info)

    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ribcl.RIBCLOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_server_capabilities')
    def test_get_server_capabilities_no_nic(self, cap_mock, maj_min_mock,
                                            nic_mock):
        info = {'address': "1.2.3.4", 'username': "admin", 'password': "Admin"}
        str_val = maj_min_mock.return_value = '2.10'
        nic_mock.return_value = None
        cap_mock.return_value = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        capabilities = self.client.get_server_capabilities()
        expected_capabilities = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        cap_mock.assert_called_once_with()
        nic_mock.assert_called_once_with(self.client.info, str_val)
        self.assertEqual(expected_capabilities, capabilities)
        self.assertEqual(info, self.client.info)

    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ribcl.RIBCLOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_server_capabilities')
    def test_get_server_capabilities_no_firmware(self, cap_mock, maj_min_mock,
                                                 nic_mock):
        maj_min_mock.return_value = None
        nic_mock.return_value = None
        cap_mock.return_value = {'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        expected_capabilities = {'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        capabilities = self.client.get_server_capabilities()
        self.assertEqual(expected_capabilities, capabilities)
        nic_mock.assert_called_once_with(self.client.info, None)

    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ribcl.RIBCLOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_server_capabilities')
    def test_get_server_capabilities_no_boot_modes(
            self, cap_mock, maj_min_mock, nic_mock):
        maj_min_mock.return_value = None
        nic_mock.return_value = None
        cap_mock.return_value = {'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        expected_capabilities = {'rom_firmware_version': 'x',
                                 'server_model': 'Gen8',
                                 'pci_gpu_devices': '2'}
        capabilities = self.client.get_server_capabilities()
        self.assertEqual(expected_capabilities, capabilities)
        nic_mock.assert_called_once_with(self.client.info, None)

    @mock.patch.object(ris.RISOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ris.RISOperations, 'get_server_capabilities')
    def test_get_server_capabilities_no_nic_Gen9(self, cap_mock, nic_mock,
                                                 mm_mock):
        str_val = mm_mock.return_value = '2.10'
        self.client.model = 'Gen9'
        nic_mock.return_value = None

        cap_mock.return_value = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'pci_gpu_devices': 2,
                                 'secure_boot': 'true'}
        capabilities = self.client.get_server_capabilities()
        cap_mock.assert_called_once_with()
        nic_mock.assert_called_once_with(self.client.info, str_val)
        expected_capabilities = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'pci_gpu_devices': 2,
                                 'secure_boot': 'true'}
        self.assertEqual(expected_capabilities, capabilities)

    @mock.patch.object(ris.RISOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ris.RISOperations, 'get_server_capabilities')
    def test_get_server_capabilities_Gen9(self, cap_mock, nic_mock, mm_mock):
        str_val = mm_mock.return_value = '2.10'
        self.client.model = 'Gen9'
        nic_mock.return_value = '10Gb'
        cap_mock.return_value = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'pci_gpu_devices': 2,
                                 'secure_boot': 'true'}
        capabilities = self.client.get_server_capabilities()
        cap_mock.assert_called_once_with()
        nic_mock.assert_called_once_with(self.client.info, str_val)
        expected_capabilities = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'pci_gpu_devices': 2,
                                 'secure_boot': 'true',
                                 'nic_capacity': '10Gb'}
        self.assertEqual(expected_capabilities, capabilities)

    @mock.patch.object(redfish, 'RedfishOperations')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    @mock.patch.object(ipmi, 'get_nic_capacity')
    def test_get_server_capabilities_Gen10(self, ipmi_mock,
                                           ribcl_product_name_mock,
                                           redfish_mock):
        ribcl_product_name_mock.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "admin", "secret")
        cap_mock = (redfish_mock.return_value.get_server_capabilities)
        self.client.get_server_capabilities()
        self.assertFalse(ipmi_mock.called)
        self.assertTrue(cap_mock.called)

    @mock.patch.object(ris.RISOperations,
                       'get_ilo_firmware_version_as_major_minor')
    @mock.patch.object(ribcl.RIBCLOperations, 'get_host_health_data')
    @mock.patch.object(ris.RISOperations,
                       '_get_number_of_gpu_devices_connected')
    @mock.patch.object(ipmi, 'get_nic_capacity')
    @mock.patch.object(ris.RISOperations, 'get_server_capabilities')
    def test_get_server_capabilities_no_boot_modes_Gen9(
            self, cap_mock, nic_mock, gpu_mock,
            host_mock, mm_mock):
        str_val = mm_mock.return_value = '2.10'
        self.client.model = 'Gen9'
        nic_mock.return_value = None
        gpu_mock.return_value = None
        cap_mock.return_value = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'secure_boot': 'true'}
        capabilities = self.client.get_server_capabilities()
        cap_mock.assert_called_once_with()
        nic_mock.assert_called_once_with(self.client.info, str_val)
        expected_capabilities = {'ilo_firmware_version': '2.10',
                                 'rom_firmware_version': 'x',
                                 'server_model': 'Gen9',
                                 'secure_boot': 'true'}
        self.assertEqual(expected_capabilities, capabilities)

    @mock.patch.object(client.IloClient, '_call_method')
    def test_activate_license(self, call_mock):
        self.client.activate_license('fake-key')
        call_mock.assert_called_once_with('activate_license', 'fake-key')

    @mock.patch.object(ris.RISOperations, 'eject_virtual_media')
    def test_eject_virtual_media_gen9(self, eject_virtual_media_mock):
        self.client.model = 'Gen9'
        self.client.eject_virtual_media(device='FLOPPY')
        eject_virtual_media_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ribcl.RIBCLOperations, 'eject_virtual_media')
    def test_eject_virtual_media_gen8(self, eject_virtual_media_mock):
        self.client.model = 'Gen8'
        self.client.eject_virtual_media(device='FLOPPY')
        eject_virtual_media_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ris.RISOperations, 'get_vm_status')
    def test_get_vm_status_gen9(self, get_vm_status_mock):
        self.client.model = 'Gen9'
        self.client.get_vm_status(device='FLOPPY')
        get_vm_status_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ribcl.RIBCLOperations, 'get_vm_status')
    def test_get_vm_status_gen8(self, get_vm_status_mock):
        self.client.model = 'Gen8'
        self.client.get_vm_status(device='FLOPPY')
        get_vm_status_mock.assert_called_once_with('FLOPPY')

    @mock.patch.object(ris.RISOperations, 'set_vm_status')
    def test_set_vm_status_gen9(self, set_vm_status_mock):
        self.client.model = 'Gen9'
        self.client.set_vm_status(device='FLOPPY', boot_option='BOOT_ONCE',
                                  write_protect='YES')
        set_vm_status_mock.assert_called_once_with('FLOPPY', 'BOOT_ONCE',
                                                   'YES')

    @mock.patch.object(ribcl.RIBCLOperations, 'set_vm_status')
    def test_set_vm_status_gen8(self, set_vm_status_mock):
        self.client.model = 'Gen8'
        self.client.set_vm_status(device='FLOPPY', boot_option='BOOT_ONCE',
                                  write_protect='YES')
        set_vm_status_mock.assert_called_once_with('FLOPPY', 'BOOT_ONCE',
                                                   'YES')

    @mock.patch.object(ris.RISOperations, 'insert_virtual_media')
    def test_insert_virtual_media_gen9(self, insert_virtual_media_mock):
        self.client.model = 'Gen9'
        self.client.insert_virtual_media(url="http://ilo/fpy.iso",
                                         device='FLOPPY')
        insert_virtual_media_mock.assert_called_once_with("http://ilo/fpy.iso",
                                                          "FLOPPY")

    @mock.patch.object(ribcl.RIBCLOperations, 'insert_virtual_media')
    def test_insert_virtual_media_gen8(self, insert_virtual_media_mock):
        self.client.model = 'Gen8'
        self.client.insert_virtual_media(url="http://ilo/fpy.iso",
                                         device='FLOPPY')
        insert_virtual_media_mock.assert_called_once_with("http://ilo/fpy.iso",
                                                          "FLOPPY")

    @mock.patch.object(ris.RISOperations, 'get_one_time_boot')
    def test_get_one_time_boot_gen9(self, get_one_time_boot_mock):
        self.client.model = 'Gen9'
        self.client.get_one_time_boot()
        get_one_time_boot_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_one_time_boot')
    def test_get_one_time_boot_gen8(self, get_one_time_boot_mock):
        self.client.model = 'Gen8'
        self.client.get_one_time_boot()
        get_one_time_boot_mock.assert_called_once_with()

    @mock.patch.object(ris.RISOperations, 'set_one_time_boot')
    def test_set_one_time_boot_gen9(self, set_one_time_boot_mock):
        self.client.model = 'Gen9'
        self.client.set_one_time_boot('cdrom')
        set_one_time_boot_mock.assert_called_once_with('cdrom')

    @mock.patch.object(ribcl.RIBCLOperations, 'set_one_time_boot')
    def test_set_one_time_boot_gen8(self, set_one_time_boot_mock):
        self.client.model = 'Gen8'
        self.client.set_one_time_boot('cdrom')
        set_one_time_boot_mock.assert_called_once_with('cdrom')

    @mock.patch.object(ris.RISOperations, 'update_persistent_boot')
    def test_update_persistent_boot_gen9(self, update_persistent_boot_mock):
        self.client.model = 'Gen9'
        self.client.update_persistent_boot(['cdrom'])
        update_persistent_boot_mock.assert_called_once_with(['cdrom'])

    @mock.patch.object(ribcl.RIBCLOperations, 'update_persistent_boot')
    def test_update_persistent_boot_gen8(self, update_persistent_boot_mock):
        self.client.model = 'Gen8'
        self.client.update_persistent_boot(['cdrom'])
        update_persistent_boot_mock.assert_called_once_with(['cdrom'])

    @mock.patch.object(ris.RISOperations, 'get_persistent_boot_device')
    def test_get_persistent_boot_device_gen9(self, get_pers_boot_device_mock):
        self.client.model = 'Gen9'
        self.client.get_persistent_boot_device()
        get_pers_boot_device_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_persistent_boot_device')
    def test_get_persistent_boot_device_gen8(self, get_pers_boot_device_mock):
        self.client.model = 'Gen8'
        self.client.get_persistent_boot_device()
        get_pers_boot_device_mock.assert_called_once_with()

    @mock.patch.object(client.IloClient, '_call_method')
    def test_update_firmware(self, _call_method_mock):
        # | GIVEN |
        some_url = 'some-url'
        some_component_type = 'ilo'
        # | WHEN |
        self.client.update_firmware(some_url, some_component_type)
        # | THEN |
        _call_method_mock.assert_called_once_with('update_firmware',
                                                  some_url,
                                                  some_component_type)

    @mock.patch.object(ris.RISOperations, 'hold_pwr_btn')
    def test_hold_pwr_btn_gen9(self, hold_pwr_btn_mock):
        self.client.model = 'Gen9'
        self.client.hold_pwr_btn()
        self.assertTrue(hold_pwr_btn_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, 'hold_pwr_btn')
    def test_hold_pwr_btn_gen8(self, hold_pwr_btn_mock):
        self.client.model = 'Gen8'
        self.client.hold_pwr_btn()
        self.assertTrue(hold_pwr_btn_mock.called)

    @mock.patch.object(ris.RISOperations, 'set_host_power')
    def test_set_host_power_gen9(self, set_host_power_mock):
        self.client.model = 'Gen9'
        self.client.set_host_power('ON')
        set_host_power_mock.assert_called_once_with('ON')

    @mock.patch.object(ribcl.RIBCLOperations, 'set_host_power')
    def test_set_host_power_gen8(self, set_host_power_mock):
        self.client.model = 'Gen8'
        self.client.set_host_power('ON')
        set_host_power_mock.assert_called_once_with('ON')

    @mock.patch.object(ris.RISOperations, 'press_pwr_btn')
    def test_press_pwr_btn_gen9(self, press_pwr_btn_mock):
        self.client.model = 'Gen9'
        self.client.press_pwr_btn()
        self.assertTrue(press_pwr_btn_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, 'press_pwr_btn')
    def test_press_pwr_btn_gen8(self, press_pwr_btn_mock):
        self.client.model = 'Gen8'
        self.client.press_pwr_btn()
        self.assertTrue(press_pwr_btn_mock.called)

    @mock.patch.object(ris.RISOperations, 'reset_server')
    def test_reset_server_gen9(self, reset_server_mock):
        self.client.model = 'Gen9'
        self.client.reset_server()
        self.assertTrue(reset_server_mock.called)

    @mock.patch.object(ribcl.RIBCLOperations, 'reset_server')
    def test_reset_server_gen8(self, reset_server_mock):
        self.client.model = 'Gen8'
        self.client.reset_server()
        self.assertTrue(reset_server_mock.called)

    @mock.patch.object(ris.RISOperations, 'get_current_bios_settings')
    def test_get_current_bios_settings_gen9(self, cur_bios_settings_mock):
        self.client.model = 'Gen9'
        apply_filter = True
        self.client.get_current_bios_settings(apply_filter)
        cur_bios_settings_mock.assert_called_once_with(True)

    @mock.patch.object(ris.RISOperations, 'get_pending_bios_settings')
    def test_get_pending_bios_settings_gen9(self, pending_bios_settings_mock):
        self.client.model = 'Gen9'
        apply_filter = True
        self.client.get_pending_bios_settings(apply_filter)
        pending_bios_settings_mock.assert_called_once_with(True)

    @mock.patch.object(ris.RISOperations, 'get_default_bios_settings')
    def test_get_default_bios_settings_gen9(self, def_bios_settings_mock):
        self.client.model = 'Gen9'
        apply_filter = False
        self.client.get_default_bios_settings(apply_filter)
        def_bios_settings_mock.assert_called_once_with(False)

    @mock.patch.object(ris.RISOperations, 'set_bios_settings')
    def test_set_bios_settings_gen9(self, bios_settings_mock):
        self.client.model = 'Gen9'
        apply_filter = False
        d = {'a': 'blah', 'b': 'blah blah'}
        self.client.set_bios_settings(d, apply_filter)
        bios_settings_mock.assert_called_once_with(d, False)

    @mock.patch.object(client.IloClient, '_call_method')
    @mock.patch.object(snmp_cpqdisk_sizes, 'get_local_gb')
    def test_get_essential_prop_no_snmp_ris(self,
                                            snmp_mock,
                                            call_mock):
        self.client.model = 'Gen9'
        properties = {'local_gb': 250}
        data = {'properties': properties}
        call_mock.return_value = data
        self.client.get_essential_properties()
        call_mock.assert_called_once_with('get_essential_properties')
        self.assertFalse(snmp_mock.called)

    @mock.patch.object(client.IloClient, '_call_method')
    @mock.patch.object(snmp_cpqdisk_sizes, 'get_local_gb')
    def test_get_essential_prop_no_snmp_local_gb_0(self,
                                                   snmp_mock,
                                                   call_mock):
        self.client.model = 'Gen9'
        properties = {'local_gb': 0}
        data = {'properties': properties}
        call_mock.return_value = data
        self.client.get_essential_properties()
        call_mock.assert_called_once_with('get_essential_properties')
        self.assertFalse(snmp_mock.called)

    @mock.patch.object(client.IloClient, '_call_method')
    @mock.patch.object(snmp_cpqdisk_sizes, 'get_local_gb')
    def test_get_essential_prop_snmp_true(self,
                                          snmp_mock,
                                          call_mock):
        self.client.model = 'Gen9'
        snmp_credentials = {'auth_user': 'user',
                            'auth_prot_pp': '1234',
                            'auth_priv_pp': '4321',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': 'true'}
        self.client.snmp_credentials = snmp_credentials
        properties = {'local_gb': 0}
        data = {'properties': properties}
        call_mock.return_value = data
        snmp_mock.return_value = 250
        self.client.get_essential_properties()
        call_mock.assert_called_once_with('get_essential_properties')
        snmp_mock.assert_called_once_with(self.client.info['address'],
                                          snmp_credentials)

    @mock.patch.object(client.IloClient, '_call_method')
    @mock.patch.object(snmp_cpqdisk_sizes, 'get_local_gb')
    def test_get_essential_prop_snmp_true_local_gb_0(self,
                                                     snmp_mock,
                                                     call_mock):
        self.client.model = 'Gen9'
        snmp_credentials = {'auth_user': 'user',
                            'auth_prot_pp': '1234',
                            'auth_priv_pp': '4321',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': 'true'}
        self.client.snmp_credentials = snmp_credentials
        properties = {'local_gb': 0}
        data = {'properties': properties}
        call_mock.return_value = data
        snmp_mock.return_value = 0
        self.client.get_essential_properties()
        call_mock.assert_called_once_with('get_essential_properties')
        snmp_mock.assert_called_once_with(self.client.info['address'],
                                          snmp_credentials)

    @mock.patch.object(snmp_cpqdisk_sizes, 'get_local_gb')
    @mock.patch.object(client.IloClient, '_call_method')
    def test_get_essential_prop_snmp_false_local_gb_0(self, call_mock,
                                                      snmp_mock):

        self.client.model = 'Gen9'
        snmp_credentials = {'auth_user': 'user',
                            'auth_prot_pp': '1234',
                            'auth_priv_pp': '4321',
                            'auth_protocol': 'SHA',
                            'priv_protocol': 'AES',
                            'snmp_inspection': False}
        self.client.snmp_inspection = False
        self.client.snmp_credentials = snmp_credentials
        properties = {'local_gb': 0}
        data = {'properties': properties}
        call_mock.return_value = data
        self.client.get_essential_properties()
        call_mock.assert_called_once_with('get_essential_properties')
        self.assertFalse(snmp_mock.called)

    @mock.patch.object(client.IloClient, '_call_method')
    def test_inject_nmi(self, call_mock):
        self.client.inject_nmi()
        call_mock.assert_called_once_with('inject_nmi')

    @mock.patch.object(ris.RISOperations, 'inject_nmi')
    def test_inject_nmi_gen9(self, inject_nmi_mock):
        self.client.model = 'Gen9'
        self.client.inject_nmi()
        inject_nmi_mock.assert_called_once_with()

    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def test_inject_nmi_gen8(self, product_mock):
        self.client.model = 'Gen8'
        self.assertRaisesRegexp(exception.IloCommandNotSupportedError,
                                'not supported',
                                self.client.inject_nmi)


class IloRedfishClientTestCase(testtools.TestCase):

    @mock.patch.object(redfish, 'RedfishOperations',
                       spec_set=True, autospec=True)
    @mock.patch.object(ribcl.RIBCLOperations, 'get_product_name')
    def setUp(self, product_mock, redfish_mock):
        super(IloRedfishClientTestCase, self).setUp()
        self.redfish_mock = redfish_mock
        product_mock.return_value = 'Gen10'
        self.client = client.IloClient("1.2.3.4", "Admin", "admin")

    def test_calling_redfish_operations_gen10(self):
        self.client.model = 'Gen10'

        def validate_method_calls(methods, method_args, missed_ops):
            for redfish_method_name in methods:
                try:
                    if method_args:
                        eval('self.client.' + redfish_method_name)(
                            *method_args)
                    else:
                        eval('self.client.' + redfish_method_name)()
                    if redfish_method_name not in ('unset_iscsi_boot_info',
                                                   'set_iscsi_boot_info'):
                        self.assertTrue(eval(
                            'self.redfish_mock.return_value.' +
                            redfish_method_name).called)
                    validate_method_calls.no_test_cases += 1
                except TypeError:
                    missed_ops.append(redfish_method_name)

        validate_method_calls.no_test_cases = 0
        missed_operations = []
        validate_method_calls(
            client.SUPPORTED_REDFISH_METHODS, (), missed_operations)

        more_missed_operations = []
        validate_method_calls(
            missed_operations, ('arg',), more_missed_operations)

        even_more_missed_operations = []
        validate_method_calls(
            more_missed_operations, ('arg1', 'arg2'),
            even_more_missed_operations)
        if(len(even_more_missed_operations) == 1):
            self.assertEqual('set_iscsi_info',
                             even_more_missed_operations[0])
        else:
            self.assertEqual(2, len(even_more_missed_operations))
            self.assertEqual(len(client.SUPPORTED_REDFISH_METHODS) - 2,
                             validate_method_calls.no_test_cases)
