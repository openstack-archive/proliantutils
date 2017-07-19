# Copyright 2017 Hewlett Packard Enterprise Development LP
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
from sushy import connector
import testtools

from proliantutils import exception
from proliantutils.redfish import main
from proliantutils.redfish.resources.account_service import account_service
from proliantutils.redfish.resources.manager import manager
from proliantutils.redfish.resources.system import system
from proliantutils.redfish.resources import update_service


class HPESushyTestCase(testtools.TestCase):

    @mock.patch.object(connector, 'Connector', autospec=True)
    def setUp(self, connector_mock):
        super(HPESushyTestCase, self).setUp()
        with open('proliantutils/tests/redfish/'
                  'json_samples/root.json', 'r') as f:
            root_json = json.loads(f.read())
        connector_mock.return_value.get.return_value.json.return_value = (
            root_json)
        self.hpe_sushy = main.HPESushy('https://1.2.3.4',
                                       username='foo',
                                       password='bar')

    def test_get_system_collection_path(self):
        self.assertEqual('/redfish/v1/Systems/',
                         self.hpe_sushy.get_system_collection_path())

    def test_get_system_collection_path_missing_systems_attr(self):
        self.hpe_sushy.json.pop('Systems')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'The attribute Systems is missing',
            self.hpe_sushy.get_system_collection_path)

    @mock.patch.object(system, 'HPESystem', autospec=True)
    def test_get_system(self, mock_system):
        sys_inst = self.hpe_sushy.get_system('1234')
        self.assertIsInstance(sys_inst,
                              system.HPESystem.__class__)
        mock_system.assert_called_once_with(self.hpe_sushy._conn,
                                            '1234',
                                            self.hpe_sushy.redfish_version)

    def test_get_manager_collection_path(self):
        self.assertEqual('/redfish/v1/Managers/',
                         self.hpe_sushy.get_manager_collection_path())

    def test_get_manager_collection_path_missing_systems_attr(self):
        self.hpe_sushy.json.pop('Managers')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'The attribute Managers is missing',
            self.hpe_sushy.get_manager_collection_path)

    @mock.patch.object(manager, 'HPEManager', autospec=True)
    def test_get_manager(self, mock_manager):
        sys_inst = self.hpe_sushy.get_manager('1234')
        self.assertIsInstance(sys_inst,
                              manager.HPEManager.__class__)
        mock_manager.assert_called_once_with(self.hpe_sushy._conn,
                                             '1234',
                                             self.hpe_sushy.redfish_version)

    @mock.patch.object(update_service, 'HPEUpdateService', autospec=True)
    def test_get_update_service(self, mock_update_service):
        us_inst = self.hpe_sushy.get_update_service()
        self.assertIsInstance(us_inst,
                              update_service.HPEUpdateService.__class__)
        mock_update_service.assert_called_once_with(
            self.hpe_sushy._conn, "/redfish/v1/UpdateService/",
            self.hpe_sushy.redfish_version)

    @mock.patch.object(account_service, 'HPEAccountService', autospec=True)
    def test_get_account_service(self, mock_account_service):
        acc_inst = self.hpe_sushy.get_account_service()
        self.assertIsInstance(acc_inst,
                              account_service.HPEAccountService.__class__)
        mock_account_service.assert_called_once_with(
            self.hpe_sushy._conn, "/redfish/v1/AccountService/",
            self.hpe_sushy.redfish_version)
