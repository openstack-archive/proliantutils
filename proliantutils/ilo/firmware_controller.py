# Copyright 2016 Hewlett Packard Enterprise Company, L.P.
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

"""
Firmware related utilities and helper functions.
"""

import abc
import os
import random
import re
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import types
import uuid

from oslo_concurrency import processutils as utils
import six

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils import log

if six.PY3:
    def b(x):
        return bytes(x, 'ascii')

else:
    def b(x):
        return x

LOG = log.get_logger(__name__)

# Supported components for firmware update
SUPPORTED_FIRMWARE_UPDATE_COMPONENTS = ['ilo', 'cpld', 'power_pic', 'bios',
                                        'chassis']
# Supported raw firmware file extensions
RAW_FIRMWARE_EXTNS = ['.hex', '.bin', '.vme', '.flash']


def check_firmware_update_component(func):
    """Checks the firmware update component."""
    @six.wraps(func)
    def wrapper(self, filename, component_type):
        """Wrapper around ``update_firmware`` call.

        :param filename: location of the raw firmware file.
        :param component_type: Type of component to be applied to.
        """
        component_type = component_type and component_type.lower()
        if (component_type not in SUPPORTED_FIRMWARE_UPDATE_COMPONENTS):
            msg = ("Got invalid component type for firmware update: "
                   "``update_firmware`` is not supported on %(component)s" %
                   {'component': component_type})
            LOG.error(self._(msg))  # noqa
            raise exception.InvalidInputError(msg)

        return func(self, filename, component_type)

    return wrapper


@six.add_metaclass(abc.ABCMeta)
class FirmwareImageControllerBase(object):
    """Base class for firmware file related operations."""

    def __init__(self, fw_file):
        self.fw_file = fw_file
        file_name, file_ext_with_dot = common.get_filename_and_extension_of(
            fw_file)
        self.fw_filename = file_name
        self.fw_file_ext = file_ext_with_dot


class FirmwareImageUploader(FirmwareImageControllerBase):
    """Helper class to upload the firmware image file

    This class acts as a helper class in uploading the firmware file to iLO.
    """

    HTTP_UPLOAD_HEADER = ("POST /cgi-bin/uploadRibclFiles HTTP/1.1\r\n"
                          "Host: localhost\r\nConnection: Close\r\n"
                          "Content-Length: %d\r\n"
                          "Content-Type: multipart/form-data; "
                          "boundary=%s\r\n\r\n")

    def upload_file_to(self, addressinfo, timeout):
        """Uploads the raw firmware file to iLO

        Uploads the raw firmware file (already set as attribute in
        FirmwareImageControllerBase constructor) to iLO, whose address
        information is passed to this method.
        :param addressinfo: tuple of hostname and port of the iLO
        :param timeout: timeout in secs, used for connecting to iLO
        :raises: IloInvalidInputError, if raw firmware file not found
        :raises: IloError, for other internal problems
        :returns: the cookie so sent back from iLO on successful upload
        """
        self.hostname, self.port = addressinfo
        self.timeout = timeout
        filename = self.fw_file

        firmware = open(filename, 'rb').read()
        # generate boundary
        boundary = b('------hpiLO3t' +
                     str(random.randint(100000, 1000000)) + 'z')

        while boundary in firmware:
            boundary = b('------hpiLO3t' +
                         str(random.randint(100000, 1000000)) + 'z')
        # generate body parts
        parts = [
            # body1
            b("--") + boundary +
            b("""\r\nContent-Disposition: form-data; """
              """name="fileType"\r\n\r\n"""),
            # body2
            b("\r\n--") + boundary +
            b('''\r\nContent-Disposition: form-data; name="fwimgfile"; '''
              '''filename="''') +
            b(filename) +
            b('''"\r\nContent-Type: application/octet-stream\r\n\r\n'''),
            # firmware image
            firmware,
            # body3
            b("\r\n--") + boundary + b("--\r\n"),
        ]
        total_bytes = sum([len(x) for x in parts])
        sock = self._get_socket()

        # send the firmware image
        sock.write(b(self.HTTP_UPLOAD_HEADER %
                     (total_bytes, boundary.decode('ascii'))))
        for part in parts:
            sock.write(part)

        data = ''
        try:
            while True:
                d = sock.read()
                data += d.decode('latin-1')
                if not d:
                    break
        except socket.sslerror:  # Connection closed
            e = sys.exc_info()[1]
            if not data:
                raise exception.IloConnectionError(
                    "Communication with %(hostname)s:%(port)d failed: "
                    "%(error)s" % {'hostname': self.hostname,
                                   'port': self.port, 'error': str(e)})

        # Received len(data) bytes
        cookie_match = re.search('Set-Cookie: *(.*)', data)
        if not cookie_match:
            raise exception.IloError("Uploading of file: %s failed due "
                                     "to unknown reason." % filename)
        # return the cookie
        return cookie_match.group(1)

    def _get_socket(self, sslversion=ssl.PROTOCOL_TLSv1):
        """Sets up an https connection and do an HTTP/raw socket request

        :param sslversion: version of ssl session
        :raises: IloConnectionError, for connection failures
        :returns: ssl wrapped socket object
        """
        err = None
        sock = None
        try:
            for res in socket.getaddrinfo(
                    self.hostname, self.port, 0, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    sock = socket.socket(af, socktype, proto)
                    sock.settimeout(self.timeout)
                    # Connecting to {self.hostname} at port {self.port}
                    sock.connect(sa)
                except socket.timeout:
                    if sock is not None:
                        sock.close()
                    err = exception.IloConnectionError(
                        "Timeout connecting to %(hostname)s:%(port)d"
                        % {'hostname': self.hostname, 'port': self.port})
                except socket.error:
                    if sock is not None:
                        sock.close()
                    e = sys.exc_info()[1]
                    err = exception.IloConnectionError(
                        "Error connecting to %(hostname)s:%(port)d : %(error)s"
                        % {'hostname': self.hostname, 'port': self.port,
                           'error': str(e)})
        except Exception:
            raise exception.IloConnectionError(
                "Unable to resolve %s" % self.hostname)

        if err is not None:
            raise err

        # wrapping the socket over ssl session
        try:
            return ssl.wrap_socket(sock, ssl_version=sslversion)
        except socket.sslerror:
            e = sys.exc_info()[1]
            msg = (getattr(e, 'reason', None) or
                   getattr(e, 'message', None))
            # Some older iLO s don't support TLSv1, retry with SSLv3
            if ('wrong version number' in msg) and (
                    sslversion == ssl.PROTOCOL_TLSv1):

                return self._get_socket(ssl.PROTOCOL_SSLv3)

            raise exception.IloConnectionError(
                "Cannot establish ssl session with %(hostname)s:%(port)d : "
                "%(error)s" % {'hostname': self.hostname, 'port': self.port,
                               'error': str(e)})


class FirmwareImageExtractor(FirmwareImageControllerBase):
    """Helper class to extract the raw file from compact firmware image file

    This class acts as a helper class in extracting the raw firmware file
    from the compact firmware file.
    """

    def extract(self):
        """Extracts the raw firmware file from its compact format

        Extracts the raw firmware file from its compact file format (already
        set as attribute in FirmwareImageControllerBase constructor).
        :raises: InvalidInputError, if raw firmware file not found
        :raises: ImageExtractionFailed, for extraction related issues
        :returns: the raw firmware file with the complete path
        :returns: boolean(True) to indicate that a new file got generated
                  after successful extraction.
        """
        target_file = self.fw_file
        common.add_exec_permission_to(target_file)
        # create a temp directory where the extraction will occur
        temp_dir = tempfile.mkdtemp()
        extract_path = os.path.join(temp_dir, self.fw_filename)

        try:
            self._do_extract(target_file, extract_path)
        except exception.ImageExtractionFailed:
            # clean up the partial extracted content, if any,
            # along with temp dir and re-raise the exception
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise

        # creating a new hard link to the core firmware file
        firmware_file_path = _get_firmware_file_in_new_path(extract_path)
        # delete the entire extracted content along with temp dir.
        shutil.rmtree(temp_dir, ignore_errors=True)

        if not firmware_file_path:
            raise exception.InvalidInputError(
                "Raw firmware file not found in: '%s'" % target_file)

        return firmware_file_path, True


def get_fw_extractor(fw_file):
    """Gets the firmware extractor object fine-tuned for specified type

    :param fw_file: compact firmware file to be extracted from
    :raises: InvalidInputError, for unsupported file types
    :returns: FirmwareImageExtractor object
    """
    fw_img_extractor = FirmwareImageExtractor(fw_file)
    extension = fw_img_extractor.fw_file_ext.lower()

    if extension == '.scexe':
        # assign _do_extract attribute to refer to _extract_scexe_file
        fw_img_extractor._do_extract = types.MethodType(
            _extract_scexe_file, fw_img_extractor)
    elif extension == '.rpm':
        # assign _do_extract attribute to refer to _extract_rpm_file
        fw_img_extractor._do_extract = types.MethodType(
            _extract_rpm_file, fw_img_extractor)
    elif extension in RAW_FIRMWARE_EXTNS:
        # Note(deray): Assigning ``extract`` attribute to return
        #     1. the firmware file itself
        #     2. boolean (False) to indicate firmware file is not extracted
        def dummy_extract(self):
            """Dummy (no-op) extract method

            :returns: the same firmware file with the complete path
            :returns: boolean(False) to indicate that a new file is not
                      generated.
            """
            return fw_img_extractor.fw_file, False

        fw_img_extractor.extract = types.MethodType(
            dummy_extract, fw_img_extractor)
    else:
        raise exception.InvalidInputError(
            'Unexpected compact firmware file type: %s' % fw_file)

    return fw_img_extractor


def _extract_scexe_file(self, target_file, extract_path):
    """Extracts the scexe file.

    :param target_file: the firmware file to be extracted from
    :param extract_path: the path where extraction is supposed to happen
    """
    # Command to extract the smart component file.
    unpack_cmd = '--unpack=' + extract_path
    # os.path.isfile(target_file)
    cmd = [target_file, unpack_cmd]
    out, err = utils.trycmd(*cmd)


def _extract_rpm_file(self, target_file, extract_path):
    """Extracts the rpm file.

    :param target_file: the firmware file to be extracted from
    :param extract_path: the path where extraction is supposed to happen
    :raises: ImageExtractionFailed, if any issue with extraction
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
    except Exception:
        raise exception.ImageExtractionFailed(
            image_ref=target_file,
            reason='Unexpected error in extracting file.')


def _get_firmware_file(path):
    """Gets the raw firmware file

    Gets the raw firmware file from the extracted directory structure
    :param path: the directory structure to search for
    :returns: the raw firmware file with the complete path
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_name, file_ext = os.path.splitext(os.path.basename(filename))
            if file_ext in RAW_FIRMWARE_EXTNS:
                # return filename
                return os.path.join(dirpath, filename)


def _get_firmware_file_in_new_path(searching_path):
    """Gets the raw firmware file in a new path

    Gets the raw firmware file from the extracted directory structure
    and creates a hard link to that in a file path and cleans up the
    lookup extract path.
    :param searching_path: the directory structure to search for
    :returns: the raw firmware file with the complete new path
    """
    firmware_file_path = _get_firmware_file(searching_path)
    if not firmware_file_path:
        return None

    # Note(deray): the path of the new firmware file will be of the form:
    #
    #    [TEMP_DIR]/xxx-xxx_actual_firmware_filename
    #
    # e.g. /tmp/77e8f689-f32c-4727-9fc3-a7dacefe67e4_ilo4_210.bin
    file_name, file_ext_with_dot = common.get_filename_and_extension_of(
        firmware_file_path)
    new_firmware_file_path = os.path.join(
        tempfile.gettempdir(), str(uuid.uuid4()) + '_' +
        file_name + file_ext_with_dot)

    # create a hard link to the raw firmware file
    os.link(firmware_file_path, new_firmware_file_path)
    return new_firmware_file_path
