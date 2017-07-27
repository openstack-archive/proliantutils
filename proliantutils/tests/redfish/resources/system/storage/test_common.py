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


import json
import mock
import testtools

from proliantutils.redfish.resources.system.storage import common
from proliantutils.redfish.resources.system import system


class CommonMethodsTestCase(testtools.TestCase):

    def setUp(self):
        super(CommonMethodsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = system_json['default']

        self.sys_inst = system.HPESystem(self.conn, '/redfish/v1/Systems/1',
                                         redfish_version='1.0.2')

    def test_get_local_gb(self):
        system_obj = mock.Mock(self.sys_inst)
        logical_mock = mock.PropertyMock(return_value=int(953837))
        type((system_obj.return_value).smart_storage.return_value
             ).logical_drives_maximum_size_mib = logical_mock
        type((system_obj.return_value).storages.return_value
             ).volumes_maximum_size_bytes = int(60000)
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)
