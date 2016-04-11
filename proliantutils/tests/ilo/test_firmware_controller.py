# Copyright 2016 Hewlett Packard Enterprise Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Test Class for Firmware controller."""
import os
import shutil
import tempfile
import unittest

import ddt
import mock
from six.moves import builtins as __builtin__

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import firmware_controller


@ddt.ddt
class FirmwareControllerModuleTestCase(unittest.TestCase):

    def setUp(self):
        # | BEFORE_EACH |
        super(FirmwareControllerModuleTestCase, self).setUp()
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'
        self.any_raw_fw_file = 'any_fw_file.bin'

    @ddt.data('ilo', 'cpld', 'power_pic', 'bios', 'chassis')
    def test_check_firmware_update_component_passes_for_valid_component(
            self, component_type):
        # | GIVEN |
        ris_or_ribcl_obj_mock = mock.MagicMock()
        update_firmware_mock = mock.MagicMock()
        # Note(deray): Need to set __name__ attribute explicitly to keep
        # ``six.wraps`` happy. Passing this to the `name` argument at the time
        # creation of Mock doesn't help.
        update_firmware_mock.__name__ = 'update_firmware_mock'
        wrapped_func = (firmware_controller.
                        check_firmware_update_component(update_firmware_mock))
        # | WHEN |
        wrapped_func(
            ris_or_ribcl_obj_mock, self.any_raw_fw_file, component_type)
        #  | THEN |
        update_firmware_mock.assert_called_once_with(
            ris_or_ribcl_obj_mock, self.any_raw_fw_file, component_type)

    def test_check_firmware_update_component_throws_for_invalid_component(
            self):
        # | GIVEN |
        def func(ris_or_ribcl_obj, filename, component_type):
            pass

        wrapped_func = (firmware_controller.
                        check_firmware_update_component(func))
        ris_or_ribcl_obj_mock = mock.MagicMock()
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          wrapped_func,
                          ris_or_ribcl_obj_mock,
                          self.any_raw_fw_file,
                          'invalid_component')

    def test_get_fw_extractor_will_set_the_fw_file_attribute(self):
        # | WHEN |
        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_scexe_file))
        # | THEN |
        self.assertEqual(self.any_scexe_file, fw_img_extractor.fw_file)

    @mock.patch.object(firmware_controller, '_extract_scexe_file',
                       autospec=True)
    def test__extract_scexe_file_gets_invoked_for_scexe_firmware_file(
            self, _extract_scexe_file_mock):
        # _extract_scexe_file gets invoked when fw_img_extractor is initialized
        # with scexe firmware file
        # | WHEN |
        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_scexe_file))
        fw_img_extractor._do_extract('some_target_file', 'some_extract_path')
        # | THEN |
        _extract_scexe_file_mock.assert_called_once_with(
            fw_img_extractor, 'some_target_file', 'some_extract_path')

    @mock.patch.object(firmware_controller, '_extract_rpm_file', autospec=True)
    def test__extract_rpm_file_gets_invoked_for_rpm_firmware_file(
            self, _extract_rpm_file_mock):
        # _extract_rpm_file gets invoked when fw_img_extractor is initialized
        # with rpm firmware file
        # | WHEN |
        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_rpm_file))
        fw_img_extractor._do_extract('some_target_file', 'some_extract_path')
        # | THEN |
        _extract_rpm_file_mock.assert_called_once_with(
            fw_img_extractor, 'some_target_file', 'some_extract_path')

    @ddt.data('any_file.hex', 'any_file.bin', 'any_file.vme', 'any_file.flash')
    def test_no_op_extract_gets_invoked_for_raw_firmware_file(self,
                                                              any_raw_file):
        # no_op extract when fw_img_extractor is initialized
        # with raw firmware file
        # | WHEN |
        fw_img_extractor = firmware_controller.get_fw_extractor(any_raw_file)
        return_result, is_extracted = fw_img_extractor.extract()
        # | THEN |
        self.assertEqual(any_raw_file, return_result)
        self.assertFalse(is_extracted)

    def test_get_fw_extractor_raises_exception_with_unknown_firmware_file(
            self):
        # | GIVEN |
        any_invalid_format_firmware_file = 'any_file.abc'
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          firmware_controller.get_fw_extractor,
                          any_invalid_format_firmware_file)

    @mock.patch.object(firmware_controller.utils, 'trycmd', autospec=True)
    def test__extract_scexe_file_issues_command_as(self, utils_trycmd_mock):
        # | GIVEN |
        any_scexe_firmware_file = 'any_file.scexe'
        any_extract_path = 'any_extract_path'
        utils_trycmd_mock.return_value = ('out', 'err')
        # | WHEN |
        firmware_controller._extract_scexe_file(
            None, any_scexe_firmware_file, any_extract_path)
        # | THEN |
        utils_trycmd_mock.assert_called_once_with(
            any_scexe_firmware_file, '--unpack=' + any_extract_path)

    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, 'subprocess', autospec=True)
    def test__extract_rpm_file_creates_dir_if_extract_path_doesnt_exist(
            self, subprocess_mock, os_mock):
        # | GIVEN |
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = False
        mock_cpio = mock.MagicMock()
        mock_cpio.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [mock.MagicMock(), mock_cpio]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # | WHEN |
        firmware_controller._extract_rpm_file(
            None, any_rpm_firmware_file, any_extract_path)
        # | THEN |
        os_mock.makedirs.assert_called_once_with(any_extract_path)

    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, 'subprocess', autospec=True)
    def test__extract_rpm_file_doesnt_create_dir_if_extract_path_present(
            self, subprocess_mock, os_mock):
        # extract_rpm_file doesn't create dir if extract path
        # is already present
        # | GIVEN |
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = True
        mock_cpio = mock.MagicMock()
        mock_cpio.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [mock.MagicMock(), mock_cpio]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # | WHEN |
        firmware_controller._extract_rpm_file(
            None, any_rpm_firmware_file, any_extract_path)
        # | THEN |
        self.assertFalse(os_mock.makedirs.called)

    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, 'subprocess', autospec=True)
    def test__extract_rpm_file_issues_commands_as(self,
                                                  subprocess_mock,
                                                  os_mock):
        # | GIVEN |
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        os_mock.path.exists.return_value = True
        rpm2cpio_mock = mock.MagicMock()
        cpio_mock = mock.MagicMock()
        cpio_mock.communicate.return_value = ('out', 'err')
        subsequent_popen_call_returns = [rpm2cpio_mock, cpio_mock]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # | WHEN |
        firmware_controller._extract_rpm_file(
            None, any_rpm_firmware_file, any_extract_path)
        # | THEN |
        popen_calls_to_assert = [
            mock.call.Popen('rpm2cpio ' + any_rpm_firmware_file,
                            shell=True,
                            stdout=subprocess_mock.PIPE),
            mock.call.Popen('cpio -idm',
                            shell=True,
                            stdin=rpm2cpio_mock.stdout),
        ]
        subprocess_mock.assert_has_calls(popen_calls_to_assert)
        cpio_mock.communicate.assert_called_once_with()

    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, 'subprocess', autospec=True)
    def test__extract_rpm_file_raises_exception_if_it_fails(self,
                                                            subprocess_mock,
                                                            os_mock):
        # | GIVEN |
        any_rpm_firmware_file = 'any_file.rpm'
        any_extract_path = 'any_extract_path'

        rpm2cpio_mock = mock.MagicMock()
        cpio_mock = mock.MagicMock()
        cpio_mock.communicate.side_effect = Exception('foo')
        subsequent_popen_call_returns = [rpm2cpio_mock, cpio_mock]
        subprocess_mock.Popen = mock.MagicMock(
            side_effect=subsequent_popen_call_returns)
        # | WHEN | & | THEN |
        self.assertRaises(exception.ImageExtractionFailed,
                          firmware_controller._extract_rpm_file,
                          None, any_rpm_firmware_file, any_extract_path)

    def test__get_firmware_file(self):
        # | GIVEN |
        temp_dir_setup = setup_fixture_create_fw_file_extracts_for('scexe')
        # | WHEN |
        return_result = firmware_controller._get_firmware_file(temp_dir_setup)
        # | THEN |
        self.assertTrue(return_result.endswith('.bin'))
        teardown_fixture_create_fw_file_extracts_for(temp_dir_setup)

    @mock.patch.object(
        firmware_controller, '_get_firmware_file', autospec=True)
    @mock.patch.object(common, 'get_filename_and_extension_of', autospec=True)
    @mock.patch.object(firmware_controller, 'tempfile', autospec=True)
    @mock.patch.object(firmware_controller.uuid, 'uuid4', autospec=True)
    @mock.patch.object(firmware_controller.os, 'link', autospec=True)
    def test__get_firmware_file_in_new_path(
            self, os_link_mock, uuid4_mock, tempfile_mock,
            get_filename_and_extension_of_mock, _get_firmware_file_mock):
        # | GIVEN |
        _get_firmware_file_mock.return_value = 'some_raw_fw_file.bin'
        get_filename_and_extension_of_mock.return_value = ('some_raw_fw_file',
                                                           '.bin')
        tempfile_mock.gettempdir.return_value = '/tmp'
        uuid4_mock.return_value = 12345
        # | WHEN |
        new_fw_file_path = (firmware_controller.
                            _get_firmware_file_in_new_path('any_path'))
        # | THEN |
        _get_firmware_file_mock.assert_called_once_with('any_path')
        # tests the hard linking of the raw fw file so found
        os_link_mock.assert_called_once_with(
            'some_raw_fw_file.bin', '/tmp/12345_some_raw_fw_file.bin')
        self.assertEqual(new_fw_file_path, '/tmp/12345_some_raw_fw_file.bin')

    @mock.patch.object(
        firmware_controller, '_get_firmware_file', autospec=True)
    def test__get_firmware_file_in_new_path_returns_none_for_file_not_found(
            self, _get_firmware_file_mock):
        # | GIVEN |
        _get_firmware_file_mock.return_value = None
        # | WHEN |
        actual_result = (firmware_controller.
                         _get_firmware_file_in_new_path('any_path'))
        # | THEN |
        self.assertIsNone(actual_result)


def teardown_fixture_create_fw_file_extracts_for(temp_dir):
    # os.removedirs(temp_dir)
    shutil.rmtree(temp_dir)


def setup_fixture_create_fw_file_extracts_for(format):
    temp_dir = tempfile.mkdtemp()
    fw_file_exts = [
        '_ilo', '.bin', '.xml', '.TXT', '.hpsetup', '.cpq_package.inc'
    ]

    if format == 'scexe':
        fw_files_dir = temp_dir
    elif format == 'rpm':
        fw_files_dir = os.path.join(
            temp_dir +
            '/please_remove_rpm_file_extracts/usr/lib/i386-linux-gnu/' +
            'hp-firmware-iloX-xxxx'
        )
    else:
        fw_files_dir = temp_dir

    if not os.path.exists(fw_files_dir):
        os.makedirs(fw_files_dir)

    for fw_file_ext in fw_file_exts:
        tempfile.NamedTemporaryFile(suffix=fw_file_ext,
                                    dir=fw_files_dir,
                                    delete=False)

    return temp_dir


class FirmwareImageExtractorTestCase(unittest.TestCase):

    def setUp(self):
        # | BEFORE_EACH |
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(firmware_controller, 'tempfile', autospec=True)
    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, '_get_firmware_file_in_new_path',
                       autospec=True)
    @mock.patch.object(firmware_controller, 'shutil', autospec=True)
    def test_extract_method_calls__do_extract_in_turn(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            os_mock, tempfile_mock, add_exec_permission_to_mock):
        # | GIVEN |
        os_mock.path.splitext.return_value = ('any_file', '.scexe')
        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_scexe_file))
        # Now mock the _do_extract method of fw_img_extractor instance
        _do_extract_mock = mock.MagicMock()
        fw_img_extractor._do_extract = _do_extract_mock

        expected_return_result = 'extracted_firmware_file'
        _get_firmware_file_in_new_path_mock.return_value = (
            expected_return_result)
        # | WHEN |
        actual_return_result, is_extracted = fw_img_extractor.extract()
        # | THEN |
        _do_extract_mock.assert_called_once_with(self.any_scexe_file, mock.ANY)
        self.assertEqual(expected_return_result, actual_return_result)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(firmware_controller, 'tempfile', autospec=True)
    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, '_get_firmware_file_in_new_path',
                       autospec=True)
    @mock.patch.object(firmware_controller, 'shutil', autospec=True)
    def test_extract_deletes_temp_extracted_folder_before_raising_exception(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            os_mock, tempfile_mock, add_exec_permission_to_mock):
        # | GIVEN |
        os_mock.path.splitext.return_value = ('any_file', '.rpm')

        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_rpm_file))
        # Now mock the _do_extract method of fw_img_extractor instance
        exc = exception.ImageExtractionFailed(
            image_ref=self.any_rpm_file, reason='God only knows!')
        _do_extract_mock = mock.MagicMock(side_effect=exc)
        fw_img_extractor._do_extract = _do_extract_mock
        # | WHEN | & | THEN |
        self.assertRaises(exception.ImageExtractionFailed,
                          fw_img_extractor.extract)
        shutil_mock.rmtree.assert_called_once_with(
            tempfile_mock.mkdtemp.return_value, ignore_errors=True)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(firmware_controller, 'tempfile', autospec=True)
    @mock.patch.object(firmware_controller, 'os', autospec=True)
    @mock.patch.object(firmware_controller, '_extract_scexe_file',
                       autospec=True)
    @mock.patch.object(firmware_controller, '_get_firmware_file_in_new_path',
                       autospec=True)
    @mock.patch.object(firmware_controller, 'shutil', autospec=True)
    def test_extract_method_raises_exception_if_raw_fw_file_not_found(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            _extract_scexe_mock, os_mock, tempfile_mock,
            add_exec_permission_to_mock):
        # | GIVEN |
        os_mock.path.splitext.return_value = ('any_file', '.scexe')
        _get_firmware_file_in_new_path_mock.return_value = None
        fw_img_extractor = (firmware_controller.
                            get_fw_extractor(self.any_scexe_file))
        # | WHEN | & | THEN |
        self.assertRaises(exception.InvalidInputError,
                          fw_img_extractor.extract)

    @mock.patch.object(common, 'add_exec_permission_to', autospec=True)
    @mock.patch.object(firmware_controller, 'tempfile', autospec=True)
    @mock.patch.object(firmware_controller, '_extract_scexe_file',
                       autospec=True)
    @mock.patch.object(firmware_controller, '_extract_rpm_file', autospec=True)
    # don't use autospec=True here(below one), setting side_effect
    # causes issue. refer https://bugs.python.org/issue17826
    @mock.patch.object(firmware_controller, '_get_firmware_file_in_new_path')
    @mock.patch.object(firmware_controller, 'shutil', autospec=True)
    def test_successive_calls_to_extract_method(
            self, shutil_mock, _get_firmware_file_in_new_path_mock,
            _extract_rpm_mock, _extract_scexe_mock, tempfile_mock,
            add_exec_permission_to_mock):
        """This is more of an integration test of the extract method

        """
        # | GIVEN |
        firmware_files = [
            self.any_scexe_file,
            'any_file.bin',
            self.any_rpm_file,
        ]
        actual_raw_fw_files = []
        expected_raw_fw_files = [
            ('extracted_file_from_scexe', True),
            ('any_file.bin', False),
            ('extracted_file_from_rpm', True)
        ]
        _get_firmware_file_in_new_path_mock.side_effect = [
            'extracted_file_from_scexe',
            'extracted_file_from_rpm',
        ]
        # | WHEN |
        for fw_file in firmware_files:
            fw_img_extractor = firmware_controller.get_fw_extractor(fw_file)
            raw_fw_file, is_extracted = fw_img_extractor.extract()
            actual_raw_fw_files.append((raw_fw_file, is_extracted))
        # | THEN |
        self.assertSequenceEqual(actual_raw_fw_files, expected_raw_fw_files)


@ddt.ddt
class FirmwareImageUploaderTestCase(unittest.TestCase):

    def setUp(self):
        # | BEFORE_EACH |
        self.any_scexe_file = 'any_file.scexe'
        self.any_rpm_file = 'any_file.rpm'

    @mock.patch.object(firmware_controller.FirmwareImageUploader,
                       '_get_socket', autospec=True)
    @mock.patch.object(firmware_controller, 'socket')
    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_upload_file_to_returns_cookie_after_successful_upload(
            self, open_mock, socket_mock, _get_socket_mock):
        # | GIVEN |
        sock_mock = _get_socket_mock.return_value
        sock_mock.read.side_effect = [b'data returned from socket with ',
                                      b'Set-Cookie: blah_blah_cookie',
                                      b'']
        fw_img_uploader = (firmware_controller.
                           FirmwareImageUploader('any_raw_file'))
        # | WHEN |
        cookie = fw_img_uploader.upload_file_to(('host', 'port'), 60)
        # | THEN |
        self.assertEqual('blah_blah_cookie', cookie)

    @mock.patch.object(firmware_controller.FirmwareImageUploader,
                       '_get_socket', autospec=True)
    @mock.patch.object(firmware_controller, 'socket')
    @mock.patch.object(__builtin__, 'open', autospec=True)
    def test_upload_file_to_throws_exception_when_cookie_not_returned(
            self, open_mock, socket_mock, _get_socket_mock):
        # | GIVEN |
        sock_mock = _get_socket_mock.return_value
        sock_mock.read.side_effect = [b'data returned from socket with ',
                                      b'No-Cookie',
                                      b'']
        fw_img_uploader = (firmware_controller.
                           FirmwareImageUploader('any_raw_file'))
        # | WHEN | & | THEN |
        self.assertRaises(exception.IloError, fw_img_uploader.upload_file_to,
                          ('host', 'port'), 60)

    @mock.patch.object(firmware_controller, 'socket')
    @mock.patch.object(firmware_controller, 'ssl')
    def test__get_socket_returns_ssl_wrapped_socket_if_all_goes_well(
            self, ssl_mock, socket_mock):
        # | GIVEN |
        socket_mock.getaddrinfo().__iter__.return_value = [
            # (family, socktype, proto, canonname, sockaddr),
            (10, 1, 6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
            (2, 1, 6, '', ('0.0.0.0-some-address', 80)),
        ]
        fw_img_uploader = (firmware_controller.
                           FirmwareImageUploader('any_raw_file'))
        fw_img_uploader.hostname = 'host'
        fw_img_uploader.port = 443
        fw_img_uploader.timeout = 'timeout'
        # | WHEN |
        returned_sock = fw_img_uploader._get_socket()
        # | THEN |
        socket_mock.socket.assert_has_calls([
            mock.call(10, 1, 6),
            mock.call().settimeout('timeout'),
            mock.call().connect(
                ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),

            mock.call(2, 1, 6),
            mock.call().settimeout('timeout'),
            mock.call().connect(('0.0.0.0-some-address', 80)),
        ])
        self.assertTrue(ssl_mock.wrap_socket.called)
        self.assertEqual(returned_sock, ssl_mock.wrap_socket())

    @ddt.data(('foo.bar.com', exception.IloConnectionError),
              ('1.1.1.1', exception.IloConnectionError),
              ('any_kind_of_address', exception.IloConnectionError),)
    @ddt.unpack
    def test__get_socket_throws_exception_in_case_of_failed_connection(
            self, input_hostname, expected_exception_type):
        # | GIVEN |
        fw_img_uploader = (firmware_controller.
                           FirmwareImageUploader('any_raw_file'))
        fw_img_uploader.hostname = input_hostname
        fw_img_uploader.port = 443
        fw_img_uploader.timeout = 1
        # | WHEN | & | THEN |
        self.assertRaises(expected_exception_type, fw_img_uploader._get_socket)
