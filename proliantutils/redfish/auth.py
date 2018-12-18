# Copyright 2018 Hewlett Packard Enterprise Development LP
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

from sushy import auth


class TokenOnlyAuth(auth.AuthBase):
    """Session Authentication class.

       This is a class used to encapsulate a redfish session.
    """

    def __init__(self, session_key=None):
        """A class representing a Session Authentication object.

        :param username: User account with admin/server-profile access
             privilege.
        :param password: User account password.
        """
        self._session_key = session_key
        super(TokenOnlyAuth, self).__init__(session_key)

    def get_session_key(self):
        """Returns the session key.

        :returns: The session key.
        """
        return self._session_key

    def _do_authenticate(self):
        """Establish a redfish session.

        :raises: MissingXAuthToken
        :raises: ConnectionError
        :raises: AccessError
        :raises: HTTPError
        """
        self._connector.set_http_session_auth(self._session_key)

    def can_refresh_session(self):
        """Method to assert if session based refresh can be done."""
        return False

    def close(self):
        """Close the Redfish Session.

        Attempts to close an established RedfishSession by
        deleting it from the remote Redfish controller.
        """
        pass

    def reset_session_attrs(self):
        """Reset active session related attributes."""
        self._session_key = None
