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

from proliantutils.redfish.resources.manager import virtual_media
from proliantutils.redfish import utils


class HPEManager(manager.Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """

    _virtual_media = None

    def set_license(self, key):
        """Set the license on a redfish system

        :param key: license key
        """
        data = {'LicenseKey': key}
        license_service_uri = (utils.get_subresource_path_by(self,
                               ['Oem', 'Hpe', 'Links', 'LicenseService']))
        self._conn.post(license_service_uri, data=data)

    @property
    def virtual_media(self):
        """Property to provide reference to `VirtualMediaCollection` instance.

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._virtual_media is None:
            self._virtual_media = virtual_media.VirtualMediaCollection(
                self._conn,
                utils.get_subresource_path_by(self, 'VirtualMedia'),
                redfish_version=self.redfish_version)

        return self._virtual_media
