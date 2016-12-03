# Copyright 2017 Hewlett Packard Enterprise Development Company, L.P.
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
from proliantutils.rest import rest_operations


"""
Class specific for Redfish APIs.
"""

LOG = log.get_logger(__name__)


class RedfishOperations(rest_operations.RestOperations):
    """Operations supported on redfish based hardware.

    This is the list of APIs which are currently supported via Redfish mode
    of operation. This is a growing list which needs to be updated as and when
    the existing API/s are migrated from its cousin RIS and RIBCL interfaces.

    --- START ---

    * get_product_name(self)
    * get_host_power_status(self)
    * get_vm_status(self, device='FLOPPY')
    * insert_virtual_media(self, url, device='FLOPPY')
    * eject_virtual_media(self, device='FLOPPY')

    --- END ---

    """

    def __init__(self, host, username, password, bios_password=None,
                 cacert=None):
        super(RedfishOperations, self).__init__(
            host, username, password, default_prefix='/redfish/v1/',
            biospassword=bios_password, cacert=cacert)

    # Override
    def _get_collection(self, collection_uri, request_headers=None):
        """Generator function that returns collection members."""

        # get the collection
        status, headers, thecollection = self._rest_get(collection_uri)

        if status != 200:
            msg = self._get_extended_error(thecollection)
            raise exception.IloError(msg)

        for member in thecollection['Members']:
            memberuri = member['@odata.id']
            yield 200, None, member, memberuri

    # Override
    def _get_type(self, obj):
        """Return the type of an object."""
        typever = obj['@odata.type']
        typesplit = typever.split('.')
        return typesplit[0] + '.' + typesplit[1]

    # Override
    def _get_host_details(self):
        """Get the system details."""
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        status, headers, system = self._rest_get('/Systems/1')
        if status < 300:
            stype = self._get_type(system)
            if (stype not in
                    ['#ComputerSystem.v1_1_0', '#ComputerSystem.v1_2_0',
                     '#ComputerSystem.v1_0_0']):
                msg = "%s is not a valid system type " % stype
                raise exception.IloError(msg)
        else:
            msg = self._get_extended_error(system)
            raise exception.IloError(msg)

        return system

    # Override
    def _get_ilo_details(self):
        """Gets iLO details

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        manager_uri = '/Managers/1'
        status, headers, manager = self._rest_get(manager_uri)

        if status != 200:
            msg = self._get_extended_error(manager)
            raise exception.IloError(msg)

        # verify expected type
        mtype = self._get_type(manager)
        if (mtype not in ['#Manager.v1_0_0', '#Manager.v1_1_0']):
            msg = "%s is not a valid Manager type " % mtype
            raise exception.IloError(msg)

        return manager, manager_uri

    # Override
    def _get_vm_device_status(self,  device='FLOPPY'):
        """Returns the given virtual media device status and device URI

        :param  device: virtual media device to be queried
        :returns json format virtual media device status and its URI
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        valid_devices = {'FLOPPY': 'floppy',
                         'CDROM': 'cd'}

        # Check if the input is valid
        if device not in valid_devices:
                raise exception.IloInvalidInputError(
                    "Invalid device. Valid devices: FLOPPY or CDROM.")

        manager, uri = self._get_ilo_details()
        try:
            vmedia_uri = manager['VirtualMedia']['@odata.id']
        except KeyError:
            msg = ('"VirtualMedia" section in Manager does not exist')
            raise exception.IloCommandNotSupportedError(msg)

        for status, hds, vmed, memberuri in self._get_collection(vmedia_uri):
            status, headers, response = self._rest_get(memberuri)
            if status != 200:
                msg = self._get_extended_error(response)
                raise exception.IloError(msg)

            if (valid_devices[device] in
               [item.lower() for item in response['MediaTypes']]):
                vm_device_uri = response['@odata.id']
                return response, vm_device_uri

        # Requested device not found
        msg = ('Virtualmedia device "' + device + '" is not'
               ' found on this system.')
        raise exception.IloError(msg)

    # Override
    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """

        data = self._get_host_details()
        return data['PowerState'].upper()
