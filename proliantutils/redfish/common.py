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

"""Common functionalities used by redfish."""

import time

from proliantutils import exception
from proliantutils import log


LOG = log.get_logger(__name__)


def wait_for_operation_to_complete(
        has_operation_completed, retries=10, delay_bw_retries=5,
        delay_before_attempts=5, failover_exc=exception.IloError,
        failover_msg=("Operation did not complete even after multiple "
                      "attempts."), is_silent_loop_exit=False):
    """Attempts the provided operation for a specified number of times.

    If it runs out of attempts, then it raises an exception. On success,
    it breaks out of the loop.
    :param has_operation_completed: the method to retry and it needs to return
                                    a boolean to indicate success or failure.
    :param retries: number of times the operation to be (re)tried, default 10
    :param delay_bw_retries: delay in seconds before attempting after
                             each failure, default 5.
    :param delay_before_attempts: delay in seconds before beginning any
                                  operation attempt, default 10.
    :param failover_exc: the exception which gets raised in case of failure
                         upon exhausting all the attempts, default IloError.
    :param failover_msg: the msg with which the exception gets raised in case
                         of failure upon exhausting all the attempts.
    :param is_silent_loop_exit: decides if exception has to be raised (in case
                                of failure upon exhausting all the attempts)
                                or not, default False (will be raised).
    :raises: failover_exc, if failure happens even after all the attempts,
             default IloError.
    """
    retry_count = retries
    # Delay for ``delay_before_attempts`` secs, before beginning any attempt
    time.sleep(delay_before_attempts)
    while retry_count:
        try:
            LOG.debug("Calling '%s', retries left: %d",
                      has_operation_completed.__name__, retry_count)
            if has_operation_completed():
                break
        except exception.IloError:
            pass
        time.sleep(delay_bw_retries)
        retry_count -= 1
    else:
        LOG.debug("Max retries exceeded with: '%s'",
                  has_operation_completed.__name__)
        if not is_silent_loop_exit:
            raise failover_exc(failover_msg)


def wait_for_ilo_after_reset(ilo_object):
    """Continuously polls for iLO to come up after reset."""

    is_ilo_up_after_reset = lambda: ilo_object.get_product_name() is not None
    is_ilo_up_after_reset.__name__ = 'is_ilo_up_after_reset'

    wait_for_operation_to_complete(
        is_ilo_up_after_reset,
        failover_exc=exception.IloConnectionError,
        failover_msg='iLO is not up after reset.'
    )


def wait_for_ilo_firmware_update_to_complete(redfish_object):
    """Continuously polls for iLO firmware update to complete."""

    p_state = ['Idle']
    c_state = ['Idle']

    def has_firmware_flash_completed():
        """Checks for completion status of firmware update operation

        The below table shows the conditions for which the firmware update
        will be considered as DONE (be it success or error)::

        +-----------------------------------+------------------------------+
        |    Previous state                 |   Current state              |
        +===================================+==============================+
        |    Idle                           |   Error, Complete            |
        +-----------------------------------+------------------------------+
        |    Updating, Verifying,           |   Complete, Error,           |
        |    Uploading, Writing             |   Unknown, Idle              |
        +-----------------------------------+------------------------------+
        """
        curr_state, curr_percent = redfish_object. \
            get_firmware_update_progress()
        p_state[0] = c_state[0]
        c_state[0] = curr_state
        if (((p_state[0] in ['Updating', 'Verifying', 'Uploading', 'Writing'])
                and (c_state[0] in ['Complete', 'Error', 'Unknown', 'Idle']))
                or (p_state[0] == 'Idle' and (c_state[0] in
                                              ['Complete', 'Error']))):
            return True
        return False

    wait_for_operation_to_complete(
        has_firmware_flash_completed,
        delay_bw_retries=30,
        failover_msg='iLO firmware update has failed.'
    )
    wait_for_ilo_after_reset(redfish_object)
