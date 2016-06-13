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

from proliantutils import exception


class ExceptionTestCase(unittest.TestCase):

    def setUp(self):
        super(ExceptionTestCase, self).setUp()

    def test_InvalidInputError(self):
        # | GIVEN |
        def raising_invalid_input_error_exc_with(msg, **kwargs):
            raise exception.InvalidInputError(msg, **kwargs)

        # | WHEN | & | THEN |
        self.assertRaisesRegexp(exception.InvalidInputError,
                                'check your input',
                                raising_invalid_input_error_exc_with,
                                'check your input')
        self.assertRaisesRegexp(exception.InvalidInputError,
                                'check your input. invalid input provided',
                                raising_invalid_input_error_exc_with,
                                'check your input. %(reason)s',
                                reason='invalid input provided')
        self.assertRaisesRegexp(exception.InvalidInputError,
                                "just check your input.. that's all",
                                raising_invalid_input_error_exc_with,
                                "just check your input.. that's all",
                                reason='invalid input provided')
        self.assertRaisesRegexp(exception.InvalidInputError,
                                'Invalid Input: Input not supported',
                                raising_invalid_input_error_exc_with,
                                None,
                                reason='Input not supported')
        self.assertRaisesRegexp(exception.InvalidInputError,
                                'check your input. invalid input provided',
                                raising_invalid_input_error_exc_with,
                                'check your input. %(why)s',
                                why='invalid input provided')
        self.assertRaisesRegexp(exception.InvalidInputError,
                                'Invalid Input: Unknown',
                                raising_invalid_input_error_exc_with,
                                None)
