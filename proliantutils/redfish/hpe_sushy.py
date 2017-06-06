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

from proliantutils.redfish.resources.system import hpe_system
from sushy.main import Sushy


class HPESushy(Sushy):
    def get_system(self, identity):
        """Given the identity return a HPESystem object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return hpe_system.HPESystem(self._conn, identity,
                                    redfish_version=self.redfish_version)
