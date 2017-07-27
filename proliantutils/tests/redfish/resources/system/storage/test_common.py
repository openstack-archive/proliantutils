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

    def test_get_local_gb_volumes_logical(self):
        system_obj = self.sys_inst
        logical_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        type(system_obj.storages).volumes_maximum_size_bytes = 60000
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_volumes(self):
        system_obj = self.sys_inst
        logical_mock = mock.PropertyMock(return_value=0)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        type(system_obj.storages).volumes_maximum_size_bytes = 1000169537536
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_logical(self):
        system_obj = self.sys_inst
        logical_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        type(system_obj.storages).volumes_maximum_size_bytes = 0
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives_and_physical_drives(self):
        system_obj = self.sys_inst
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = 0
        type(system_obj.storages).volumes_maximum_size_bytes = 0
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            953837)
        type(system_obj.storages).drives_maximum_size_bytes = 60000
        type(system_obj.simple_storages).maximum_size_bytes = 40000
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives(self):
        system_obj = self.sys_inst
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = 0
        type(system_obj.storages).volumes_maximum_size_bytes = 0
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = 0
        type(system_obj.storages).drives_maximum_size_bytes = 1000169537536
        type(system_obj.simple_storages).maximum_size_bytes = 40000
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_physical_drives(self):
        system_obj = self.sys_inst
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = 0
        type(system_obj.storages).volumes_maximum_size_bytes = 0
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            953837)
        type(system_obj.storages).drives_maximum_size_bytes = 0
        type(system_obj.simple_storages).maximum_size_bytes = 0
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_simple_storage(self):
        system_obj = self.sys_inst
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = 0
        type(system_obj.storages).volumes_maximum_size_bytes = 0
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = 0
        type(system_obj.storages).drives_maximum_size_bytes = 0
        type(system_obj.simple_storages).maximum_size_bytes = 1000169537536
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)
