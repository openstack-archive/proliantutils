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
from proliantutils import log
from proliantutils.redfish.resources.system import system
from proliantutils.redfish.resources import update_service
import sushy

LOG = log.get_logger(__name__)


class HPESushy(sushy.Sushy):
    """Class that extends base Sushy class

    This class extends the Sushy class to override certain methods
    required to customize the functionality of different resources
    """

    def get_system(self, identity):
        """Given the identity return a HPESystem object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return system.HPESystem(self._conn, identity,
                                redfish_version=self.redfish_version)

    def get_update_service(self, identity):
        """Given the identity return a HPEUpdateService object

        :param identity: The identity of the UpdateService resource
        :returns: The UpdateService object
        """
        return update_service.\
            HPEUpdateService(self._conn, identity,
                             redfish_version=self.redfish_version)

    def _get_update_service_path(self):
        """Helper function to find the UpdateService path"""
        update_service = self.json.get('UpdateService')
        if not update_service:
            raise exception.MissingAttributeError(attribute='UpdateService',
                                                  resource=self._root_prefix)
        return update_service.get('@odata.id')

    def _get_update_service(self):
        """Get the UpdateService

        :returns: the UpdateService instance
        :raises: IloError
        """
        update_service_url = self._get_update_service_path()
        try:
            return self.get_update_service(update_service_url)
        except sushy.exceptions.SushyError as e:
            msg = ('The Redfish System resource UpdateService '
                   'was not found. Error %(error)s' %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
