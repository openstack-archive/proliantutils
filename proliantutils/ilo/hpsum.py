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


def _execute_hpsum(hpsum_file_path, components):
    """Executes the hpsum firmware update command.

    This method executes the hpsum firmware update command with the list
    of firmware components,if any, to be updated. If components to be updated
    are not given, it performs firmware update on all the components.

    :param hpsum_file_path: A string with the path to the hpsum binary to be
        executed
    :param components: A list of components to be updated, if any.
    :returns: A tuple containing stdout and stderr after running the process.
    :raises: HpsumOperationError, when the hpsum firmware update operation on
        the node fails.
    """
    cmd = ""
    if components:
        for item in components:
            cmd = cmd + " --c " + str(item)
    try:
        stdout, stderr = processutils.execute(hpsum_file_path, "-s", cmd)
    except processutils.ProcessExecutionError as e:
        msg = ("Unable to perform hpsum firmware update on the node. %s" % e)
        raise exception.HpsumOperationError(msg)
    return stdout, stderr


def _get_ilo_object(node):
    """Create and return a ilo object."""
    info = node.get('driver_info')
    ilo_address = info.get('ilo_address')
    ilo_username = info.get('ilo_username')
    ilo_password = info.get('ilo_password')

    return client.IloClient(ilo_address, ilo_username, ilo_password)


def _get_args(node, key):
    """Parse and return string value from node dictionary.

    :param node: a dictionary of the node object.
    :param key: A string, key to search for the value in the dictionary
        node.
    :returns: A string value.
    """
    clean_steps = node['driver_internal_info']['clean_steps']
    for step in clean_steps:
        if step['step'] == 'hpsum_firmware_update':
            if key in step['args']:
                return step['args'][key]


def _list_to_dict(list):
    """Converts a list to dictionary."""
    return {list[0]: list[1]}


def _parse_hpsum_ouput():
    """Parse the hpsum output log file.

    This method parse through the hpsum log file in the
    default location to return the hpsum update status

    :returns: A dictionary of components updated with the version
        and firmware update status
    :raises: HpsumOperationError, when the hpsum log file does not
        exists.
    """
    output_file = '/var/hp/log/localhost/hpsum_log.txt'
    if os.path.exists(output_file):
        output_data = open('/var/hp/log/localhost/hpsum_log.txt').read()
        ret_data = output_data.split('Deployed Components:', 1)[1]
        ret_data = ret_data.split('Exit status', 1)[0]

        temp_result = {}
        result = {}

        for line in re.split('\n', ret_data):
            if line:
                line = line.replace(" ", "")
                temp = _list_to_dict(line.split(':'))
                if temp.keys()[0] in temp_result.keys():
                    key = temp_result['ComponentName']
                    temp_result.pop('ComponentName')
                    result[key] = temp_result
                    temp_result = {}

                temp_result.update(temp)
        return result
    else:
        msg = ("Unable to find the hpsum output file in the location %s"
               % output_file)
        raise exception.HpsumOperationError(msg)


def hpsum_firmware_update(node):
    """Performs hpsum firmware update on the node.

    This method performs hpsum firmware update by mounting the
    SPP ISO on the node. It can perform firmware update on all
    the firmware components or the list of firmware components.

    :param node: A dictionary of the node object.
    :returns: A dictionary of components updates, with their version
        and update status.
    :raises: HpsumOperationError, when the vmedia device is not found or
        when the mount operation fails.
    :raises: IloError, when the eject vmedia or insert vmedia operations
        fails.
    """
    hpsum_update_iso = _get_args(node, 'firmware_update_iso')
    device = 'CDROM'

    ilo_object = _get_ilo_object(node)
    try:
        ilo_object.eject_virtual_media(device)
        ilo_object.insert_virtual_media(hpsum_update_iso, device)
    except exception.IloError:
        msg = ("Unable to attach hpsum SPP iso %s to the iLO"
               % hpsum_update_iso)
        raise exception.IloError(msg)

    vmedia_device_file = ""
    vmedia_device_dir = "/dev/disk/by-label/"
    for file in os.listdir(vmedia_device_dir):
        if fnmatch.fnmatch(file, 'SPP*'):
            vmedia_device_file = os.path.join(vmedia_device_dir, file)

    if not os.path.exists(vmedia_device_file):
        msg = "Unable to find the virtual media device for HPSUM"
        raise exception.HpsumOperationError(msg)

    vmedia_mount_point = tempfile.mkdtemp()
    try:
        try:
            stdout, stderr = processutils.execute("mount", vmedia_device_file,
                                                  vmedia_mount_point)
        except processutils.ProcessExecutionError as e:
            msg = ("Unable to mount virtual media device %(device)s: "
                   "%(error)s" % {'device': vmedia_device_file, 'error': e})
            raise exception.HpsumOperationError(msg)

        hpsum_file_path = os.path.join(vmedia_mount_point,
                                       'hp/swpackages/hpsum')

        update_components = _get_args(node, 'update_components')
        _execute_hpsum(hpsum_file_path, update_components)

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

    return _parse_hpsum_ouput()
