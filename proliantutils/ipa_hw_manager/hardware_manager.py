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

from proliantutils.hpssa import manager as hpssa_manager


class ProliantHardwareManager(hardware.GenericHardwareManager):

    HARDWARE_MANAGER_VERSION = "3"

    def get_clean_steps(self, node, ports):
        return [{'step': 'create_configuration',
                 'interface': 'raid',
                 'priority': 0},
                {'step': 'delete_configuration',
                 'interface': 'raid',
                 'priority': 0}]

    def evaluate_hardware_support(cls):
        return hardware.HardwareSupport.SERVICE_PROVIDER

    def create_configuration(self, node, ports):
        target_raid_config = node.get('target_raid_config', {}).copy()
        return hpssa_manager.create_configuration(
            raid_config=target_raid_config)

    def delete_configuration(self, node, ports):
        return hpssa_manager.delete_configuration()
