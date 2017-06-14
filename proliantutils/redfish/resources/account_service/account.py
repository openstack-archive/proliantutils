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


def get_member_uri(username, members):
    """Returns the uri of account to be updated

    :param username: username of account
    :param members: collection of accounts

    :returns account uri
    """
    for member in members:
        if member.username == username:
            return member.mem_uri


class HPEAccount(base.ResourceBase):

    username = base.Field('UserName')

    mem_uri = base.Field('@odata.id')


class HPEAccountCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return HPEAccount
