# Copyright 2016 Hewlett Packard Enterprise Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from proliantutils.redfish import auth as token_auth
from sushy import connector
from sushy import main
import testtools


class TokenOnlyAuthTestCase(testtools.TestCase):

    @mock.patch.object(main, 'Sushy', autospec=True)
    @mock.patch.object(connector, 'Connector', autospec=True)
    def setUp(self, mock_connector, mock_root):
        super(TokenOnlyAuthTestCase, self).setUp()
        self.conn = mock_connector.return_value
        self.root = mock_root.return_value
        self._session_key = "Testingkey"
        self.token_auth = token_auth.TokenOnlyAuth(self._session_key)

    def test_init(self):
        self.assertEqual(self._session_key,
                         self.token_auth._session_key)

    def test_get_session_key(self):
        self.token_auth._session_key = self._session_key
        self.assertEqual(self._session_key,
                         self.token_auth.get_session_key())

    def test_authenticate(self):
        self.token_auth.set_context(self.root, self.conn)
        self.token_auth.authenticate()
        self.conn.set_http_session_auth.assert_called_once_with(
            self._session_key)

    def test_can_refresh_session(self):
        self.assertFalse(self.token_auth.can_refresh_session())

    def test_reset_session_attrs(self):
        self.token_auth._session_key = self._session_key
        self.assertEqual(self._session_key,
                         self.token_auth.get_session_key())
        self.token_auth.reset_session_attrs()
        self.assertIsNone(self.token_auth.get_session_key())
