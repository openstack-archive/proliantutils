# Copyright 2017 Hewlett Packard Enterprise Company, L.P.
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


import fnmatch
import io
import os
import re
import shutil
import tarfile
import tempfile
import time

from oslo_concurrency import processutils
from oslo_serialization import base64

from proliantutils import exception
from proliantutils.ilo import client
from proliantutils import utils


HPSUM_LOCATION = 'hp/swpackages'

WAIT_TIME_DISK_LABEL_TO_BE_VISIBLE = 5

# List of log files created by SUM based firmware update.
OUTPUT_FILES = ['/var/hp/log/localhost/hpsum_log.txt',
                '/var/hp/log/localhost/hpsum_detail_log.txt',
                '/var/log/sum/localhost/sum_log.txt',
                '/var/log/sum/localhost/sum_detail_log.txt']

EXIT_CODE_TO_STRING = {
    0: "The smart component was installed successfully.",
    1: ("The smart component was installed successfully, but the system "
        "must be restarted."),
    3: ("The smart component was not installed. Node is already "
        "up-to-date."),
    253: "The installation of the component failed."
    }


def _execute_sum(sum_file_path, components=None):
    """Executes the SUM based firmware update command.

    This method executes the SUM based firmware update command to update the
    components specified, if not, it performs update on all the firmware
    components on th server.

    :param sum_file_path: A string with the path to the SUM binary to be
        executed
    :param components: A list of components to be updated. If it is None, all
        the firmware components are updated.
    :returns: A string with the statistics of the updated/failed components.
    :raises: SUMOperationError, when the SUM based firmware update operation
        on the node fails.
    """
    cmd = ' --c ' + ' --c '.join(components) if components else ''

    try:
        processutils.execute('./hpsum', '--s', '--romonly', cmd,
                             cwd=sum_file_path)
    except processutils.ProcessExecutionError as e:
        result = _parse_sum_ouput(e.exit_code)
        if result:
            return result
        else:
            raise exception.SUMOperationError(reason=str(e))


def _get_log_file_data_as_encoded_content():
    """Gzip and base64 encode files and BytesIO buffers.

    This method gets the log files created by SUM based
    firmware update and tar zip the files.
    :returns: A gzipped and base64 encoded string as text.
    """
    with io.BytesIO() as fp:
        with tarfile.open(fileobj=fp, mode='w:gz') as tar:
            for f in OUTPUT_FILES:
                if os.path.isfile(f):
                    tar.add(f)

        fp.seek(0)
        return base64.encode_as_bytes(fp.getvalue())


def _parse_sum_ouput(exit_code):
    """Parse the SUM output log file.

    This method parses through the SUM log file in the
    default location to return the SUM update status. Sample return
    string:

    "Summary: The installation of the component failed. Status of updated
     components: Total: 5 Success: 4 Failed: 1"

    :param exit_code: A integer returned by the SUM after command execution.
    :returns: A string with the statistics of the updated/failed
        components and 'None' when the exit_code is not 0, 1, 3 or 253.
    """
    if exit_code == 3:
        return "Summary: %s" % EXIT_CODE_TO_STRING.get(exit_code)

    if exit_code in (0, 1, 253):
        if os.path.exists(OUTPUT_FILES[0]):
            with open(OUTPUT_FILES[0], 'r') as f:
                output_data = f.read()

            ret_data = output_data[(output_data.find('Deployed Components:') +
                                    len('Deployed Components:')):
                                   output_data.find('Exit status:')]

            failed = 0
            success = 0
            for line in re.split('\n\n', ret_data):
                if line:
                    if 'Success' not in line:
                        failed += 1
                    else:
                        success += 1

            return {
                'Summary': (
                    "%(return_string)s Status of updated components: Total: "
                    "%(total)s Success: %(success)s Failed: %(failed)s." %
                    {'return_string': EXIT_CODE_TO_STRING.get(exit_code),
                     'total': (success + failed), 'success': success,
                     'failed': failed}),
                'Log Data': _get_log_file_data_as_encoded_content()
            }

        return "UPDATE STATUS: UNKNOWN"


def update_firmware(node):
    """Performs SUM based firmware update on the node.

    This method performs SUM firmware update by mounting the
    SPP ISO on the node. It performs firmware update on all or
    some of the firmware components.

    :param node: A node object of type dict.
    :returns: Operation Status string.
    :raises: SUMOperationError, when the vmedia device is not found or
        when the mount operation fails or when the image validation fails.
    :raises: IloConnectionError, when the iLO connection fails.
    :raises: IloError, when vmedia eject or insert operation fails.
    """
    sum_update_iso = node['clean_step']['args'].get('url')

    # Validates the http image reference for SUM update ISO.
    try:
        utils.validate_href(sum_update_iso)
    except exception.ImageRefValidationFailed as e:
        raise exception.SUMOperationError(reason=e)

    # Ejects the CDROM device in the iLO and inserts the SUM update ISO
    # to the CDROM device.
    info = node.get('driver_info')
    ilo_object = client.IloClient(info.get('ilo_address'),
                                  info.get('ilo_username'),
                                  info.get('ilo_password'))

    ilo_object.eject_virtual_media('CDROM')
    ilo_object.insert_virtual_media(sum_update_iso, 'CDROM')

    # Waits for the OS to detect the disk and update the label file. SPP ISO
    # is identified by matching its label.
    time.sleep(WAIT_TIME_DISK_LABEL_TO_BE_VISIBLE)
    vmedia_device_dir = "/dev/disk/by-label/"
    for file in os.listdir(vmedia_device_dir):
        if fnmatch.fnmatch(file, 'SPP*'):
            vmedia_device_file = os.path.join(vmedia_device_dir, file)

    if not os.path.exists(vmedia_device_file):
        msg = "Unable to find the virtual media device for SUM"
        raise exception.SUMOperationError(reason=msg)

    # Validates the SPP ISO image for any file corruption using the checksum
    # of the ISO file.
    expected_checksum = node['clean_step']['args'].get('checksum')
    try:
        utils.verify_image_checksum(vmedia_device_file, expected_checksum)
    except exception.ImageRefValidationFailed as e:
        raise exception.SUMOperationError(reason=e)

    # Mounts SPP ISO on a temporary directory.
    vmedia_mount_point = tempfile.mkdtemp()
    try:
        try:
            processutils.execute("mount", vmedia_device_file,
                                 vmedia_mount_point)
        except processutils.ProcessExecutionError as e:
            msg = ("Unable to mount virtual media device %(device)s: "
                   "%(error)s" % {'device': vmedia_device_file, 'error': e})
            raise exception.SUMOperationError(reason=msg)

        # Executes the SUM based firmware update by passing the default hpsum
        # executable path and the components specified, if any.
        sum_file_path = os.path.join(vmedia_mount_point, HPSUM_LOCATION)
        components = node['clean_step']['args'].get('components')

        result = _execute_sum(sum_file_path, components=components)

        processutils.trycmd("umount", vmedia_mount_point)
    finally:
        shutil.rmtree(vmedia_mount_point, ignore_errors=True)

    return result
