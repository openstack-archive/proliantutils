# Copyright 2016 Hewlett Packard Enterprise Development LP
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
"""Test Class for Exception."""

import unittest

import ddt

from proliantutils import exception


@ddt.ddt
class ExceptionTestCase(unittest.TestCase):

    def setUp(self):
        super(ExceptionTestCase, self).setUp()

    @ddt.data(('check your input',   # input - exception message
               None,                 # input - exception kwargs
               'check your input'),  # expected raised exception message

              ('check your input. %(reason)s',
               {'reason': 'invalid input provided'},
               'check your input. invalid input provided'),

              ('check your input. %(why)s',
               {'why': 'invalid input provided'},
               'check your input. invalid input provided'),

              ("just check your input.. that's all. no any reason given",
               {'reason': 'some reason'},
               "just check your input.. that's all. no any reason given"),

              (None,
               {'reason': 'Input not supported'},
               'Invalid Input: Input not supported'),

              (None,
               None,
               'Invalid Input: Unknown'),)
    @ddt.unpack
    def test_InvalidInputError(self, input_exc_message, input_exc_kwargs,
                               expected_exc_message):
        # | GIVEN |
        def raising_invalid_input_error_exc_with(msg, **kwargs):
            raise exception.InvalidInputError(msg, **kwargs)

        input_exc_kwargs = input_exc_kwargs or {}
        # | WHEN | & | THEN |
        with self.assertRaises(exception.InvalidInputError) as cm:
            raising_invalid_input_error_exc_with(input_exc_message,
                                                 **input_exc_kwargs)

        the_exception = cm.exception
        self.assertEqual(expected_exc_message, str(the_exception))
