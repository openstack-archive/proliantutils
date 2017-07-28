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


import mock
import sushy
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system.storage import common


class CommonMethodsTestCase(testtools.TestCase):

    def setUp(self):
        super(CommonMethodsTestCase, self).setUp()
        self.system_obj = mock.MagicMock()

    def test_get_local_gb_volumes_logical(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(return_value=60000)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_volumes(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(return_value=1000169537536)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_logical(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives_and_physical_drives(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=60000)
        type(system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=40000)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_drives(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(return_value=1000169537536)
        type(system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=40000)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_physical_drives(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(return_value=953837)
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_local_gb_simple_storage(self):
        system_obj = self.system_obj
        log_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            log_mock)
        vol_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).volumes_maximum_size_bytes = vol_mock
        phy_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            phy_mock)
        dr_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.storages).drives_maximum_size_bytes = dr_mock
        si_mock = mock.PropertyMock(return_value=1000169537536)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        expected = 930
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test_get_safely_value_of(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(return_value=1000169537536)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common.get_safely_value_of(system_obj.simple_storages,
                                            'maximum_size_bytes')
        self.assertEqual(1000169537536, actual)

    def test_get_safely_value_of_sushy_error(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common.get_safely_value_of(system_obj.simple_storages,
                                            'maximum_size_bytes')
        self.assertEqual(0, actual)

    def test_get_safely_value_of_fail_missing_attribute(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(
            side_effect=exception.MissingAttributeError)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common.get_safely_value_of(system_obj.simple_storages,
                                            'maximum_size_bytes')
        self.assertEqual(0, actual)

    def test_has_ssd(self):
        obj = self.system_obj
        phy_mock = mock.PropertyMock(return_value=True)
        type(obj.smart_storage.array_controllers.physical_drive).has_ssd = (
            phy_mock)
        drive_mock = mock.PropertyMock(return_value=None)
        type(obj.storage.drive).has_ssd = drive_mock
        self.assertTrue(common.has_ssd(obj))

    def test_has_rotational(self):
        obj = self.system_obj
        phy_mock = mock.PropertyMock(return_value=True)
        type(obj.smart_storage.array_controllers.
             physical_drive).has_rotational = phy_mock
        drive_mock = mock.PropertyMock(return_value=None)
        type(obj.storage.drive).has_rotational = drive_mock
        self.assertTrue(common.has_rotational(obj))

    def test_drive_rotational_speed_rpm(self):
        obj = self.system_obj
        phy_mock = mock.PropertyMock(
            return_value={'drive_rotational_15000_rpm': 'true'})
        type(obj.smart_storage.array_controllers.
             physical_drive).drive_rotational_speed_rpm = phy_mock
        drive_mock = mock.PropertyMock(
            return_value={'drive_rotational_10000_rpm': 'true'})
        type(obj.storage.drive).drive_rotational_speed_rpm = drive_mock
        expected = {'drive_rotational_15000_rpm': 'true',
                    'drive_rotational_10000_rpm': 'true'}
        actual = common.drive_rotational_speed_rpm(obj)
        self.assertEqual(actual, expected)

    def test_logical_raid_levels(self):
        obj = self.system_obj
        log_mock = mock.PropertyMock(return_value={'logical_raid_level_0':
                                                   'true'})
        type(obj.smart_storage.array_controllers.
             logical_drive).logical_raid_level = log_mock
        vol_mock = mock.PropertyMock(return_value={'logical_raid_level_1':
                                                   'true'})
        type(obj.storage.volume).logical_raid_level = vol_mock
        expected = {'logical_raid_level_0': 'true',
                    'logical_raid_level_1': 'true'}
        actual = common.logical_raid_levels(obj)
        self.assertEqual(expected, actual)

    def test_has_nvme_ssd(self):
        obj = self.system_obj
        phy_mock = mock.PropertyMock(return_value=True)
        type(obj.smart_storage.array_controllers.
             physical_drive).has_nvme_ssd = (phy_mock)
        drive_mock = mock.PropertyMock(return_value=None)
        type(obj.storage.drive).has_nvme_ssd = drive_mock
        self.assertTrue(common.has_nvme_ssd(obj))
