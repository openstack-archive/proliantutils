# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__author__ = 'HPE'

from sushy.resources.manager import manager

from proliantutils import exception
from proliantutils.redfish.resources.manager import virtual_media


class HPEManager(manager.Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """

    _vmedia_resources = None

    def _get_vmedia_collection_path(self):
        """Helper function to find the VirtualMediaCollection path"""
        vmedia_col = self.json.get('VirtualMedia')
        if not vmedia_col:
            raise exception.MissingAttributeError(attribute='VirtualMedia',
                                                  resource=self._path)
        return vmedia_col.get('@odata.id')

    @property
    def vmedia_resources(self):
        """Property to provide reference to `VirtualMediaCollection` instance.

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._vmedia_resources is None:
            self._vmedia_resources = virtual_media.VirtualMediaCollection(
                self._conn,
                self._get_vmedia_collection_path(),
                redfish_version=self.redfish_version)

        return self._vmedia_resources
