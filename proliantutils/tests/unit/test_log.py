# Copyright 2015 Hewlett-Packard Development Company, L.P.
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
"""Test Class for Log."""

import unittest

import ddt

from proliantutils import log


@ddt.ddt
class LogTestCase(unittest.TestCase):

    def setUp(self):
        super(LogTestCase, self).setUp()

    @ddt.data(('pear',),
              ('apple',),
              ('banana',),)
    @ddt.unpack
    def test_get_logger_returns_the_same_logger_for_a_given_name(
            self, logger_name):
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger1 = log.get_logger(logger_name)
        logger2 = log.get_logger(logger_name)
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertIs(logger1, logger2)

    def test_get_logger_returns_the_base_logger_for_no_name(self):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        base_logger = log.get_logger('proliantutils')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger1 = log.get_logger(None)
        logger2 = log.get_logger('')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        self.assertIs(logger1, base_logger)
        self.assertIs(logger2, base_logger)
