# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

"""Logger utility for proliantutils"""

import functools
import logging

base_logger = logging.getLogger('proliantutils')
base_logger.addHandler(logging.NullHandler())


def get_logger(name):
    """Return a logger with the specified name

    If no name is specified then it returns the base logger
    with the name, 'proliantutils'.

    :param name: logger name
    """
    if not name:
        return base_logger

    logger = logging.getLogger(name)
    return logger


def get_ilo_contextual_logger(name):
    """Return an ilo contextual logger with the specified name

    If no name is specified then it returns the base logger
    with the name, 'proliantutils'. The returned logger will
    have some extra methods of providing the ilo info as the prefix
    of every log statement. Those extra ability methods are the
    corresponding shortened api/s of the well known log functions.
    E.g.
        d ---> will delegate to `debug` with ilo info prepended
        c ---> will delegate to `critical` with ilo info prepended

    :param name: logger name
    """
    logger = get_logger(name)
    return IloContextualLogger(logger)


def _ilo_info_coercing_decorator(log_func):
    @functools.wraps(log_func)
    def wrapped_func(self, host, msg, *args, **kwargs):
        ilo_info_coerced_message = self._get_ilo_contextual_log_msg(host,
                                                                    msg)
        log_func(self, None, ilo_info_coerced_message, *args, **kwargs)

    return wrapped_func


class IloContextualLogger(logging.LoggerAdapter):
    """Custom Logger Adapter class with ILO contextual info

    This adapter has additional log functions along with the usual
    log functions and the names being the shortened format for their
    corresponding cousins and taking an extra parameter(ilo host info)
    as the first parameter. This ilo info is prepended to the log message.
    """
    def __init__(self, logger, extra=None):
        super(IloContextualLogger, self).__init__(logger, extra)

    @_ilo_info_coercing_decorator
    def d(self, host, msg, *args, **kwargs):
        """Delegate a debug call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.debug(msg, *args, **kwargs)

    @_ilo_info_coercing_decorator
    def i(self, host, msg, *args, **kwargs):
        """Delegate a info call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.info(msg, *args, **kwargs)

    @_ilo_info_coercing_decorator
    def w(self, host, msg, *args, **kwargs):
        """Delegate a warning call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.warning(msg, *args, **kwargs)

    @_ilo_info_coercing_decorator
    def e(self, host, msg, *args, **kwargs):
        """Delegate a error call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.error(msg, *args, **kwargs)

    @_ilo_info_coercing_decorator
    def c(self, host, msg, *args, **kwargs):
        """Delegate a critical call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.critical(msg, *args, **kwargs)

    @_ilo_info_coercing_decorator
    def exc(self, host, msg, *args, **kwargs):
        """Delegate a exception call to the underlying logger

        Prepends the ilo contextual information while delegating the call.
        :param host: ilo host address
        :param msg: log message
        """
        self.exception(msg, *args, **kwargs)

    def _get_ilo_contextual_log_msg(self, host, msg):
        """Message formatter with ilo info

        Returns the log message by prepending the ilo host address.
        :param host: ilo host address
        :param msg: log message
        """
        new_msg = '[iLO:{0}] {1}'.format(host, msg)
        return new_msg
