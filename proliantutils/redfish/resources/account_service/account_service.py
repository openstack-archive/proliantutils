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

from proliantutils.redfish.resources.account_service import account
from proliantutils.redfish import utils


class HPEAccountService(base.ResourceBase):
    """Class that extends the functionality of Base resource class

    This class extends the functionality of Base resource class
    from sushy
    """

    _account = None

    def update_credentials(self, member_uri, password):
        """Update credentials of a redfish system

        :param member_uri: URL to update credentials
        :param password: password to be updated
        :returns: response object of the patch operation
        """
        if member_uri is not None:
            return self._conn.patch(member_uri, data=password)

    @property
    def account(self):
        """Property to provide reference to account resources instance

        """
        if self._account is None:
            self._account = account.HPEAccountCollection(
                self._conn, utils.get_subresource_path_by(self, ('Accounts')),
                redfish_version=self.redfish_version)

        return self._account
