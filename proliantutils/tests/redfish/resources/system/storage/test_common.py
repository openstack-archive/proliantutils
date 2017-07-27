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

import ddt
import mock
import sushy
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system.storage import common


@ddt.ddt
class CommonMethodsTestCase(testtools.TestCase):

    def setUp(self):
        super(CommonMethodsTestCase, self).setUp()
        self.system_obj = mock.MagicMock()

    @ddt.data((953837, 60000, 60000, 60000, 60000, 930),
              (sushy.exceptions.SushyError, 1000169537536, 60000, 60000,
               60000, 930),
              (953837, sushy.exceptions.SushyError, 60000, 60000, 60000,
               930),
              (sushy.exceptions.SushyError, sushy.exceptions.SushyError,
               953837, 60000, 40000, 930),
              (sushy.exceptions.SushyError, sushy.exceptions.SushyError,
               sushy.exceptions.SushyError, 1000169537536, 40000, 930),
              (sushy.exceptions.SushyError, sushy.exceptions.SushyError,
               sushy.exceptions.SushyError, sushy.exceptions.SushyError,
               1000169537536, 930),
              )
    @ddt.unpack
    def test_get_local_gb(self, logical_max, volume_max, physical_max,
                          drive_max, simple_max, expected):

        def _mock_property(value):
            if value is sushy.exceptions.SushyError:
                mock_value = mock.PropertyMock(side_effect=value)
            else:
                mock_value = mock.PropertyMock(return_value=value)
            return mock_value
        system_obj = self.system_obj
        type(system_obj.smart_storage).logical_drives_maximum_size_mib = (
            _mock_property(logical_max))
        type(system_obj.storages).volumes_maximum_size_bytes = (
            _mock_property(volume_max))
        type(system_obj.smart_storage).physical_drives_maximum_size_mib = (
            _mock_property(physical_max))
        type(system_obj.storages).drives_maximum_size_bytes = (
            _mock_property(drive_max))
        type(system_obj.simple_storages).maximum_size_bytes = (
            _mock_property(simple_max))
        actual = common.get_local_gb(system_obj)
        self.assertEqual(expected, actual)

    def test__get_attribute_value_of(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(return_value=1000169537536)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common._get_attribute_value_of(system_obj.simple_storages,
                                                'maximum_size_bytes')
        self.assertEqual(1000169537536, actual)

    def test__get_attribute_value_of_sushy_error(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(side_effect=sushy.exceptions.SushyError)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common._get_attribute_value_of(system_obj.simple_storages,
                                                'maximum_size_bytes', value=0)
        self.assertEqual(0, actual)

    def test__get_attribute_value_of_fail_missing_attribute(self):
        system_obj = self.system_obj
        si_mock = mock.PropertyMock(
            side_effect=exception.MissingAttributeError)
        type(system_obj.simple_storages).maximum_size_bytes = si_mock
        actual = common._get_attribute_value_of(system_obj.simple_storages,
                                                'maximum_size_bytes')
        self.assertIsNone(actual)
