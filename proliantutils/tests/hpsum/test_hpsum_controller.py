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

import os
import shutil
import tempfile

import mock
from oslo_concurrency import processutils
import testtools

from proliantutils import exception
from proliantutils.hpsum import hpsum_controller
from proliantutils.ilo import client as ilo_client
from proliantutils.tests.hpsum import hpsum_sample_output as constants
from proliantutils import utils


class HpsumFirmwareUpdateTest(testtools.TestCase):

    def setUp(self):
        super(HpsumFirmwareUpdateTest, self).setUp()
        self.info = {'ilo_address': '1.2.3.4',
                     'ilo_password': '12345678',
                     'ilo_username': 'admin'}
        clean_step = {
            'interface': 'management',
            'step': 'update_firmware',
            'args': {'firmware_update_mode': u'hpsum',
                     'firmware_images': [{'url': 'http://1.2.3.4/SPP.iso',
                                          'checksum': '1234567890'}]}}
        self.node = {'driver_info': self.info,
                     'clean_step': clean_step}

    @mock.patch.object(hpsum_controller, 'open',
                       mock.mock_open(read_data=constants.HPSUM_OUTPUT_DATA))
    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(processutils, 'execute')
    def test_execute_hpsum(self, execute_mock, exists_mock):
        exists_mock.return_value = True
        value = ("hpsum_service_x64 started successfully. Sending Shutdown "
                 "request to engine. Successfully shutdown the service.")
        execute_mock.side_effect = processutils.ProcessExecutionError(
            stdout=value, stderr=None, exit_code=0)
        ret_value = ("Summary: The smart component was installed successfully."
                     " Status of updated components: Total: 2 Success: 2 "
                     "Failed: 0.")

        stdout = hpsum_controller._execute_hpsum("hpsum", components=None)

        self.assertEqual(ret_value, stdout)
        execute_mock.assert_called_once_with("hpsum", "--s", "--romonly", "")

    @mock.patch.object(processutils, 'execute')
    def test_execute_hpsum_with_args(self, execute_mock):
        value = ("hpsum_service_x64 started successfully. Sending Shutdown "
                 "request to engine. Successfully shutdown the service.")
        execute_mock.side_effect = processutils.ProcessExecutionError(
            stdout=value, stderr=None, exit_code=3)
        ret_value = ("Summary: The smart component was not installed. Node is "
                     "already up-to-date.")

        stdout = hpsum_controller._execute_hpsum("hpsum",
                                                 components=["foo", "bar"])

        execute_mock.assert_called_once_with(
            "hpsum", "--s", "--romonly", " --c foo --c bar")
        self.assertEqual(ret_value, stdout)

    @mock.patch.object(
        hpsum_controller, 'open',
        mock.mock_open(read_data=constants.HPSUM_OUTPUT_DATA_FAILURE))
    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(processutils, 'execute')
    def test_execute_hpsum_update_fails(self, execute_mock, exists_mock):
        exists_mock.return_value = True
        ret = ("Summary: The installation of the component failed. Status "
               "of updated components: Total: 2 Success: 1 Failed: 1.")
        value = ("hpsum_service_x64 started successfully. Sending Shutdown "
                 "request to engine. Successfully shutdown the service.")
        execute_mock.side_effect = processutils.ProcessExecutionError(
            stdout=value, stderr=None, exit_code=253)

        stdout = hpsum_controller._execute_hpsum("hpsum", components=None)

        self.assertEqual(ret, stdout)
        execute_mock.assert_called_once_with("hpsum", "--s", "--romonly", "")

    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(processutils, 'execute')
    def test_execute_hpsum_fails(self, execute_mock, exists_mock):
        exists_mock.return_value = False
        value = ("Error: Cannot launch hpsum_service_x64 locally. Reason: "
                 "General failure.")
        execute_mock.side_effect = processutils.ProcessExecutionError(
            stdout=value, stderr=None, exit_code=255)

        ex = self.assertRaises(exception.HpsumOperationError,
                               hpsum_controller._execute_hpsum, "hpsum",
                               None)
        self.assertIn(value, str(ex))

    @mock.patch.object(utils, 'validate_href')
    @mock.patch.object(utils, 'verify_image_checksum')
    @mock.patch.object(hpsum_controller, '_execute_hpsum')
    @mock.patch.object(os, 'listdir')
    @mock.patch.object(shutil, 'rmtree', autospec=True)
    @mock.patch.object(tempfile, 'mkdtemp', autospec=True)
    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(os, 'mkdir')
    @mock.patch.object(processutils, 'execute')
    @mock.patch.object(ilo_client, 'IloClient', spec_set=True, autospec=True)
    def test_update_firmware(self, client_mock, execute_mock, mkdir_mock,
                             exists_mock, mkdtemp_mock, rmtree_mock,
                             listdir_mock, execute_hpsum_mock,
                             verify_image_mock, validate_mock):
        ilo_mock_object = client_mock.return_value
        eject_media_mock = ilo_mock_object.eject_virtual_media
        insert_media_mock = ilo_mock_object.insert_virtual_media
        execute_hpsum_mock.return_value = 'SUCCESS'
        listdir_mock.return_value = ['SPP_LABEL']
        mkdtemp_mock.return_value = "/tempdir"
        null_output = ["", ""]
        exists_mock.side_effect = [True, False]
        execute_mock.side_effect = [null_output, null_output]

        ret_val = hpsum_controller.update_firmware(self.node)

        eject_media_mock.assert_called_once_with('CDROM')
        insert_media_mock.assert_called_once_with('http://1.2.3.4/SPP.iso',
                                                  'CDROM')
        execute_mock.assert_any_call('mount', "/dev/disk/by-label/SPP_LABEL",
                                     "/tempdir")
        execute_hpsum_mock.assert_any_call('/tempdir/hp/swpackages/hpsum',
                                           components=None)
        exists_mock.assert_called_once_with("/dev/disk/by-label/SPP_LABEL")
        execute_mock.assert_any_call('umount', "/tempdir")
        mkdtemp_mock.assert_called_once_with()
        rmtree_mock.assert_called_once_with("/tempdir", ignore_errors=True)
        self.assertEqual('SUCCESS', ret_val)

    @mock.patch.object(utils, 'validate_href')
    @mock.patch.object(ilo_client, 'IloClient', spec_set=True, autospec=True)
    def test_update_firmware_vmedia_attach_fails(self, client_mock,
                                                 validate_mock):
        ilo_mock_object = client_mock.return_value
        eject_media_mock = ilo_mock_object.eject_virtual_media
        value = ("Unable to attach hpsum SPP iso http://1.2.3.4/SPP.iso "
                 "to the iLO")
        eject_media_mock.side_effect = exception.IloError(value)

        exc = self.assertRaises(exception.IloError,
                                hpsum_controller.update_firmware, self.node)
        self.assertEqual(value, str(exc))

    @mock.patch.object(utils, 'validate_href')
    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(os, 'listdir')
    @mock.patch.object(ilo_client, 'IloClient', spec_set=True, autospec=True)
    def test_update_firmware_device_file_not_found(self, client_mock,
                                                   listdir_mock, exists_mock,
                                                   validate_mock):
        ilo_mock_object = client_mock.return_value
        eject_media_mock = ilo_mock_object.eject_virtual_media
        insert_media_mock = ilo_mock_object.insert_virtual_media

        listdir_mock.return_value = ['SPP_LABEL']
        exists_mock.return_value = False

        msg = ("An error occurred while performing hpsum based firmware "
               "update, reason: Unable to find the virtual media device "
               "for HPSUM")
        exc = self.assertRaises(exception.HpsumOperationError,
                                hpsum_controller.update_firmware, self.node)
        self.assertEqual(msg, str(exc))
        eject_media_mock.assert_called_once_with('CDROM')
        insert_media_mock.assert_called_once_with('http://1.2.3.4/SPP.iso',
                                                  'CDROM')
        exists_mock.assert_called_once_with("/dev/disk/by-label/SPP_LABEL")

    @mock.patch.object(utils, 'validate_href')
    @mock.patch.object(utils, 'verify_image_checksum')
    @mock.patch.object(processutils, 'execute')
    @mock.patch.object(tempfile, 'mkdtemp', autospec=True)
    @mock.patch.object(os, 'mkdir')
    @mock.patch.object(os.path, 'exists')
    @mock.patch.object(os, 'listdir')
    @mock.patch.object(ilo_client, 'IloClient', spec_set=True, autospec=True)
    def test_update_firmware_mount_fails(self, client_mock, listdir_mock,
                                         exists_mock, mkdir_mock,
                                         mkdtemp_mock, execute_mock,
                                         verify_image_mock, validate_mock):
        ilo_mock_object = client_mock.return_value
        eject_media_mock = ilo_mock_object.eject_virtual_media
        insert_media_mock = ilo_mock_object.insert_virtual_media
        listdir_mock.return_value = ['SPP_LABEL']
        exists_mock.return_value = True
        mkdtemp_mock.return_value = "/tempdir"
        execute_mock.side_effect = processutils.ProcessExecutionError

        msg = ("Unable to mount virtual media device "
               "/dev/disk/by-label/SPP_LABEL")
        exc = self.assertRaises(exception.HpsumOperationError,
                                hpsum_controller.update_firmware, self.node)
        self.assertIn(msg, str(exc))
        eject_media_mock.assert_called_once_with('CDROM')
        insert_media_mock.assert_called_once_with('http://1.2.3.4/SPP.iso',
                                                  'CDROM')
        exists_mock.assert_called_once_with("/dev/disk/by-label/SPP_LABEL")

    @mock.patch.object(hpsum_controller, 'open',
                       mock.mock_open(read_data=constants.HPSUM_OUTPUT_DATA))
    @mock.patch.object(os.path, 'exists')
    def test__parse_hpsum_ouput(self, exists_mock):
        exists_mock.return_value = True
        expt_ret = ("Summary: The smart component was installed successfully. "
                    "Status of updated components: Total: 2 Success: 2 "
                    "Failed: 0.")

        ret = hpsum_controller._parse_hpsum_ouput(0)

        exists_mock.assert_called_once_with(hpsum_controller.OUTPUT_FILE)
        self.assertEqual(expt_ret, ret)

    @mock.patch.object(
        hpsum_controller, 'open',
        mock.mock_open(read_data=constants.HPSUM_OUTPUT_DATA_FAILURE))
    @mock.patch.object(os.path, 'exists')
    def test__parse_hpsum_ouput_some_failed(self, exists_mock):
        exists_mock.return_value = True
        expt_ret = ("Summary: The installation of the component failed. "
                    "Status of updated components: Total: 2 Success: 1 "
                    "Failed: 1.")

        ret = hpsum_controller._parse_hpsum_ouput(253)

        exists_mock.assert_called_once_with(hpsum_controller.OUTPUT_FILE)
        self.assertEqual(expt_ret, ret)

    @mock.patch.object(os.path, 'exists')
    def test__parse_hpsum_ouput_fails(self, exists_mock):
        exists_mock.return_value = False
        expt_ret = ("UPDATE STATUS: UNKNOWN")

        ret = hpsum_controller._parse_hpsum_ouput(1)

        exists_mock.assert_called_once_with(hpsum_controller.OUTPUT_FILE)
        self.assertEqual(expt_ret, ret)
