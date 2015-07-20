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
import subprocess
import tempfile
import time
import types

from oslo_concurrency import processutils as utils
import six

from proliantutils import exception

# Max number of times an operation to be retried
RETRY_COUNT = 10
# Supported raw firmware file extensions
RAW_FIRMWARE_EXTNS = ['.hex', '.bin', '.vme']


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


def isDisk(result):
    """Checks if result has a disk related strings."""

    disk_identifier = ["Logical Drive", "HDD", "Storage", "LogVol"]
    return any(e in result for e in disk_identifier)


def get_filename_or_extension_of(target_file, ext=False):
    """Gets the filename or extension of the target file.

    Returns the filename if the ext boolean parameter is False,
    or extension of the target file, otherwise
    :param target_file: the complete path of the target file
    :param ext: deciding factor for return value
    :return: returns filename if False, extension otherwise
    """
    base_target_filename = os.path.basename(target_file)
    file_n, file_ext_with_dot = os.path.splitext(base_target_filename)
    if ext is True:
        # returns extension with the period.
        return file_ext_with_dot
    else:
        return file_n


def add_exec_permission_to(target_file):
        # Add executable permissions to the file
        mode = os.stat(target_file).st_mode
        os.chmod(target_file, mode | stat.S_IXUSR)


class MetaSingleton(type):
    """Singleton class maker

    This class is to be used to make any given class
    a singleton class. Use it sparingly, especially weighing
    the need for making a class Singleton::

      @six.add_metaclass(MetaSingleton)
      class ClasssToBeMadeSingleton(object):
          pass

    and that's it. Your class starts functioning as Singleton classes.
    """
    _instances = {}

    def __call__(cls_, *args, **kwargs):
        if cls_ not in cls_._instances:
            cls_._instances[cls_] = super(MetaSingleton, cls_).__call__(
                *args, **kwargs)
        return cls_._instances[cls_]


@six.add_metaclass(MetaSingleton)
class FirmwareImageProcessor(object):

    @classmethod
    def get_processor(cls, compact_fw_file):
        """Gets the singleton processor object fine-tuned for specified type

        :param cls: ref to FirmwareImageProcessor class
        :param compact_fw_file: specified file
        :raise IloInvalidInputError: for unsupported file types
        :return: FirmwareImageProcessor singleton object
        """
        fw_img_processor = FirmwareImageProcessor()
        fw_img_processor.compact_fw_file = compact_fw_file
        extension = get_filename_or_extension_of(compact_fw_file, ext=True)
        extension = extension.lower()

        if extension == '.scexe':
            fw_img_processor.__do_extract = types.MethodType(
                _extract_scexe_file, fw_img_processor)
        elif extension == '.rpm':
            fw_img_processor.__do_extract = types.MethodType(
                _extract_rpm_file, fw_img_processor)
        elif extension in RAW_FIRMWARE_EXTNS:
            fw_img_processor.actual_extract = fw_img_processor.extract

            def dummy_extract(self):
                # sanitize the ``extract`` method
                fw_img_processor.extract = fw_img_processor.actual_extract
                return fw_img_processor.compact_fw_file

            fw_img_processor.extract = types.MethodType(
                dummy_extract, fw_img_processor)
        else:
            raise exception.IloInvalidInputError(
                'Unexpected compact firmware file type: {}'.format(
                    compact_fw_file)
            )

        return fw_img_processor

    def extract(self):
        """Extracts the raw firmware file from its compact format

        :raise RawFirmwareFileNotFoundError: if raw firmware file not found
        :raise IloError: for other internal problems
        :return: the raw firmware file with the complete path
        """
        target_file = self.compact_fw_file
        add_exec_permission_to(target_file)

        filename = get_filename_or_extension_of(target_file)
        extract_path = os.path.join(tempfile.mkdtemp(), filename)

        self.__do_extract(target_file, extract_path)

        firmware_file = _get_firmware_file(extract_path)
        if firmware_file:
            return firmware_file
        raise exception.RawFirmwareFileNotFoundError(
            compact_file=target_file)


def _extract_scexe_file(self, target_file, extract_path):
    """Extracts the scexe file.

    :param target_file: the firmware file to be extracted
    :param extract_path: the path where extraction is supposed to happen
    """
    # Command to extract the smart component file.
    unpack_cmd = '--unpack=' + extract_path
    # os.path.isfile(target_file)
    cmd = [target_file, unpack_cmd]
    out, err = utils.trycmd(*cmd)


def _extract_rpm_file(self, target_file, extract_path):
    """Extracts the rpm file.

    :param target_file: the firmware file to be extracted
    :param extract_path: the path where extraction is supposed to happen
    :raise IloError: if any problem in running extraction command
    """
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    os.chdir(extract_path)

    try:
        rpm2cpio = subprocess.Popen('rpm2cpio ' + target_file,
                                    shell=True,
                                    stdout=subprocess.PIPE)
        cpio = subprocess.Popen('cpio -idm', shell=True,
                                stdin=rpm2cpio.stdout)
        out, err = cpio.communicate()
    # except (subprocess.SubprocessError, Exception):
    except Exception:
        raise exception.IloError('Unexpected error in extracting file: {}'
                                 .format(target_file))


def _get_firmware_file(path):
    """Gets the raw firmware file

    Gets the raw firmware file from the extracted directory structure
    :param path: the directory structure to search for
    :return: the raw firmware file with the complete path
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_n, file_ext = os.path.splitext(os.path.basename(filename))
            if file_ext in RAW_FIRMWARE_EXTNS:
                # return filename
                return os.path.join(dirpath, filename)
