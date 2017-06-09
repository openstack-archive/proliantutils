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

from proliantutils.redfish.resources import update_service


class HPEUpdateServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEUpdateServiceTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/update_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.us_inst = update_service.HPEUpdateService(
            self.conn, '/redfish/v1/UpdateService/1',
            redfish_version='1.0.2')

    def test_flash_firmware_update(self):
        firmware_update_uri = ('/redfish/v1/UpdateService/Actions/'
                               'UpdateService.SimpleUpdate/')
        self.us_inst.flash_firmware_update({'ImageURI': 'web_url'})
        self.us_inst._conn.post.assert_called_once_with(
            firmware_update_uri, data={'ImageURI': 'web_url'})
