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

import sushy

from proliantutils.redfish import connector as prutils_connector
from proliantutils.redfish.resources.account_service import account_service
from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.system import system
from proliantutils.redfish.resources import update_service
from proliantutils.redfish import utils


class HPESushy(sushy.Sushy):
    """Class that extends base Sushy class

    This class extends the Sushy class to override certain methods
    required to customize the functionality of different resources.
    It bypasses the initialization of the Sushy class and initializes
    the ResourceBase class with customized HPE specific connector subtype.
    """

    def __init__(self, base_url, username=None, password=None,
                 root_prefix='/redfish/v1/', verify=True,
                 auth=None, connector=None):
        """Initializes HPE specific sushy object.

        :param base_url: The base URL to the Redfish controller. It
            should include scheme and authority portion of the URL. For
            example: https://mgmt.vendor.com
        :param username: User account with admin/server-profile access
            privilege
        :param password: User account password
        :param root_prefix: The default URL prefix. This part includes
            the root service and version. Defaults to /redfish/v1
        :param verify: Either a boolean value, a path to a CA_BUNDLE
            file or directory with certificates of trusted CAs. If set to
            True the driver will verify the host certificates; if False
            the driver will ignore verifying the SSL certificate; if it's
            a path the driver will use the specified certificate or one of
            the certificates in the directory. Defaults to True.
        :param auth: An authentication mechanism to utilize.
        :param connector: A user-defined connector object. Defaults to None.
        """
        super(HPESushy, self).__init__(
            base_url, username, password,
            root_prefix=root_prefix, verify=verify, auth=auth,
            connector=prutils_connector.HPEConnector(base_url, verify))

    def get_system_collection_path(self):
        return utils.get_subresource_path_by(self, 'Systems')

    def get_system(self, identity):
        """Given the identity return a HPESystem object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return system.HPESystem(self._conn, identity,
                                redfish_version=self.redfish_version)

    def get_manager_collection_path(self):
        return utils.get_subresource_path_by(self, 'Managers')

    def get_manager(self, identity):
        """Given the identity return a HPEManager object

        :param identity: The identity of the Manager resource
        :returns: The Manager object
        """
        return manager.HPEManager(self._conn, identity,
                                  redfish_version=self.redfish_version)

    def get_update_service(self):
        """Return a HPEUpdateService object

        :returns: The UpdateService object
        """
        update_service_url = utils.get_subresource_path_by(self,
                                                           'UpdateService')
        return (update_service.
                HPEUpdateService(self._conn, update_service_url,
                                 redfish_version=self.redfish_version))

    def get_account_service(self):
        """Return a HPEAccountService object"""
        account_service_url = utils.get_subresource_path_by(self,
                                                            'AccountService')

        return (account_service.
                HPEAccountService(self._conn, account_service_url,
                                  redfish_version=self.redfish_version))
