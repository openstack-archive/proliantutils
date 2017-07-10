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

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a PCIDevice

        :param connector: A Connector instance
        :param identity: The identity of the ethernet interface.
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PCIDevice, self).__init__(connector, identity,
                                        redfish_version)


class PCIDeviceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return PCIDevice

    _gpu_device_count = 0

    @property
    def gpu_devices(self):
        gpu_list = []
        for member in self.get_members():
            if member.class_code in CLASSCODE_FOR_GPU_DEVICES:
                if member.sub_class_code in SUBCLASSCODE_FOR_GPU_DEVICES:
                    gpu_list.append(member)
        self._gpu_devices_count = len(gpu_list)
        return self._gpu_devices_count

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a PciDeviceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the PCIDevice
            collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PCIDeviceCollection, self).__init__(connector, path,
                                                  redfish_version)
