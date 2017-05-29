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

from proliantutils.redfish import utils
from sushy.resources import base
from sushy.resources.manager import manager


class HPEManager(manager.Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """

    def set_license(self, key):
        """Set the license on a redfish system

        :param key: license key
        :returns: response object of the post operation
        """
        lic_key = {'LicenseKey': key}
        target_uri = (utils.get_subresource_path_by(self,
                      ['Oem', 'Hpe', 'Links', 'LicenseService']))
        return self._conn.post(target_uri, data=lic_key)
