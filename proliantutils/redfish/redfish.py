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

from six.moves.urllib import parse

from proliantutils import exception
from proliantutils.ilo import operations
from proliantutils import log
from proliantutils import rest


"""
Class specific for Redfish APIs.
"""

VALID_POWER_VALUES = {
    'ON': 'On',
    'OFF': 'ForceOff',
}

LOG = log.get_logger(__name__)


class RedfishOperations(operations.IloOperations):
    """Operations supported on redfish based hardware.

    This is the list of APIs which are currently supported via Redfish mode
    of operation. This is a growing list which needs to be updated as and when
    the existing API/s (of its cousin RIS and RIBCL interfaces) are migrated.

    --- START ---

    * get_product_name(self)
    * get_host_power_status(self)

    --- END ---

    """

    def __init__(self, redfish_controller_ip, username, password,
                 bios_password=None, cacert=None, root_prefix='/redfish/v1/'):
        """A class representing supported RedfishOperations

        :param redfish_controller_ip: The ip address of the Redfish controller.
        :param username: User account with admin/server-profile access
            privilege
        :param password: User account password
        :param bios_password: bios password
        :param cacert: a path to a CA_BUNDLE file or directory with
            certificates of trusted CAs. If set to None, the driver will
            ignore verifying the SSL certificate; if it's a path the driver
            will use the specified certificate or one of the certificates in
            the directory. Defaults to None.
        :param root_prefix: The default URL prefix. This part includes
            the root service and version. Defaults to /redfish/v1
        """
        super(RedfishOperations, self).__init__()
        self._conn = rest.RestConnectorBase(redfish_controller_ip, username,
                                            password, bios_password, cacert)
        self._root_prefix = root_prefix
        # Fetch the ServiceRoot response
        self._fetch_root_resources()

    def _fetch_root_resources(self):
        """Fetches the service root resources

        Retrieves/fetches the resources at ServiceRoot
        :raises: IloConnectionError
        """
        status, headers, service_root_resp = (
            self._conn._rest_get(self._root_prefix))
        self._root_resp = service_root_resp

    def _get_system_collection_path(self):
        """Helper function to find the SystemCollection path"""
        systems_col = self._root_resp.get('Systems')
        if not systems_col:
            raise exception.MissingAttributeError(attribute='Systems',
                                                  resource=self._root_prefix)
        return systems_col.get('@odata.id')

    def _get_system_details(self, system_id):
        """Get the system details.

        :param system_id: The identity of the System resource
        :raises: IloError
        :raises: MissingAttributeError
        """
        system_url = parse.urljoin(self._get_system_collection_path(),
                                   system_id)
        status, headers, system = self._conn._rest_get(system_url)
        return system

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        :raises: MissingAttributeError
        """
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        system = self._get_system_details('1')
        return system['Model']

    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        :raises: MissingAttributeError
        """
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        system = self._get_system_details('1')
        return system['PowerState'].upper()

    def _get_reset_system_path_for(self, system_id):
        """Gets the reset system path

        :param system_id: The identity of the System resource
        """
        system = self._get_system_details(system_id)
        actions = system.get('Actions')
        if not actions:
            raise exception.MissingAttributeError(
                attribute='Actions', resource=system.get('@odata.id'))

        reset_action = actions.get('#ComputerSystem.Reset')
        if not reset_action:
            raise exception.MissingAttributeError(
                attribute='Actions/#ComputerSystem.Reset',
                resource=system.get('@odata.id'))

        target_uri = reset_action.get('target')
        if not target_uri:
            raise exception.MissingAttributeError(
                attribute='Actions/#ComputerSystem.Reset/target',
                resource=system.get('@odata.id'))

        return target_uri

    def set_host_power(self, value):
        """Sets the power state of the system.

        :param value: The target value to be set. Value can be:
            'ON' or 'OFF'.
        :raises: IloError, on an error from iLO.
        :raises: InvalidInputError, if the target value is not
            allowed.
        """
        if value not in VALID_POWER_VALUES:
            msg = ('The parameter "%(parameter)s" value "%(value)s" is '
                   'invalid. Valid values are: %(valid_power_values)s' %
                   {'parameter': 'value', 'value': value,
                    'valid_power_values': VALID_POWER_VALUES.keys()})
            raise exception.InvalidInputError(msg)

        # Check current power status, do not act if it's in requested state.
        current_power_status = self.get_host_power_status()
        if current_power_status == value:
            LOG.debug(self._("Node is already in '%(value)s' power state."),
                      {'value': value})
            return

        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        target_uri = self._get_reset_system_path_for('1')

        target_value = VALID_POWER_VALUES[value]
        self._conn._rest_post(target_uri, None,
                              {'ResetType': target_value})
