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

from proliantutils import log
from proliantutils.rest import rest_operations


"""
Class specific for RIS APIs.
"""

LOG = log.get_logger(__name__)


class RISOperations(rest_operations.RestOperations):

    def __init__(self, host, username, password, bios_password=None,
                 cacert=None):
        super(RISOperations, self).__init__(host, username, password,
                                            biospassword=bios_password,
                                            cacert=cacert)
