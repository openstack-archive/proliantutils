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

import json
import mock

from proliantutils.redfish import auth as token_auth
from proliantutils.redfish import connector
from sushy.tests.unit import base


class TokenOnlyAuthTestCase(base.TestCase):

    @mock.patch.object(connector, 'HPEConnector', autospec=True)
    def setUp(self, mock_connector):
        super(TokenOnlyAuthTestCase, self).setUp()
        with open('proliantutils/tests/redfish/'
                  'json_samples/root.json', 'r') as f:
            root_json = json.loads(f.read())
        mock_connector.return_value.get.return_value.json.return_value = (
            root_json)

        self._session_key = "Testingkey" 
        self.token_auth = token_auth.TokenOnlyAuth(self._session_key)
        self.conn = mock_connector 

    def test_init(self):
        self.assertEqual(self._session_key,
                         self.token_auth._session_key)

    def test_get_session_key(self):
        self.token_auth._session_key = self._session_key
        self.assertEqual(self._session_key,
                         self.token_auth.get_session_key())

    def test__do_authenticate(self):
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
