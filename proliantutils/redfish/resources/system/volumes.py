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

import logging

from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')


class Volumes(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The processor identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    encrypted = base.Field('Encrypted')
    """Is this Volume encrypted"""

    capacity_bytes = base.Field('CapacityBytes')
    """The size in bytes of this Volume"""

    volume_type = base.Field('VolumeType')
    """The type of this volume."""

    drives_list = base.Field('Drives')
    """An array of references to the drives which contain this volume.

    This will reference Drives that either wholly or only partly contain
    this volume."""

    status = HealthStatusField("Status")


class VolumesCollection(base.ResourceCollectionBase):

    _maximum_size = None

    @property
    def _resource_type(self):
        return Volumes

    @property
    def maximum_size(self):
        """Gets the biggest volume

        :returns size in bytes.
        """
        if self._maximum_size is None:
            self._maximum_size = 0
            for mem in self.get_members():
                if self._maximum_size < mem.capacity_bytes:
                    self._maximum_size = mem.capacity_bytes
        return self._maximum_size

    def refresh(self):
        super(VolumesCollection, self).refresh()
        self._maximum_size = None
