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

import os
import re
import stat
import time

from proliantutils import exception
from proliantutils import log


LOG = log.get_logger(__name__)

ILO_VER_STR_PATTERN = r"\d+\.\d+"


def wait_for_operation_to_complete(
        has_operation_completed, retries=10, delay_bw_retries=5,
        delay_before_attempts=10, failover_exc=exception.IloError,
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


def wait_for_ris_firmware_update_to_complete(ris_object):
    """Continuously polls for iLO firmware update to complete."""

    p_state = ['IDLE']
    c_state = ['IDLE']

    def has_firmware_flash_completed():
        """Checks for completion status of firmware update operation

        The below table shows the conditions for which the firmware update
        will be considered as DONE (be it success or error)::

        +---------------------+--------------------+
        |    Previous state   |    Current state   |
        +=====================+====================+
        |    IDLE             |    ERROR           |
        +---------------------+--------------------+
        |    PROGRESSING      |    ERROR           |
        +---------------------+--------------------+
        |    PROGRESSING      |    COMPLETED       |
        +---------------------+--------------------+
        |    PROGRESSING      |    UNKNOWN         |
        +---------------------+--------------------+
        |    PROGRESSING      |    IDLE            |
        +---------------------+--------------------+
        """
        curr_state, curr_percent = ris_object.get_firmware_update_progress()
        p_state[0] = c_state[0]
        c_state[0] = curr_state
        if (((p_state[0] == 'PROGRESSING') and (c_state[0] in
                                                ['COMPLETED', 'ERROR',
                                                 'UNKNOWN', 'IDLE']))
                or (p_state[0] == 'IDLE' and c_state[0] == 'ERROR')):
            return True
        return False

    wait_for_operation_to_complete(
        has_firmware_flash_completed,
        delay_bw_retries=30,
        failover_msg='iLO firmware update has failed.'
    )
    wait_for_ilo_after_reset(ris_object)


def wait_for_ribcl_firmware_update_to_complete(ribcl_object):
    """Continuously checks for iLO firmware update to complete."""

    def is_ilo_reset_initiated():
        """Checks for initiation of iLO reset

        Invokes the ``get_product_name`` api and returns
            i) True, if exception gets raised as that marks the iLO reset
               initiation.
            ii) False, if the call gets through without any failure, marking
                that iLO is yet to be reset.
        """
        try:
            LOG.debug(ribcl_object._('Checking for iLO reset...'))
            ribcl_object.get_product_name()
            return False
        except exception.IloError:
            LOG.debug(ribcl_object._('iLO is being reset...'))
            return True

    # Note(deray): wait for 5 secs, before checking if iLO reset got triggered
    # at every interval of 6 secs. This looping call happens for 10 times.
    # Once it comes out of the wait of iLO reset trigger, then it starts
    # waiting for iLO to be up again after reset.
    wait_for_operation_to_complete(
        is_ilo_reset_initiated,
        delay_bw_retries=6,
        delay_before_attempts=5,
        is_silent_loop_exit=True
    )
    wait_for_ilo_after_reset(ribcl_object)


def isDisk(result):
    """Checks if result has a disk related strings."""

    disk_identifier = ["Logical Drive", "HDD", "Storage", "LogVol"]
    return any(e in result for e in disk_identifier)


def get_filename_and_extension_of(target_file):
    """Gets the base filename and extension of the target file.

    :param target_file: the complete path of the target file
    :returns: base filename and extension
    """
    base_target_filename = os.path.basename(target_file)
    file_name, file_ext_with_dot = os.path.splitext(base_target_filename)
    return file_name, file_ext_with_dot


def add_exec_permission_to(target_file):
    """Add executable permissions to the file

    :param target_file: the target file whose permission to be changed
    """
    mode = os.stat(target_file).st_mode
    os.chmod(target_file, mode | stat.S_IXUSR)


def get_major_minor(ilo_ver_str):
    """Extract the major and minor number from the passed string

    :param ilo_ver_str: the string that contains the version information
    :returns: String of the form "<major>.<minor>" or None
    """
    if not ilo_ver_str:
        return None
    try:
        # Note(vmud213):This logic works for all strings
        # that contain the version info as <major>.<minor>
        # Formats of the strings:
        #    Release version ->  "2.50 Feb 18  2016"
        #    Debug version   ->  "iLO 4 v2.50"
        #    random version  ->  "XYZ ABC 2.30"
        pattern = re.search(ILO_VER_STR_PATTERN, ilo_ver_str)
        if pattern:
            matched = pattern.group(0)
            if matched:
                return matched
            return None
    except Exception:
        return None
