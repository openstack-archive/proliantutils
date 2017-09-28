# Copyright 2018 Hewlett Packard Enterprise Development LP
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

import json

import mock
import sushy
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import ethernet_interface
from proliantutils.redfish.resources.system import memory
from proliantutils.redfish.resources.system import secure_boot
from proliantutils.redfish.resources.system import smart_storage_config
from proliantutils.redfish.resources.system.storage import simple_storage
from proliantutils.redfish.resources.system.storage import smart_storage
from proliantutils.redfish.resources.system.storage import storage
from proliantutils.redfish.resources.system import system
from proliantutils.redfish import utils
from sushy.resources.system import system as sushy_system


class HPESystemTestCase(testtools.TestCase):

    def setUp(self):
        super(HPESystemTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = system_json['default']

        self.sys_inst = system.HPESystem(
            self.conn, '/redfish/v1/Systems/1',
            redfish_version='1.0.2')

    def test_attributes(self):
        self.assertEqual(sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI,
                         self.sys_inst.supported_boot_mode)

    def test__get_hpe_push_power_button_action_element(self):
        value = self.sys_inst._get_hpe_push_power_button_action_element()
        self.assertEqual("/redfish/v1/Systems/1/Actions/Oem/Hpe/"
                         "HpeComputerSystemExt.PowerButton/",
                         value.target_uri)
        self.assertEqual(["Press", "PressAndHold"], value.allowed_values)

    def test__get_hpe_push_power_button_action_element_missing_action(self):
        self.sys_inst._hpe_actions.computer_system_ext_powerbutton = None
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'Oem/Hpe/Actions/#HpeComputerSystemExt.PowerButton is missing',
            self.sys_inst._get_hpe_push_power_button_action_element)

    def test_push_power_button(self):
        self.sys_inst.push_power_button(
            sys_cons.PUSH_POWER_BUTTON_PRESS)
        self.sys_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Systems/1/Actions/Oem/Hpe/'
            'HpeComputerSystemExt.PowerButton/',
            data={'PushType': 'Press'})

    def test_push_power_button_invalid_value(self):
        self.assertRaises(exception.InvalidInputError,
                          self.sys_inst.push_power_button, 'invalid-value')

    def test_bios_settings(self):
        self.assertIsNone(self.sys_inst._bios_settings)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/bios.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_bios = self.sys_inst.bios_settings
        self.assertIsInstance(actual_bios,
                              bios.BIOSSettings)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_bios,
                      self.sys_inst.bios_settings)
        self.conn.get.return_value.json.assert_not_called()

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_persistent(self,
                                               set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['CDROM'], persistent=True)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_CD,
            enabled=sushy.BOOT_SOURCE_ENABLED_CONTINUOUS)

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_device_unknown_persistent(
            self, set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['unknown'], persistent=True)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_NONE,
            enabled=sushy.BOOT_SOURCE_ENABLED_CONTINUOUS)

    @mock.patch.object(sushy_system.System, 'set_system_boot_source')
    def test_update_persistent_boot_not_persistent(
            self, set_system_boot_source_mock):
        self.sys_inst.update_persistent_boot(['CDROM'], persistent=False)
        set_system_boot_source_mock.assert_called_once_with(
            sushy.BOOT_SOURCE_TARGET_CD,
            enabled=sushy.BOOT_SOURCE_ENABLED_ONCE)

    def test_bios_settings_on_refresh(self):
        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/bios.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.bios_settings,
                              bios.BIOSSettings)

        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.sys_inst.invalidate()
        self.sys_inst.refresh(force=False)

        # | WHEN & THEN |
        self.assertIsNotNone(self.sys_inst._bios_settings)
        self.assertTrue(self.sys_inst._bios_settings._is_stale)

        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/bios.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.bios_settings,
                              bios.BIOSSettings)
        self.assertFalse(self.sys_inst._bios_settings._is_stale)

    def test_update_persistent_boot_uefi_target(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = (json.loads(f.read())[
                'System_op_for_update_persistent_boot_uefi_target'])
        self.sys_inst.uefi_target_override_devices = (system_json[
            'Boot']['UefiTargetBootSourceOverride@Redfish.AllowableValues'])
        self.sys_inst.update_persistent_boot(['ISCSI'], persistent=True)
        uefi_boot_settings = {
            'Boot': {'UefiTargetBootSourceOverride': 'PciRoot(0x0)/Pci(0x1C,0x0)/Pci(0x0,0x0)/MAC(98F2B3EEF886,0x0)/IPv4(172.17.1.32)/iSCSI(iqn.2001-04.com.paresh.boot:volume.bin,0x1,0x0,None,None,None,TCP)'}  # noqa
        }

        calls = [mock.call('/redfish/v1/Systems/1', data=uefi_boot_settings),
                 mock.call('/redfish/v1/Systems/1',
                           data={'Boot':
                                 {'BootSourceOverrideTarget': 'UefiTarget',
                                  'BootSourceOverrideEnabled': 'Continuous'}})]
        self.sys_inst._conn.patch.assert_has_calls(calls)

    def test_update_persistent_boot_uefi_no_iscsi_device(self):
        self.assertRaisesRegex(
            exception.IloError,
            'No UEFI iSCSI bootable device found on system.',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True)

    def test_update_persistent_boot_uefi_target_fail(self):
        update_mock = mock.PropertyMock(
            side_effect=sushy.exceptions.SushyError)
        type(self.sys_inst).uefi_target_override_devices = update_mock
        self.assertRaisesRegex(
            exception.IloError,
            'Unable to get uefi target override devices.',
            self.sys_inst.update_persistent_boot, ['ISCSI'], True)
        del type(self.sys_inst).uefi_target_override_devices

    def test_pci_devices(self):
        pci_dev_return_value = None
        pci_dev1_return_value = None
        pci_coll_return_value = None
        self.assertIsNone(self.sys_inst._pci_devices)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device_collection.json') as f:
            pci_coll_return_value = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device.json') as f:
            pci_dev_return_value = json.loads(f.read())
        with open('proliantutils/tests/redfish/'
                  'json_samples/pci_device1.json') as f:
            pci_dev1_return_value = json.loads(f.read())
            self.conn.get.return_value.json.side_effect = (
                [pci_coll_return_value, pci_dev_return_value,
                 pci_dev1_return_value])
        actual_pci = self.sys_inst.pci_devices
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_pci,
                      self.sys_inst.pci_devices)
        self.conn.get.return_value.json.assert_not_called()

    def test_secure_boot_with_missing_path_attr(self):
        def _get_secure_boot():
            return self.sys_inst.secure_boot

        self.sys_inst._json.pop('SecureBoot')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'attribute SecureBoot is missing',
            _get_secure_boot)

    def test_secure_boot(self):
        # check for the underneath variable value
        self.assertIsNone(self.sys_inst._secure_boot)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN |
        actual_secure_boot = self.sys_inst.secure_boot
        # | THEN |
        self.assertIsInstance(actual_secure_boot,
                              secure_boot.SecureBoot)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_secure_boot,
                      self.sys_inst.secure_boot)
        self.conn.get.return_value.json.assert_not_called()

    def test_secure_boot_on_refresh(self):
        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.secure_boot,
                              secure_boot.SecureBoot)

        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.sys_inst.invalidate()
        self.sys_inst.refresh(force=False)

        # | WHEN & THEN |
        self.assertIsNotNone(self.sys_inst._secure_boot)
        self.assertTrue(self.sys_inst._secure_boot._is_stale)

        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/secure_boot.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.secure_boot,
                              secure_boot.SecureBoot)
        self.assertFalse(self.sys_inst._secure_boot._is_stale)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path(self, res_mock):
        res = 'EthernetInterfaces'
        res_mock.return_value = '/redfish/v1/Systems/1/EthernetInterfaces'
        path = self.sys_inst._get_hpe_sub_resource_collection_path(res)
        self.assertTrue(res_mock.called)
        self.assertEqual(path, res_mock.return_value)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path_oem_path(self, res_mock):
        res = 'EthernetInterfaces'
        error_val = exception.MissingAttributeError
        oem_path = '/redfish/v1/Systems/1/EthernetInterfaces'
        res_mock.side_effect = [error_val, oem_path]
        path = self.sys_inst._get_hpe_sub_resource_collection_path(res)
        self.assertTrue(res_mock.called)
        self.assertEqual(path, oem_path)

    @mock.patch.object(utils, 'get_subresource_path_by')
    def test_get_hpe_sub_resource_collection_path_fail(self, res_mock):
        error_val = exception.MissingAttributeError
        res_mock.side_effect = [error_val, error_val]
        self.assertRaises(
            exception.MissingAttributeError,
            self.sys_inst._get_hpe_sub_resource_collection_path,
            'EthernetInterfaces')
        self.assertTrue(res_mock.called)

    def test_ethernet_interfaces(self):
        self.conn.get.return_value.json.reset_mock()
        eth_coll = None
        eth_value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'ethernet_interface_collection.json')
        with open(path, 'r') as f:
            eth_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'ethernet_interface.json', 'r') as f:
            eth_value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [eth_coll,
                                                       eth_value]
        self.assertIsNone(self.sys_inst._ethernet_interfaces)
        actual_macs = self.sys_inst.ethernet_interfaces.summary
        self.assertEqual({'Port 1': '12:44:6A:3B:04:11'},
                         actual_macs)
        self.assertIsInstance(self.sys_inst._ethernet_interfaces,
                              ethernet_interface.EthernetInterfaceCollection)

    def test_ethernet_interfaces_oem(self):
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = (
            system_json['System_for_oem_ethernet_interfaces'])

        self.sys_inst = system.HPESystem(
            self.conn, '/redfish/v1/Systems/1',
            redfish_version='1.0.2')

        self.conn.get.return_value.json.reset_mock()
        eth_coll = None
        eth_value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'ethernet_interface_collection.json')
        with open(path, 'r') as f:
            eth_coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'ethernet_interface.json', 'r') as f:
            eth_value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [eth_coll,
                                                       eth_value]
        self.assertIsNone(self.sys_inst._ethernet_interfaces)
        actual_macs = self.sys_inst.ethernet_interfaces.summary
        self.assertEqual({'Port 1': '12:44:6A:3B:04:11'},
                         actual_macs)
        self.assertIsInstance(self.sys_inst._ethernet_interfaces,
                              ethernet_interface.EthernetInterfaceCollection)

    def test_smart_storage(self):
        self.conn.get.return_value.json.reset_mock()
        value = None
        with open('proliantutils/tests/redfish/json_samples/'
                  'smart_storage.json', 'r') as f:
            value = (json.loads(f.read()))
        self.conn.get.return_value.json.return_value = value
        self.assertIsNone(self.sys_inst._smart_storage)
        value = self.sys_inst.smart_storage
        self.assertIsInstance(value, smart_storage.HPESmartStorage)

    def test_storages(self):
        self.conn.get.return_value.json.reset_mock()
        coll = None
        value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'storage_collection.json')
        with open(path, 'r') as f:
            coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'storage.json', 'r') as f:
            value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [coll, value]
        self.assertIsNone(self.sys_inst._storages)
        value = self.sys_inst.storages
        self.assertIsInstance(value, storage.StorageCollection)

    def test_simple_storages(self):
        self.conn.get.return_value.json.reset_mock()
        coll = None
        value = None
        path = ('proliantutils/tests/redfish/json_samples/'
                'simple_storage_collection.json')
        with open(path, 'r') as f:
            coll = json.loads(f.read())
        with open('proliantutils/tests/redfish/json_samples/'
                  'simple_storage.json', 'r') as f:
            value = (json.loads(f.read()))
        self.conn.get.return_value.json.side_effect = [coll, value]
        self.assertIsNone(self.sys_inst._simple_storages)
        value = self.sys_inst.simple_storages
        self.assertIsInstance(value, simple_storage.SimpleStorageCollection)

    def test_simple_storage_on_refresh(self):
        with open('proliantutils/tests/redfish/json_samples/'
                  'simple_storage_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.assertIsInstance(self.sys_inst.simple_storages,
                              simple_storage.SimpleStorageCollection)
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.sys_inst.invalidate()
        self.sys_inst.refresh(force=False)

        self.assertIsNotNone(self.sys_inst._simple_storages)
        self.assertTrue(self.sys_inst._simple_storages._is_stale)

        with open('proliantutils/tests/redfish/json_samples/'
                  'simple_storage_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.assertIsInstance(self.sys_inst.simple_storages,
                              simple_storage.SimpleStorageCollection)
        self.assertFalse(self.sys_inst._simple_storages._is_stale)

    def test_memory(self):
        self.assertIsNone(self.sys_inst._memory)
        self.conn.get.return_value.json.reset_mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        actual_memory = self.sys_inst.memory
        self.assertIsInstance(actual_memory,
                              memory.MemoryCollection)
        self.conn.get.return_value.json.assert_called_once_with()
        # reset mock
        self.conn.get.return_value.json.reset_mock()
        self.assertIs(actual_memory,
                      self.sys_inst.memory)
        self.conn.get.return_value.json.assert_not_called()

    def test_memory_collection_on_refresh(self):
        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.memory,
                              memory.MemoryCollection)

        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.sys_inst.invalidate()
        self.sys_inst.refresh(force=False)

        # | WHEN & THEN |
        self.assertIsNotNone(self.sys_inst._memory)
        self.assertTrue(self.sys_inst._memory._is_stale)

        # | GIVEN |
        with open('proliantutils/tests/redfish/json_samples/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.sys_inst.memory,
                              memory.MemoryCollection)
        self.assertFalse(self.sys_inst._memory._is_stale)

    def test_storage_on_refresh(self):
        with open('proliantutils/tests/redfish/json_samples/'
                  'storage_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.assertIsInstance(self.sys_inst.storages,
                              storage.StorageCollection)
        # On refreshing the system instance...
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read())['default'])

        self.sys_inst.invalidate()
        self.sys_inst.refresh(force=False)

        self.assertIsNotNone(self.sys_inst._storages)
        self.assertTrue(self.sys_inst._storages._is_stale)

        with open('proliantutils/tests/redfish/json_samples/'
                  'simple_storage_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.assertIsInstance(self.sys_inst.storages,
                              storage.StorageCollection)
        self.assertFalse(self.sys_inst._storages._is_stale)

    def test_get_host_post_state(self):
        expected = sys_cons.POST_STATE_FINISHEDPOST
        self.assertEqual(expected, self.sys_inst.post_state)

    @mock.patch.object(smart_storage_config, 'HPESmartStorageConfig',
                       autospec=True)
    def test_get_smart_storage_config(self, mock_ssc):
        ssc_element = '/redfish/v1/systems/1/smartstorageconfig/'
        ssc_inst = self.sys_inst.get_smart_storage_config(ssc_element)
        self.assertIsInstance(ssc_inst,
                              smart_storage_config.HPESmartStorageConfig.
                              __class__)
        mock_ssc.assert_called_once_with(
            self.conn, "/redfish/v1/systems/1/smartstorageconfig/",
            redfish_version='1.0.2')

    @mock.patch.object(system.HPESystem, 'get_smart_storage_config')
    def test_delete_raid(self, get_smart_storage_config_mock):
        config_id = ['/redfish/v1/systems/1/smartstorageconfig/']
        type(self.sys_inst).smart_storage_config_identities = (
            mock.PropertyMock(return_value=config_id))
        (get_smart_storage_config_mock.return_value.
         delete_raid.return_value) = 'Status: Success'
        result = self.sys_inst.delete_raid()
        get_smart_storage_config_mock.assert_called_once_with(config_id[0])
        self.assertEqual([('/redfish/v1/systems/1/smartstorageconfig/',
                           'Status: Success')], result)

    @mock.patch.object(system.HPESystem, 'get_smart_storage_config')
    def test_delete_raid_controller_failed(self,
                                           get_smart_storage_config_mock):
        config_id = ['/redfish/v1/systems/1/smartstorageconfig/',
                     '/redfish/v1/systems/1/smartstorageconfig1/',
                     '/redfish/v1/systems/1/smartstorageconfig2/']
        type(self.sys_inst).smart_storage_config_identities = (
            mock.PropertyMock(return_value=config_id))
        get_smart_storage_config_mock.return_value.delete_raid.side_effect = (
            [None, sushy.exceptions.SushyError, None])
        self.assertRaisesRegex(
            exception.IloError,
            "The Redfish controller failed to delete the "
            "raid configuration in one or more controllers with",
            self.sys_inst.delete_raid)

    def test_check_smart_storage_config_ids(self):
        type(self.sys_inst).smart_storage_config_identities = (
            mock.PropertyMock(return_value=None))
        self.assertRaisesRegex(
            exception.IloError,
            "The Redfish controller failed to get the SmartStorageConfig "
            "controller configurations",
            self.sys_inst.check_smart_storage_config_ids)
