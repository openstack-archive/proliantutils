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

"""Test class for Utils Module."""

import json

import ddt
import mock
import testtools

from sushy.resources import base

from proliantutils import exception
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system import system
from proliantutils.redfish import utils


@ddt.ddt
class UtilsTestCase(testtools.TestCase):

    def setUp(self):
        super(UtilsTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/system.json', 'r') as f:
            system_json = json.loads(f.read())
        self.conn.get.return_value.json.return_value = system_json['default']

        self.sys_inst = system.HPESystem(self.conn, '/redfish/v1/Systems/1',
                                         redfish_version='1.0.2')

    @ddt.data(('SecureBoot', '/redfish/v1/Systems/1/SecureBoot/'),
              (['Oem', 'Hpe', 'Links', 'NetworkAdapters'],
               '/redfish/v1/Systems/1/NetworkAdapters/'),
              )
    @ddt.unpack
    def test_get_subresource_path_by(self, subresource_path, expected_result):
        value = utils.get_subresource_path_by(self.sys_inst,
                                              subresource_path)
        self.assertEqual(expected_result, value)

    @ddt.data(('NonSecureBoot', 'attribute NonSecureBoot is missing'),
              (['Links', 'Chassis'],
               'attribute Links/Chassis/@odata.id is missing'),
              )
    @ddt.unpack
    def test_get_subresource_path_by_when_fails(
            self, subresource_path, expected_exception_string_subset):
        self.assertRaisesRegex(
            exception.MissingAttributeError,
            expected_exception_string_subset,
            utils.get_subresource_path_by,
            self.sys_inst, subresource_path)

    def test_get_subresource_path_by_fails_with_empty_path(self):
        self.assertRaisesRegex(
            ValueError,
            '"subresource_path" cannot be empty',
            utils.get_subresource_path_by,
            self.sys_inst, [])

    @ddt.data((sys_cons.SUPPORTED_LEGACY_BIOS_ONLY,
               ('true', 'false')),
              (sys_cons.SUPPORTED_UEFI_ONLY,
               ('false', 'true')),
              (sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI,
               ('true', 'true')))
    @ddt.unpack
    def test_get_supported_boot_modes(self, boot_mode,
                                      expected_boot_modes):
        actual_boot_modes = utils.get_supported_boot_mode(boot_mode)
        self.assertEqual(expected_boot_modes, actual_boot_modes)

    @ddt.data(('SecureBoot', ['HEAD', 'GET', 'PATCH', 'POST']),
              ('Bios', ['GET', 'HEAD']))
    @ddt.unpack
    def test_get_allowed_operations(self, subresource_path, expected):
        response_mock = mock.MagicMock()
        response_mock.headers = {'Allow': expected}
        self.conn.get.return_value = response_mock
        ret_val = utils.get_allowed_operations(self.sys_inst, subresource_path)
        self.assertEqual(ret_val, expected)

    @ddt.data(('PATCH', 'SecureBoot', ['HEAD', 'GET', 'PATCH', 'POST'], True),
              ('POST', 'Bios', ['GET', 'HEAD'], False))
    @ddt.unpack
    @mock.patch.object(utils, 'get_allowed_operations')
    def test_is_operation_allowed(self, method, subresource_path,
                                  allowed_operations, expected,
                                  get_method_mock):
        get_method_mock.return_value = allowed_operations
        ret_val = utils.is_operation_allowed(method, self.sys_inst,
                                             subresource_path)
        self.assertEqual(ret_val, expected)

    @ddt.data(([2, 4, 6], 6),
              ([], 0))
    @ddt.unpack
    def test_max_safe(self, iterable, expected):
        actual = utils.max_safe(iterable)
        self.assertEqual(expected, actual)


class NestedResource(base.ResourceBase):

    def _parse_attributes(self):
        pass

    def some_init_operation(self):
        pass


class BaseResource(base.ResourceBase):

    _nested_resource = None
    _a = None
    _b = None

    def _parse_attributes(self):
        pass

    @utils.lazy_load_and_cache('_nested_resource')
    def get_nested_resource(self):
        nested_res = NestedResource(
            self._conn, "Path / Identity to NestedResource",
            redfish_version=self.redfish_version)
        nested_res.some_init_operation()
        return nested_res

    @property
    @utils.lazy_load_and_cache('_a')
    def a(self):
        return 1

    @a.setter
    def a(self, value):
        self._a = value

    @property
    @utils.lazy_load_and_cache('_b', should_set_attribute=False)
    def b(self):
        self._b = {'hi': 'little chap'}
        # Do some complex calculation. Update the intrinsic value.
        # No need to return any value.
        self._b.update({'Hello': 'Ladies and gentlemen'})

    @b.setter
    def b(self, value):
        self._b = value


class LazyLoadAndCacheTestCase(testtools.TestCase):

    def setUp(self):
        super(LazyLoadAndCacheTestCase, self).setUp()
        self.conn = mock.Mock()
        self.res = BaseResource(connector=self.conn, path='/Foo',
                                redfish_version='1.0.2')

    def test_lazy_load_and_cache(self):
        self.assertIsNone(self.res._a)
        result = self.res.a
        self.assertEqual(1, result)
        self.assertEqual(result, self.res._a)

        # Checking for non-None value
        self.res.a = 2
        self.assertEqual(2, self.res.a)

    def test_lazy_load_and_cache_should_not_set_attribute(self):
        self.assertIsNone(self.res._b)
        result = self.res.b
        self.assertEqual({'hi': 'little chap',
                          'Hello': 'Ladies and gentlemen'}, result)
        self.assertEqual(result, self.res._b)

        # Checking for non-None value
        self.res.b = 100
        self.assertEqual(100, self.res.b)

    def test_lazy_load_and_cache_fail(self):
        self.assertRaisesRegex(
            TypeError,
            "Invalid argument type provided:",
            utils.lazy_load_and_cache,
            {})

    @mock.patch.object(NestedResource, 'some_init_operation')
    def test_lazy_load_and_cache_resource(self, some_init_operation_mock):
        self.assertIsNone(self.res._nested_resource)
        nested_res = self.res.get_nested_resource()
        self.assertIsInstance(nested_res, NestedResource)
        self.assertEqual(nested_res, self.res._nested_resource)
        self.assertTrue(some_init_operation_mock.called)

        some_init_operation_mock.reset_mock()
        # verify subsequent invocation
        self.assertEqual(nested_res, self.res.get_nested_resource())
        self.assertFalse(some_init_operation_mock.called)
