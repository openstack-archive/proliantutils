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

from proliantutils.redfish.resources.system.bios import BiosResource
from proliantutils.redfish.resources.system.bios import BiosSettings
from sushy.resources.system import system

class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """
    bios_odataid = base.Field(['Bios', '@odata.id'])
    @property
    def bios_resource(self):
        odataid_val = HPESystem.bios_odataid._load(self.json, self)
        bios_resource = BiosResource(
            self._conn, odataid_val, redfish_version=self.redfish_version)
        return bios_resource

    @property
    def bios_settings(self):
        bios_odataid_val = HPESystem.bios_odataid._load(self.json, self)
        bios_resource = BiosResource(self._conn, bios_odataid_val,
                                     redfish_version=self.redfish_version)
        bios_settings_uri = bios_resource.bios_settings_odataid
        bios_settings = BiosSettings(self._conn, bios_settings_uri,
                                     redfish_version=self.redfish_version)
        return bios_settings 
