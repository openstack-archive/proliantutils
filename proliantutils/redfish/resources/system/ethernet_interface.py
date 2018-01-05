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

from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import mappings as sys_map
from sushy.resources import base


class HealthStatusField(base.CompositeField):
    state = base.MappedField(
        'State', sys_map.HEALTH_STATE_VALUE_MAP)
    health = base.MappedField('Health', sys_map.HEALTH_VALUE_MAP)


class EthernetInterface(base.ResourceBase):
    """This class represents the EthernetInterfaces resource"""

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

    speed_mbps = base.Field('SpeedMbps')
    """This is the current speed in Mbps of this interface."""

    status = HealthStatusField("Status")


class EthernetInterfaceCollection(base.ResourceCollectionBase):

    _summary = None

    @property
    def _resource_type(self):
        return EthernetInterface

    @property
    def summary(self):
        """property to return the summary MAC addresses and state

        This filters the MACs whose health is OK,
        and in 'Enabled' State would be returned.
        The returned format will be {<port_id>: <mac_address>}.
        This is because RIBCL returns the data in format
        {'Port 1': 'aa:bb:cc:dd:ee:ff'} and ironic ilo drivers inspection
        consumes the data in this format.
        Note: 'Id' is referred to as "Port number".
        """
        if self._summary is None:
            mac_dict = {}
            for eth in self.get_members():
                if eth.mac_address is not None:
                    if (eth.status is not None and
                            eth.status.health == sys_cons.HEALTH_OK
                            and eth.status.state ==
                            sys_cons.HEALTH_STATE_ENABLED):
                        mac_dict.update(
                            {'Port ' + eth.identity: eth.mac_address})
            self._summary = mac_dict
        return self._summary

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        self._summary = None
