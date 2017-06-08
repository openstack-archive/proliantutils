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

from proliantutils.redfish.resources.system import secure_boot
from sushy.resources import base
from sushy.resources.system import system


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """
    secure_boot_odataid = base.Field(['SecureBoot', '@odata.id'])

    @property
    def secure_boot_resource(self):
        odataid_val = HPESystem.secure_boot_odataid._load(self.json, self)
        secure_boot_resource = secure_boot.SecureBootResource(
            self._conn, odataid_val,
            redfish_version=self.redfish_version)
        return secure_boot_resource

    def secure_boot_config(self, data):
        if data is not None:
            target_uri = HPESystem.secure_boot_odataid._load(self.json, self)
            self._conn.patch(target_uri, data=data)
