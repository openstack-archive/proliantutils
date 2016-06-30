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
        """Return the clean steps supported by this hardware manager.

        This method returns the clean steps that are supported by
        proliant hardware manager.  This method is invoked on every
        hardware manager by Ironic Python Agent to give this information
        back to Ironic.

        :param node: A dictionary of the node object
        :param ports: A list of dictionaries containing information of ports
            for the node
        :returns: A list of dictionaries, each item containing the step name,
            interface and priority for the clean step.
        """
        steps = [{'step': 'create_configuration',
                  'interface': 'raid',
                  'priority': 0},
                 {'step': 'delete_configuration',
                  'interface': 'raid',
                  'priority': 0},
                 {'step': 'hardware_disk_erase',
                  'interface': 'deploy',
                  'priority': 0}]
        return steps

    def evaluate_hardware_support(cls):
        return hardware.HardwareSupport.SERVICE_PROVIDER

    def create_configuration(self, node, ports):
        """Create RAID configuration on the bare metal.

        This method creates the desired RAID configuration as read from
        node['target_raid_config'].

        :param node: A dictionary of the node object
        :param ports: A list of dictionaries containing information of ports
            for the node
        :returns: The current RAID configuration of the below format.
            raid_config = {
                'logical_disks': [{
                    'size_gb': 100,
                    'raid_level': 1,
                    'physical_disks': [
                        '5I:0:1',
                        '5I:0:2'],
                    'controller': 'Smart array controller'
                    },
                ]
            }
        """
        target_raid_config = node.get('target_raid_config', {}).copy()
        return hpssa_manager.create_configuration(
            raid_config=target_raid_config)

    def delete_configuration(self, node, ports):
        """Deletes RAID configuration on the bare metal.

        This method deletes all the RAID disks on the bare metal.
        :param node: A dictionary of the node object
        :param ports: A list of dictionaries containing information of ports
            for the node
        """
        return hpssa_manager.delete_configuration()

    def hardware_disk_erase(self, node, ports):
        """Erases the devices on the bare metal.

        This method erases all the disks on the bare metal.
        :param node: A dictionary of the node object
        :param ports: A list of dictionaries containing information of ports
            for the node
        """
        info = node.get('driver_internal_info', {})
        erase_pattern = info.get('hardware_erase_pattern', 'zero')
        return hpssa_manager.hardware_disk_erase(erase_pattern)
