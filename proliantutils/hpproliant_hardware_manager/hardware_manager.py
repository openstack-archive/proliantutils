import os
import re

from ironic_python_agent import errors
from ironic_python_agent import hardware
from ironic_python_agent.openstack.common import log
from ironic_python_agent import utils

LOG = log.getLogger()

class HPProliantHardwareManager(hardware.GenericHardwareManager):
    HARDWARE_MANAGER_VERSION = "3"

    def get_clean_steps(self):
        pass

    def evaluate_hardware_support(cls):
        return hardware.HardwareSupport.SERVICE_PROVIDER
    
    def erase_block_device(self, block_device):
        npass = 3
        cmd = ['shred', '--force', '--zero', '--verbose',
               '--iterations', npass, block_device.name]

        utils.execute(*cmd, check_exit_code=[0])

    def erase_devices(self):
        block_devices = self.list_block_devices()
        for block_device in block_devices:
            self.erase_block_device(block_device)
