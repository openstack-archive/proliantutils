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
import os
import stat
import tempfile
from oslo_concurrency import processutils as utils
import subprocess
import types

from proliantutils import exception

# Max number of times an operation to be retried
RETRY_COUNT = 10
# Supported core firmware file extensions
SUPPORTED_FIRMWARE_EXTNS = ['hex', 'bin', 'vme']


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


class MetaSingleton(type):
    _instances = {}

    def __call__(cls_, *args, **kwargs):
        if cls_ not in cls_._instances:
            cls_._instances[cls_] = super(MetaSingleton, cls_).__call__(*args, **kwargs)
        return cls_._instances[cls_]


def get_fw_extension(fw_file):
    """
    Returns the extension of the firmware file.
    :param fw_file: the complete path of the firmware file
    :return: extension of the firmware file
    """
    file_n, file_ext_with_dot = os.path.splitext(fw_file)
    return file_ext_with_dot[1:]

class FirmwareProcessor(object):

    __metaclass__ = MetaSingleton

#     def __init__(self, compact_fw_file):
#         self._compact_fw_file = compact_fw_file

    @property
    def compact_fw_file(self):
        return self._compact_fw_file

    @compact_fw_file.setter
    def compact_fw_file(self, value):
        self._compact_fw_file = value

    @classmethod
    def get_fw_processor(cls, compact_fw_file):
        fw_processor = FirmwareProcessor()
        fw_processor.compact_fw_file = compact_fw_file
        extension = get_fw_extension(compact_fw_file)
        if extension:
            extension = extension.lower()

        if extension == 'scexe':
            fw_processor.__do_extract = types.MethodType(
                                    _extract_scexe_file, fw_processor)
        elif extension == 'rpm':
            fw_processor.__do_extract = types.MethodType(
                                    _extract_rpm_file, fw_processor)
        elif extension in SUPPORTED_FIRMWARE_EXTNS:
            fw_processor.extract = lambda self: fw_processor.compact_fw_file
        else:
            raise RuntimeError('Unexpected compact firmware file type: {}'.format(compact_fw_file))

        return fw_processor

    def extract(self):
        target_file = self.compact_fw_file
        # Add executable permissions to the file
        mode = os.stat(target_file).st_mode
        os.chmod(target_file, mode | stat.S_IXUSR)

        base_target_filename = os.path.basename(target_file)
        filename, ext = os.path.splitext(base_target_filename)
        extract_path = os.path.join(tempfile.mkdtemp(), filename)

        self.__do_extract(target_file, extract_path)

        firmware_file = _get_firmware_file(extract_path)
        return firmware_file


def _extract_scexe_file(self, target_file, extract_path):
    """
    Extract the scexe file.
    :param target_file: the firmware file to be extracted
    :param extract_path: the path where extraction is supposed to happen
    """
    # Command to extract the smart component file.
    unpack_cmd = '--unpack=' + extract_path
    # print os.path.isfile(target_file)
    cmd = [target_file, unpack_cmd]
    out, err = utils.trycmd(*cmd)


def _extract_rpm_file(self, target_file, extract_path):
    """
    Extract the rpm file.
    :param target_file: the firmware file to be extracted
    :param extract_path: the path where extraction is supposed to happen
    """
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    os.chdir(extract_path)

    rpm2cpio = subprocess.Popen('rpm2cpio ' + target_file, shell=True, stdout=subprocess.PIPE)
    cpio = subprocess.Popen('cpio -idm', shell=True, stdin=rpm2cpio.stdout)

    out, err = cpio.communicate()


def _get_firmware_file(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_n, file_ext = os.path.splitext(os.path.basename(filename))
            ext = file_ext[1:]
            if ext in SUPPORTED_FIRMWARE_EXTNS:
                #return filename
                return os.path.join(dirpath, filename)
