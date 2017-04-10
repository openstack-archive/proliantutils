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
import testtools

from proliantutils import exception
from proliantutils.redfish import redfish
from proliantutils import rest


class RedfishOperationsTestCase(testtools.TestCase):

    @mock.patch.object(rest, 'RestConnectorBase', autospec=True)
    def setUp(self, rest_connector_mock):
        super(RedfishOperationsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        rest_connector_mock.return_value = self.conn
        with open('proliantutils/tests/redfish/'
                  'json_samples/root.json', 'r') as f:
            self.conn._rest_get.return_value = 200, None, json.loads(f.read())

        self.rf_client = redfish.RedfishOperations(
            '1.2.3.4', username='foo', password='bar')
        rest_connector_mock.assert_called_once_with(
            '1.2.3.4', 'foo', 'bar', None, None)

    def test__fetch_root_resources(self):
        rf_client = self.rf_client
        rf_client._fetch_root_resources()
        self.assertEqual('HPE RESTful Root Service',
                         rf_client._root_resp.get('Name'))
        self.assertEqual('1.0.0', rf_client._root_resp.get('RedfishVersion'))
        self.assertEqual('7704b47b-2fbe-5920-99a5-b766dd84cc28',
                         rf_client._root_resp.get('UUID'))
        for resource in ['Systems', 'Managers', 'Chassis']:
            self.assertTrue(resource in rf_client._root_resp)

    def test__get_system_collection_path(self):
        self.assertEqual('/redfish/v1/Systems/',
                         self.rf_client._get_system_collection_path())

    def test__get_system_collection_path_missing_systems_attr(self):
        self.rf_client._root_resp.pop('Systems')
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            'The attribute Systems is missing',
            self.rf_client._get_system_collection_path)

    def test_get_product_name(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn._rest_get.return_value = 200, None, json.loads(f.read())
        product_name = self.rf_client.get_product_name()
        self.assertEqual('ProLiant DL180 Gen10', product_name)

    def test_get_host_power_status(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            self.conn._rest_get.return_value = 200, None, json.loads(f.read())
        power_state = self.rf_client.get_host_power_status()
        self.assertEqual('ON', power_state)
