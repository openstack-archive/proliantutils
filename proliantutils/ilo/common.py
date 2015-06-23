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

import os.path
import re
import stat
import time

from oslo.concurrency import processutils as utils

from proliantutils import exception

# Max number of times an operation to be retried
RETRY_COUNT = 10
TEMP_DIR = '/tmp'
CHUNK_SIZE = 1024*1024
SUPPORTED_FW_EXTNS = ['hex', 'bin', 'vme']


def wait_for_ilo_after_reset(ilo_object):
    """Checks if iLO is up after reset."""

    retry_count = RETRY_COUNT
    # Delay for 10 sec, for the reset operation to take effect.
    time.sleep(10)

    while retry_count:
        try:
            ilo_object.get_product_name()
            break
        except exception.IloError:
            retry_count -= 1
            time.sleep(5)
    else:
        msg = ('iLO is not up after reset.')
        raise exception.IloConnectionError(msg)


def _parse_firmware_url(url):
    """Checks if its a valid url and extracts it."""
    filename = os.path.basename(url)
    name, ext = os.path.splitext(filename)
    if not any(e in ext for e in ('scexe', 'rpm')):
        raise exception.InvalidInputError("Not a valid file")
    # TODO(ramineni):Need to also categorize .bin, .hex or .Bxx
    # as valid files
    return name, ext


def extract(location):
    """Extract the file based on extension.

    :param location: path of the file to be extracted
    :returns: extracted location of the file
    """
    # Add executable permissions to the file
    mode = os.stat(location).st_mode
    os.chmod(location, mode | stat.S_IXUSR)

    name, ext = _parse_firmware_url(location)
    path_extract = os.path.join(TEMP_DIR, name)

    if 'scexe' in ext:
        return _extract_scexe(location, path_extract)
    elif 'rpm' in ext:
        # Create a temp dir to extract rpm
        if not os.path.exists(path_extract):
            os.makedirs(path_extract)
        return _extract_rpm(location, path_extract)
    else:
        # It should be a direct .bin or .hex or .Bxx file
        return location


def _extract_scexe(target_file, extract_path):
    """Extract the scexe file."""
    # Command to extract the smart component file.
    unpack_cmd = '--unpack=' + extract_path
    args = [target_file, unpack_cmd]
    try:
        out, err = utils.execute(*args)
    except Exception as err_msg:
        raise exception.IloError(err_msg)

    filename = _validate_and_get_firmware_file(extract_path)
    return filename


def _validate_and_get_firmware_file(path):
    """Parses the extract directory and get the firmware file."""
    for root, dirnames, filenames in os.walk(path):
        for name in filenames:
            ext = os.path.splitext(os.path.basename(name))[1][1::]
            if ext:
                for e in SUPPORTED_FW_EXTNS:
                    if re.match(e, ext):
                        return name


def _extract_rpm(target_file, extract_path=None):
    """Using rpm2cpio command to extract rpm file."""
    os.chdir(extract_path)
    cmd = ['rpm2cpio', target_file, '|', 'cpio', '-idm']
    try:
        out, err = utils.execute(*cmd)
    except Exception as err_msg:
        raise exception.IloError(err_msg)

    filename = _validate_and_get_firmware_file(extract_path)
    return filename
