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
    """Class that extends the functionality of AccountService resource class

    This class extends the functionality of Account resource class
    from sushy
    """

    _accounts = None

    @property
    @utils.lazy_load_and_cache_resource('_accounts')
    def accounts(self):
        """Property to provide instance of HPEAccountCollection"""
        return account.HPEAccountCollection(
            self._conn, utils.get_subresource_path_by(self, 'Accounts'),
            redfish_version=self.redfish_version)

    def refresh(self):
        super(HPEAccountService, self).refresh()
        self._accounts = None
