# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

"""Common functionalities used by both RIBCL and RIS."""

import time

from proliantutils import exception

# Max number of times an operation to be retried
RETRY_COUNT = 5


def wait_for_ilo_after_reset(ilo_object):
    """Checks if iLO is up after reset."""

    retry_count = RETRY_COUNT
    while retry_count:
        try:
            # Delay for 5 sec, for the reset operation to take effect.
            time.sleep(10)
            ilo_object.get_product_name()
            break
        except exception.IloError:
            retry_count -= 1
    else:
        msg = ('iLO is not up after reset.')
        raise exception.IloConnectionError(msg)
