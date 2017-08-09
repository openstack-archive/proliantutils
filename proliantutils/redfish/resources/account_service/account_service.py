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

import functools

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
    @utils.init_and_set_resource_if_not_already(
        account.HPEAccountCollection,
        functools.partial(utils.get_subresource_path_by,
                          subresource_path='Accounts'))
    def accounts(self):
        """Property to provide instance of HPEAccountCollection"""
        return '_accounts'

    def refresh(self):
        super(HPEAccountService, self).refresh()
        self._accounts = None
