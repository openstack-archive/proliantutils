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

LOG = logging.getLogger(__name__)

CLASSCODE_FOR_GPU_DEVICES = [3]
SUBCLASSCODE_FOR_GPU_DEVICES = [0, 1, 2, 128]


class PCIDevice(base.ResourceBase):

    identity = base.Field('Id', required=True)

    name = base.Field('Name')

    class_code = base.Field('ClassCode')

    sub_class_code = base.Field('SubclassCode')

    _nic_capacity = None

    def refresh(self):
        super(PCIDevice, self).refresh()
        self._nic_capacity = None

    @property
    def nic_capacity(self):
        if self._nic_capacity is None:
            for item in self.name.split():
                if 'Gb' in item:
                    capacity = item.strip('Gb')
                    self._nic_capacity = (
                        int(capacity) if capacity.isdigit() else 0)
                    break
            else:
                self._nic_capacity = 0
        return self._nic_capacity


class PCIDeviceCollection(base.ResourceCollectionBase):

    _gpu_devices = None
    _max_nic_capacity = None

    @property
    def _resource_type(self):
        return PCIDevice

    @property
    def gpu_devices(self):
        if self._gpu_devices is None:
            self._gpu_devices = []
            for member in self.get_members():
                if member.class_code in CLASSCODE_FOR_GPU_DEVICES:
                    if member.sub_class_code in SUBCLASSCODE_FOR_GPU_DEVICES:
                        self._gpu_devices.append(member)
        return self._gpu_devices

    def refresh(self):
        super(PCIDeviceCollection, self).refresh()
        self._gpu_devices = None
        self._max_nic_capacity = None

    @property
    def max_nic_capacity(self):
        """Gets the maximum NIC capacity"""
        if self._max_nic_capacity is None:
            self._max_nic_capacity = (
                str(max([m.nic_capacity for m in self.get_members()])) + 'Gb')
        return self._max_nic_capacity
