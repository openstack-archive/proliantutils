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

from ironic_python_agent import hardware
from oslo_concurrency import processutils

from proliantutils.hpssa import manager as hpssa_manager


class ProliantHardwareManager(hardware.GenericHardwareManager):

    HARDWARE_MANAGER_VERSION = "3"

    def get_clean_steps(self):
        pass

    def evaluate_hardware_support(cls):
        return hardware.HardwareSupport.SERVICE_PROVIDER

    def erase_block_device(self, block_device):
        npass = 3
        cmd = ('shred', '--force', '--zero', '--verbose',
               '--iterations', npass, block_device.name)
        processutils.execute(*cmd)

    def erase_devices(self):
        block_devices = self.list_block_devices()
        for block_device in block_devices:
            self.erase_block_device(block_device)

    def create_raid_configuration(self, raid_config):
        return hpssa_manager.create_configuration(raid_config=raid_config)

    def delete_raid_configuration(self):
        hpssa_manager.delete_configuration()
