# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
from oslo_utils import importutils
import testtools

from proliantutils import exception
from proliantutils.hpssa import manager as hpssa_manager
from proliantutils.ipa_hw_manager import hardware_manager

ironic_python_agent = importutils.try_import('ironic_python_agent')


class ProliantHardwareManagerTestCase(testtools.TestCase):

    def setUp(self):
        self.hardware_manager = hardware_manager.ProliantHardwareManager()
        super(ProliantHardwareManagerTestCase, self).setUp()

    def test_get_clean_steps(self):
        self.assertEqual(
            [{'step': 'create_configuration',
              'interface': 'raid',
              'priority': 0},
             {'step': 'delete_configuration',
              'interface': 'raid',
              'priority': 0},
             {'step': 'erase_devices',
              'interface': 'deploy',
              'priority': 0},
             {'step': 'update_firmware',
              'interface': 'management',
              'priority': 0}],
            self.hardware_manager.get_clean_steps("", ""))

    @mock.patch.object(hpssa_manager, 'create_configuration')
    def test_create_configuration(self, create_mock):
        create_mock.return_value = 'current-config'
        manager = self.hardware_manager
        node = {'target_raid_config': {'foo': 'bar'}}
        ret = manager.create_configuration(node, [])
        create_mock.assert_called_once_with(raid_config={'foo': 'bar'})
        self.assertEqual('current-config', ret)

    @mock.patch.object(hpssa_manager, 'delete_configuration')
    def test_delete_configuration(self, delete_mock):
        delete_mock.return_value = 'current-config'
        ret = self.hardware_manager.delete_configuration("", "")
        delete_mock.assert_called_once_with()
        self.assertEqual('current-config', ret)

    @mock.patch.object(ironic_python_agent.hardware.GenericHardwareManager,
                       'erase_devices')
    @mock.patch.object(hpssa_manager, 'erase_devices')
    def test_erase_devices(self, erase_mock, generic_erase_mock):
        node = {}
        port = {}
        erase_mock.return_value = 'erase_status'
        generic_erase_mock.return_value = {'foo': 'bar'}
        ret = self.hardware_manager.erase_devices(node, port)
        erase_mock.assert_called_once_with()
        generic_erase_mock.assert_called_once_with(node, port)
        self.assertEqual({'Disk Erase Status': 'erase_status', 'foo': 'bar'},
                         ret)

    @mock.patch.object(ironic_python_agent.hardware.GenericHardwareManager,
                       'erase_devices')
    @mock.patch.object(hpssa_manager, 'erase_devices')
    def test_erase_devices_not_supported(self, erase_mock, generic_erase_mock):
        node = {}
        port = {}
        value = ("Sanitize erase not supported in the "
                 "available controllers")
        e = exception.HPSSAOperationError(reason=value)
        erase_mock.side_effect = e

        exc = self.assertRaises(exception.HPSSAOperationError,
                                self.hardware_manager.erase_devices,
                                node, port)

        self.assertIn(value, str(exc))
