# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from proliantutils.redfish.resources.system import mappings as sys_map
from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    state = base.MappedField(
        'State', sys_map.HEALTH_STATE_VALUE_MAP)
    health = base.Field('Health')


class EthernetInterface(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The Ethernet Interface identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    permanent_mac_address = base.Field('PermanentMACAddress')
    """This is the permanent MAC address assigned to this interface (port) """

    mac_address = base.Field('MACAddress')
    """This is the currently configured MAC address of the interface."""

    speedmbps = base.Field('SpeedMbps')
    """This is the current speed in Mbps of this interface."""

    status = HealthStatusField("Status")

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a EthernetInterface

        :param connector: A Connector instance
        :param identity: The identity of the ethernet interface.
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(EthernetInterface, self).__init__(connector, identity,
                                                redfish_version)


class EthernetInterfaceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return EthernetInterface

    _eth_summary = None

    @property
    def eth_summary(self):
        """property to return the MAC addresses.

        This filters the MACs whose health is OK,
        which means the MACs in both 'Enabled' and 'Disabled' States
        are returned.
        """
        mac_dict = {}
        for eth in self.get_members():
            if eth.mac_address is not None:
                if eth.status is not None and eth.status.health == 'OK':
                    mac_dict.update({eth.mac_address: eth.status.state})
        self._eth_summary = mac_dict
        return self._eth_summary

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a EthernetInterfaceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the EthernetInterface
            collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(EthernetInterfaceCollection, self).__init__(connector, path,
                                                          redfish_version)
