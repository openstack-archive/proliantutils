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


from proliantutils.redfish.resources.system import mappings as sys_map

from sushy.resources import base


class Drive(base.ResourceBase):
    """This class represents the Drive resource"""

    capacity_bytes = base.Field('CapacityBytes', adapter=int)
    """The size in bytes of this Drive"""

    media_type = base.MappedField('MediaType', sys_map.MEDIA_TYPE_MAP)
    """The type of media contained in this drive"""

    protocol = base.MappedField('Protocol', sys_map.DEVICE_PROTOCOLS_MAP)
    """The protocol this drive is using to communicate to the storage
    controller."""

    rotation_speed_rpm = base.Field('RotationSpeedRPM', adapter=int)
    """The rotation speed of this Drive in Revolutions per Minute (RPM)."""
