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
import random
import re
import shutil
import socket
import ssl
import stat
import subprocess
import sys
import tempfile
import time
import types

from oslo_concurrency import processutils as utils
import six

from proliantutils import exception

if six.PY3:
    def b(x):
        return bytes(x, 'ascii')

else:
    def b(x):
        return x

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

    :param target_file: the target file whose permission is changed
    """
    mode = os.stat(target_file).st_mode
    os.chmod(target_file, mode | stat.S_IXUSR)


class FirmwareImageProcessor(object):
    """Helper class to process the firmware image file

    This class acts as a helper class for firmware related
    operations. Some of the operations involved are:
        1. helps in extracting the raw firmware file from the
        compact firmware file.
        2. helps in uploading the firmware file to iLO.
    """

    HTTP_UPLOAD_HEADER = ("POST /cgi-bin/uploadRibclFiles HTTP/1.1\r\n"
                          "Host: localhost\r\nConnection: Close\r\n"
                          "Content-Length: %d\r\n"
                          "Content-Type: multipart/form-data; "
                          "boundary=%s\r\n\r\n")
    BLOCK_SIZE = 64 * 1024
    SSL_VERSION = ssl.PROTOCOL_TLSv1

    def __init__(self, fw_file):
        self.fw_file = fw_file
        file_name, file_ext_with_dot = get_filename_and_extension_of(
            fw_file)
        self.fw_filename = file_name
        self.fw_file_ext = file_ext_with_dot

    def extract(self):
        """Extracts the raw firmware file from its compact format

        :raises: IloInvalidInputError, if raw firmware file not found
        :raises: IloError, for other internal problems
        :returns: the raw firmware file with the complete path
        """
        target_file = self.fw_file
        add_exec_permission_to(target_file)
        temp_dir = tempfile.mkdtemp()
        extract_path = os.path.join(temp_dir, self.fw_filename)

        self._do_extract(target_file, extract_path)

        firmware_file_path = _get_firmware_file_in_new_path(extract_path)
        if not firmware_file_path:
            raise exception.IloInvalidInputError(
                "Raw firmware file not found from: %s" % target_file)

        return firmware_file_path

    def upload_file_to(self, addressinfo, timeout):
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
            if len(part) < self.BLOCK_SIZE:
                sock.write(part)
            else:
                sent = 0
                fwlen = len(part)
                while sent < fwlen:
                    written = sock.write(part[sent:sent+self.BLOCK_SIZE])
                    if written is None:
                        plen = len(part[sent:sent+self.BLOCK_SIZE])
                        raise exception.IloConnectionError(
                            "Unexpected EOF while sending %d bytes "
                            "(%d of %d sent before)" % (plen, sent, fwlen))

                    sent += written
#                     if callable(progress):
#                         progress("Sending request %d/%d bytes (%d%%)" %
#                                    (sent, fwlen, 100.0*sent/fwlen))

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
                    "Communication with %s:%d failed: %s" %
                    (self.hostname, self.port, str(e))
                )

        # Received len(data) bytes
        if 'Set-Cookie:' not in data:
            raise exception.IloError("Internal problem occurred in "
                                     "uploading the file")
        cookie = re.search('Set-Cookie: *(.*)', data).group(1)
        return cookie

    def _get_socket(self):
        """Set up an https connection and do an HTTP/raw socket request

        """
        # Connecting to <self.hostname> at port <self.port>
        err = None
        for res in socket.getaddrinfo(
                self.hostname, self.port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                sock.settimeout(self.timeout)
                # self._debug(2, "Connecting to %s port %d" % sa[:2])
                sock.connect(sa)
            except socket.timeout:
                if sock is not None:
                    sock.close()
                err = exception.IloConnectionError(
                    "Timeout connecting to %s port %d"
                    % (self.hostname, self.port)
                )
            except socket.error:
                if sock is not None:
                    sock.close()
                e = sys.exc_info()[1]
                err = exception.IloConnectionError(
                    "Error connecting to %s port %d: %s"
                    % (self.hostname, self.port, str(e))
                )

        if err is not None:
            raise err

        if not sock:
            raise exception.IloConnectionError(
                "Unable to resolve %s" % self.hostname
            )

        try:
            return ssl.wrap_socket(sock, ssl_version=self.SSL_VERSION)
        except socket.sslerror:
            e = sys.exc_info()[1]
            msg = (getattr(e, 'reason', None) or
                   getattr(e, 'message', None))
            # Some ancient iLO's don't support TLSv1, retry with SSLv3
            if ('wrong version number' in msg) and (
                    self.sslversion == ssl.PROTOCOL_TLSv1):
                self.SSL_VERSION = ssl.PROTOCOL_SSLv3
                return self._get_socket()
            raise exception.IloConnectionError(
                "Cannot establish ssl session with %s:%d: %s" %
                (self.hostname, self.port, msg)
            )


def get_fw_extractor(fw_file):
    """Gets the firmware extractor object fine-tuned for specified type

    :param fw_file: compact firmware file to be extracted from
    :raises: IloInvalidInputError, for unsupported file types
    :returns: FirmwareImageProcessor object
    """
    fw_img_extractor = FirmwareImageProcessor(fw_file)
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
        # assign extract attribute to return the file itself

        def dummy_extract(self):
            return fw_img_extractor.fw_file

        fw_img_extractor.extract = types.MethodType(
            dummy_extract, fw_img_extractor)
    else:
        raise exception.IloInvalidInputError(
            'Unexpected compact firmware file type: {}'.format(
                fw_file))

    return fw_img_extractor


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
    :raises: IloError, if any problem in running extraction command
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
        raise exception.IloError('Unexpected error in extracting file: {}'
                                 .format(target_file))


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
        # even if the raw firmware file was not found,
        # then also cleanup the directory
        shutil.rmtree(searching_path, ignore_errors=True)
        return None

    # create a hard link to the raw firmware file and
    # delete the entire extracted content
    new_firmware_file_path = os.path.join(
        tempfile.mkdtemp(), os.path.basename(firmware_file_path))
    os.link(firmware_file_path, new_firmware_file_path)
    shutil.rmtree(searching_path, ignore_errors=True)

    return new_firmware_file_path
