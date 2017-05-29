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

from proliantutils import exception
from sushy.resources import base
from sushy.resources.manager.manager import Manager


class HPEManager(Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """
    lic_uri = base.Field(['Oem', 'Hpe', 'Links',
                          'LicenseService', '@odata.id'])

    def get_license_uri(self):
        """Get the license uri to activate_license

        :returns: license uri
        """
        license_uri = HPEManager.lic_uri._load(self.json, self)
        if not license_uri:
            raise exception.MissingAttributeError(
                attribute='Oem/Hpe/Links/LicenseService',
                resource=self.path)
        return license_uri

    def set_license(self, data):
        """Set the license on a redfish system

        :param data: license key in dictionary format.
        :returns: response object of the post operation
        """
        if data is not None:
            target_uri = self.get_license_uri()
            return self._conn.post(target_uri, data=data)
