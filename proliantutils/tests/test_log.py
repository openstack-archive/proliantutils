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
import mock

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

    @mock.patch.object(log.logging.LoggerAdapter, 'debug', autospec=True)
    def test_ilo_contextual_logger_calls_debug_when_invoked_thru_d(
            self, adapter_debug_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.d('1.2.3.4', 'debug msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_debug_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] debug msg with %d %s', 2,
            'parameters')

    @mock.patch.object(log.logging.LoggerAdapter, 'info', autospec=True)
    def test_ilo_contextual_logger_calls_info_when_invoked_thru_i(
            self, adapter_info_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.i('1.2.3.4', 'info msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_info_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] info msg with %d %s', 2,
            'parameters')

    @mock.patch.object(log.logging.LoggerAdapter, 'warning', autospec=True)
    def test_ilo_contextual_logger_calls_warning_when_invoked_thru_w(
            self, adapter_warning_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.w('1.2.3.4', 'warning msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_warning_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] warning msg with %d %s', 2,
            'parameters')

    @mock.patch.object(log.logging.LoggerAdapter, 'error', autospec=True)
    def test_ilo_contextual_logger_calls_error_when_invoked_thru_e(
            self, adapter_error_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.e('1.2.3.4', 'error msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_error_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] error msg with %d %s', 2,
            'parameters')

    @mock.patch.object(log.logging.LoggerAdapter, 'critical', autospec=True)
    def test_ilo_contextual_logger_calls_critical_when_invoked_thru_c(
            self, adapter_critical_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.c('1.2.3.4', 'critical msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_critical_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] critical msg with %d %s', 2,
            'parameters')

    @mock.patch.object(log.logging.LoggerAdapter, 'exception', autospec=True)
    def test_ilo_contextual_logger_calls_exception_when_invoked_thru_exc(
            self, adapter_exception_mock):
        # -----------------------------------------------------------------------
        # GIVEN
        # -----------------------------------------------------------------------
        logger = log.get_ilo_contextual_logger('my_module')
        # -----------------------------------------------------------------------
        # WHEN
        # -----------------------------------------------------------------------
        logger.exc('1.2.3.4', 'exception msg with %d %s', 2, 'parameters')
        # -----------------------------------------------------------------------
        # THEN
        # -----------------------------------------------------------------------
        adapter_exception_mock.assert_called_once_with(
            logger, '[iLO:1.2.3.4] exception msg with %d %s', 2,
            'parameters')
