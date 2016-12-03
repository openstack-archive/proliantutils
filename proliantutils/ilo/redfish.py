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

from proliantutils.ilo import rest_operations
from proliantutils import log


"""
Class specific for Redfish APIs.
"""

LOG = log.get_logger(__name__)


class RedfishOperations(rest_operations.IloRestOperations):

    def __init__(self, host, username, password, bios_password=None,
                 cacert=None):
        super(RedfishOperations, self).__init__(
            host, username, password, default_prefix='/redfish/v1/',
            biospassword=bios_password, cacert=cacert)

    # Note(deray): This is the list of APIs which are currently supported
    # via Redfish mode of operation. This is a growing list which needs
    # to be updated as and when the existing API/s are migrated from its
    # cousin RIS and RIBCL interfaces.
    #
    #    --- START ---
    #
    #    get_product_name(self),
    #    get_host_power_status(self),
    #    get_vm_status(self, device='FLOPPY'),
    #
    #    --- END ---
