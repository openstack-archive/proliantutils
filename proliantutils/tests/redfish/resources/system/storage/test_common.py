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
        self.system_obj = mock.MagicMock()

    def test_get_local_gb_volumes_logical_1(self):
        logical_mock = mock.PropertyMock(return_value=953837)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=60000)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_volumes_logical(self):
        logical_mock = mock.PropertyMock(return_value=953837)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=60000)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_volumes(self):
        logical_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=1000169537536)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_logical(self):
        logical_mock = mock.PropertyMock(return_value=953837)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives_and_physical_drives(self):
        logical_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=953837)
        type(self.system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=60000)
        type(self.system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=40000)
        type(self.system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives(self):
        logical_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=1000169537536)
        type(self.system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=40000)
        type(self.system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_physical_drives(self):
        logical_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=953837)
        type(self.system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_simple_storage(self):
        logical_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).logical_drives_maximum_size_mib = (
            logical_mock)
        vol_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=0)
        type(self.system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=1000169537536)
        type(self.system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(self.system_obj)
        self.assertEqual(expected, actual)
