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

from proliantutils import exception


class HPEAccountService(base.ResourceBase):
    """Class that extends the functionality of Base resource class

    This class extends the functionality of Base resource class
    from sushy
    """
    def get_account_data(self, acc_uri):
        """Get account related data

        :param acc_uri: URL to get account data
        :returns: response object of the get operation
        """
        if acc_uri is not None:
            response = self._conn.get(acc_uri)
            if response.status_code != 200:
                msg = ("%s is not a valid response code received "
                       % response.status_code)
                raise exception.IloError(msg)
            return response

    def update_credentials(self, member_uri, password):
        """Update credentials of a redfish system

        :param member_uri: URL to update credentials
        :param password: password to be updated
        :returns: response object of the patch operation
        """
        if member_uri is not None:
            return self._conn.patch(member_uri, data=password)
