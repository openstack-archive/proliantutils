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

from sushy.resources import base


class BiosResource(base.ResourceBase):

    BootMode = base.Field(["Attributes", "BootMode"])
    BiosSettingsURI = base.Field(["@Redfish.Settings", "SettingsObject",
                                 "@odata.id"])

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a BootResource

        :param connector: A Connector instance
        :param identity: The identity of the BootResource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(BiosResource, self).__init__(connector, identity,
                                           redfish_version)


class BiosSettings(base.ResourceBase):

    BootMode = base.Field(["Attributes", "BootMode"])
    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a BootResource

        :param connector: A Connector instance
        :param identity: The identity of the BootResource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(BiosSettings, self).__init__(connector, identity,
                                           redfish_version)
