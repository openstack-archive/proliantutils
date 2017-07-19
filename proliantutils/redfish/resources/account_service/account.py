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

from sushy.resources import base


class HPEAccount(base.ResourceBase):
    """Class that defines the functionality for Account."""

    username = base.Field('UserName')

    def update_credentials(self, password):
        """Update credentials of a redfish system

        :param password: password to be updated
        """
        data = {
            'Password': password,
        }
        self._conn.patch(self.path, data=data)


class HPEAccountCollection(base.ResourceCollectionBase):
    """Class that defines the functionality for AccountCollection."""

    @property
    def _resource_type(self):
        return HPEAccount

    def get_member_details(self, username):
        """Returns the HPEAccount object

        :param username: username of account
        :returns: HPEAccount object if criterion matches, None otherwise
        """
        members = self.get_members()
        for member in members:
            if member.username == username:
                return member
