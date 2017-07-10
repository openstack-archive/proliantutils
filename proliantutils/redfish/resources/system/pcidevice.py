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


class PciDevice(base.ResourceBase):

    identity = base.Field('Id', required=True)

    name = base.Field('Name')

    class_code = base.Field('ClassCode')

    device_id = base.Field('DeviceID')

    device_instance = base.Field('DeviceInstance')

    device_location = base.Field('DeviceLocation')

    device_number = base.Field('DeviceNumber')

    device_sub_instance = base.Field('DeviceSubInstance')

    device_type = base.Field('DeviceType')

    function_number = base.Field('FunctionNumber')

    location_string = base.Field('LocationString')

    segment_number = base.Field('SegmentNumber')

    structured_name = base.Field('StructuredName')

    sub_class_code = base.Field('SubclassCode')

    sub_system_device_id = base.Field('SubsystemDeviceID')

    sub_system_vendor_id = base.Field('SubsystemVendorID')

    uefi_device_path = base.Field('UEFIDevicePath')

    vendor_id = base.Field('VendorID')

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a PCIDevice

        :param connector: A Connector instance
        :param identity: The identity of the ethernet interface.
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PciDevice, self).__init__(connector, identity,
                                        redfish_version)


class PciDeviceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return PciDevice

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a PciDeviceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the PCIDevice
            collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PciDeviceCollection, self).__init__(connector, path,
                                                  redfish_version)
