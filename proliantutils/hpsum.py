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
import os
import re
import shutil
import tempfile

from oslo_concurrency import processutils

from proliantutils import exception
from proliantutils.ilo import client
from proliantutils import utils


OUTPUT_FILE = '/var/hp/log/localhost/hpsum_log.txt'

HPSUM_LOCATION = 'hp/swpackages/hpsum'


def _return_code_mapping(exit_code):
    return_code = {
        0: "The smart component was installed successfully.",
        1: ("The smart component was installed successfully, but the system "
            "must be restarted."),
        2: ("The installation was not attempted because the required hardware "
            "is not present, the software is current, or there is nothing to "
            "install."),
        3: ("The smart component was not installed. Node is already "
            "up-to-date."),
        5: ("A user canceled the installation before anything could be "
            "installed."),
        6: ("The installer cannot run because of an unmet dependency or "
            "installation tool failure."),
        7: ("The actual installation operation (not the installation tool) "
            "failed.")}

    return return_code.get(exit_code, None)


def _execute_hpsum(hpsum_file_path):
    """Executes the hpsum firmware update command.

    This method executes the hpsum firmware update command to update all the
    firmware components in the server.

    :param hpsum_file_path: A string with the path to the hpsum binary to be
        executed
    :returns: A String with hpsum based firmware update return status.
    :raises: HpsumOperationError, when the hpsum firmware update operation on
        the node fails.
    """
    try:
        processutils.execute(hpsum_file_path, "--s",
                                              "--romonly")
    except processutils.ProcessExecutionError as e:
        if e.exit_code >= 0:
            msg = _return_code_mapping(e.exit_code)
        else:
            msg = "Unable to perform hpsum firmware update on the node."
            output_file = OUTPUT_FILE
            if os.path.exists(output_file):
                result = _parse_hpsum_ouput()
                msg = msg + str(result)
            else:
                msg = msg + str(e)

            raise exception.HpsumOperationError(msg)
    return msg


def _parse_hpsum_ouput():
    """Parse the hpsum output log file.

    This method parse through the hpsum log file in the
    default location to return the hpsum update status

    :returns: A list of components updated with the version
        and firmware update status
    :raises: HpsumOperationError, when the hpsum log file does not
        exists and also when the parsing of hpsum output file fails.
    """
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            output_data = f.read()

        ret_data = output_data[output_data.find('Deployed Components:') + 21:
                               output_data.find('Exit status:')]

        result = []
        for line in re.split('\n\n', ret_data):
            if line:
                tmp_result = [x.strip() for x in line.split('\n')]
                result.append(tmp_result)

        return result
    else:
        msg = ("Unable to find the hpsum output file in the location %s"
               % OUTPUT_FILE)
        raise exception.HpsumOperationError(msg)


def _get_clean_arg_value(node, key):
    """Return the clean step argument from node dictionary.

    :param node: a dictionary of the node object.
    :param key: A string, key to search for the value in the dictionary
        node.
    :returns: A string value.
    """
    return node['clean_step']['args']['firmware_images'][0][key]


def hpsum_firmware_update(node):
    """Performs hpsum firmware update on the node.

    This method performs hpsum firmware update by mounting the
    SPP ISO on the node. It performs firmware update on all
    the firmware components.

    :param node: A dictionary of the node object.
    :returns: A list of components updates, with their version
        and update status.
    :raises: HpsumOperationError, when the vmedia device is not found or
        when the mount operation fails.
    """
    hpsum_update_iso = _get_clean_arg_value(node, 'url')
    try:
        utils.validate_href(hpsum_update_iso)
    except exception.ImageRefValidationFailed as e:
        raise exception.HpsumOperationError(e)

    info = node.get('driver_info')

    ilo_object = client.IloClient(info.get('ilo_address'),
                                  info.get('ilo_username'),
                                  info.get('ilo_password'))

    ilo_object.eject_virtual_media('CDROM')
    ilo_object.insert_virtual_media(hpsum_update_iso, 'CDROM')

    vmedia_device_dir = "/dev/disk/by-label/"
    for file in os.listdir(vmedia_device_dir):
        if fnmatch.fnmatch(file, 'SPP*'):
            vmedia_device_file = os.path.join(vmedia_device_dir, file)

    if not os.path.exists(vmedia_device_file):
        msg = "Unable to find the virtual media device for HPSUM"
        raise exception.HpsumOperationError(msg)

    expected_checksum = _get_clean_arg_value(node, 'checksum')

    try:
        utils.verify_image_checksum(vmedia_device_file, expected_checksum)
    except exception.ImageRefValidationFailed as e:
        raise exception.HpsumOperationError(e)

    vmedia_mount_point = tempfile.mkdtemp()
    try:
        try:
            stdout, stderr = processutils.execute("mount", vmedia_device_file,
                                                  vmedia_mount_point)
        except processutils.ProcessExecutionError as e:
            msg = ("Unable to mount virtual media device %(device)s: "
                   "%(error)s" % {'device': vmedia_device_file, 'error': e})
            raise exception.HpsumOperationError(msg)

        hpsum_file_path = os.path.join(vmedia_mount_point, HPSUM_LOCATION)

        stdout = _execute_hpsum(hpsum_file_path)
        result = {"RETURN STATUS": stdout}

        try:
            stdout, stderr = processutils.execute("umount",
                                                  vmedia_mount_point)
        except processutils.ProcessExecutionError as e:
            pass
    finally:
        try:
            shutil.rmtree(vmedia_mount_point)
        except Exception as e:
            pass

    result.update({"DETAILS": _parse_hpsum_ouput()})
    return result
