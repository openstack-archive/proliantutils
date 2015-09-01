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
