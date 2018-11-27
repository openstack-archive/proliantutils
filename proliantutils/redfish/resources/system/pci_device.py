# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from sushy.resources import base
from sushy import utils as sushy_utils

LOG = logging.getLogger(__name__)

CLASSCODE_FOR_GPU_DEVICES = [3]
SUBCLASSCODE_FOR_GPU_DEVICES = [0, 1, 2, 128]


class PCIDevice(base.ResourceBase):

    identity = base.Field('Id', required=True)

    name = base.Field('Name')

    class_code = base.Field('ClassCode')

    sub_class_code = base.Field('SubclassCode')

    @property
    @sushy_utils.cache_it
    def nic_capacity(self):
        for item in self.name.split():
            if 'Gb' in item:
                capacity = item.strip('Gb')
                return int(capacity) if capacity.isdigit() else 0
        return 0


class PCIDeviceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return PCIDevice

    @property
    @sushy_utils.cache_it
    def gpu_devices(self):
        gpu_devices = []
        for member in self.get_members():
            if member.class_code in CLASSCODE_FOR_GPU_DEVICES:
                if member.sub_class_code in SUBCLASSCODE_FOR_GPU_DEVICES:
                    gpu_devices.append(member)
        return gpu_devices

    @property
    @sushy_utils.cache_it
    def max_nic_capacity(self):
        """Gets the maximum NIC capacity"""
        return str(max([m.nic_capacity for m in self.get_members()])) + 'Gb'
