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

<<<<<<< HEAD
import sushy

from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.system import system
from proliantutils.redfish import utils
=======
from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.account_service import account_service
from proliantutils.redfish.resources.system import system
import sushy

LOG = log.get_logger(__name__)
>>>>>>> 3b18f82... Adds 'reset_ilo_credentials' for redfish systems


class HPESushy(sushy.Sushy):
    """Class that extends base Sushy class

    This class extends the Sushy class to override certain methods
    required to customize the functionality of different resources
    """

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

    def get_account_service(self, identity):
        """Given the identity return a HPEAccountService object

        :param identity: The identity of the AccountService resource
        :returns: The AccountService object
        """
        return account_service.\
            HPEAccountService(self._conn, identity,
                              redfish_version=self.redfish_version)

    def _get_account_service_collection_path(self):
        """Helper function to find the AccountService path"""
        account_service = self.json.get('AccountService')
        if not account_service:
            raise exception.MissingAttributeError(attribute='AccountService',
                                                  resource=self._root_prefix)
        return account_service.get('@odata.id')

    def _get_account_service(self):
        """Get the AccountService

        """
        account_service_url = self._get_account_service_collection_path()
        try:
            return self.get_account_service(account_service_url)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish System "%(account_service)s" '
                          'was not found. Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
