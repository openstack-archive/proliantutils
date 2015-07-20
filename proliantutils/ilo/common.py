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
import stat
import time

from proliantutils import exception


def wait_for_operation_to_complete(has_operation_completed,
                                   retries=10,
                                   delay_bw_retries=5,
                                   failover_exc=exception.IloError,
                                   failover_msg=(
        "Operation did not complete even after multiple attempts.")):
    """Attempts the provided operation for a specified number of times.

    If it runs out of attempts, then it raises an exception. On success,
    it breaks out of the loop.
    :param has_operation_completed: the method to retry and it needs to return
                                    a boolean to indicate success or failure.
    :param retries: number of times the operation to be (re)tried, default 10
    :param delay_bw_retries: delay in seconds before attempting after
                             each failure, default 5.
    :param failover_exc: the exception which gets raised in case of failure
                         upon exhausting all the attempts, default IloError.
    :param failover_msg: the msg with which the exception gets raised in case
                         of failure upon exhausting all the attempts.
    :raises: IloError, if failure happens even after all the attempts.
    """
    retry_count = retries
    # Delay for 10 secs, before beginning any attempt
    time.sleep(10)

    while retry_count:
        try:
            if has_operation_completed():
                break
        except exception.IloError:
            pass
        time.sleep(delay_bw_retries)
        retry_count -= 1
    else:
        raise failover_exc(failover_msg)


def wait_for_ilo_after_reset(ilo_object):
    """Continuously polls for iLO to come up after reset."""

    wait_for_operation_to_complete(
        lambda: ilo_object.get_product_name() is not None,
        failover_exc=exception.IloConnectionError,
        failover_msg='iLO is not up after reset.'
    )


def wait_for_firmware_update_to_complete(ris_object):
    """Continuously polls for iLO firmware update to complete."""

    p_state = ['IDLE']
    c_state = ['IDLE']

    def inprogress_operation_completed():
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
        inprogress_operation_completed,
        delay_bw_retries=30,
        failover_msg='iLO firmware update has failed.'
    )


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
