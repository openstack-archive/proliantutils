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
    bios_settings_odataid = base.Field(["@Redfish.Settings", "SettingsObject",
                                       "@odata.id"])
    base_uri = base.Field(['Oem', 'Hpe', 'Links',
                                  'BaseConfigs', '@odata.id'])

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a BootResource

        :param connector: A Connector instance
        :param identity: The identity of the BootResource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(BiosResource, self).__init__(connector, identity,
                                           redfish_version)

    def get_bios_config_uri(self):
        """Get the default bios config uri

        :returns: default bios config uri
        """
        bios_uri = BiosResource.base_uri._load(self.json, self)
        if not bios_uri:
            raise exception.MissingAttributeError(
                attribute='Oem/Hpe/Links/BaseConfigs',
                resource=self.path)
        return bios_uri

    def get_bios_default_data(self):
        """Get the default bios config data

        :returns: default bios config data
        """
        base_config_uri = self.get_bios_config_uri()
        response = self._conn.get(base_config_uri)
        if response.status_code != 200:
            msg = ("%s is not a valid response code received "
                   % response.status_code)
            raise exception.IloError(msg)
        return response

    def update_bios_default_data(self, bios_uri, data):
        """Update bios default settings

        :param bios_uri: bios settings uri
        :param data: default bios config data
        :returns response object of the post operation
        """
        if bios_uri is not None:
            return self._conn.patch(bios_uri, data=data)


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
