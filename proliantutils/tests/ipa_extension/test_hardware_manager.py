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
from oslo.concurrency import processutils
import testtools

from proliantutils.hpssa import manager as hpssa_manager
from proliantutils.ipa_extension import hardware_manager


class ProliantHardwareManagerTestCase(testtools.TestCase):

    def setUp(self):
        self.hardware_manager = hardware_manager.ProliantHardwareManager()
        super(ProliantHardwareManagerTestCase, self).setUp()

    @mock.patch.object(processutils, 'execute')
    def test_erase_block_device(self, processutils_mock):
        device = mock.MagicMock()
        p = mock.PropertyMock(return_value='/dev/sda')
        type(device).name = p
        cmd_expected = ('shred', '--force', '--zero', '--verbose',
                        '--iterations', 3, '/dev/sda')
        self.hardware_manager.erase_block_device(device)
        processutils_mock.assert_called_once_with(*cmd_expected)

    @mock.patch.object(hardware_manager.ProliantHardwareManager,
                       'erase_block_device')
    def test_erase_devices(self, erase_block_device_mock):
        disks = ['/dev/sda', '/dev/sdb']
        self.hardware_manager.list_block_devices.return_value = disks
        self.hardware_manager.erase_devices()
        self.hardware_manager.list_block_devices.assert_called_once_with()
        erase_block_device_mock.assert_any_call('/dev/sda')
        erase_block_device_mock.assert_any_call('/dev/sdb')

    @mock.patch.object(hpssa_manager, 'create_configuration')
    def test_create_raid_configuration(self, create_mock):
        create_mock.return_value = 'current-config'
        manager = self.hardware_manager
        ret = manager.create_raid_configuration(raid_config='target')
        create_mock.assert_called_once_with(raid_config='target')
        self.assertEqual('current-config', ret)

    @mock.patch.object(hpssa_manager, 'delete_configuration')
    def test_delete_raid_configuration(self, delete_mock):
        self.hardware_manager.delete_raid_configuration()
        delete_mock.assert_called_once_with()
