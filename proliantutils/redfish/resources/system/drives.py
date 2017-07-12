# Copyright 2017 Hewlett Packard Enterprise Development LP
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

# There is no explicit collection for Drives. That said, a URI link as
# "/redfish/v1/Systems/1/Storage/1/Drives" will be an invalid URI.

import logging

from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')


class Drives(base.ResourceBase):

    identity = base.Field('Id')
    """The Drive identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    block_size_bytes = base.Field('BlockSizeBytes')
    """The size of the smallest addressible unit of this drive in bytes"""

    capable_speed_Gbs = base.Field('CapableSpeedGbs')
    """The speed which this drive can communicate to a storage controller
    in ideal conditions in Gigabits per second"""

    capacity_bytes = base.Field('CapacityBytes')
    """The size in bytes of this Drive"""

    media_type = base.Field('MediaType')
    """The type of media contained in this drive"""

    protocol = base.Field('Protocol')
    """The protocol this drive is using to communicate to the storage
    controller."""

    rotation_speed_rpm = base.Field('RotationSpeedRPM')
    """The rotation speed of this Drive in Revolutions per Minute (RPM)."""

    volumes = base.Field('Volumes')
    """A reference to the Volumes associated with this drive."""

    status = HealthStatusField("Status")
