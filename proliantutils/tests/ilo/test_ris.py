# Copyright 2014 Hewlett-Packard Development Company, L.P.
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
import unittest

import mock
import ris_constants

from proliantutils.ilo import ris


class IloRisTestCase(unittest.TestCase):

    def setUp(self):
        super(IloRisTestCase, self).setUp()
        self.ilo = ris.RISOperations("x.x.x.x", "Administrator", "admin", None)

    @mock.patch.object(ris.RISOperations, '_get_bios_setting')
    def test_get_http_boot_url(self, get_bios_settings_mock):
        get_bios_settings_mock.return_value = ris_constants.GET_HTTP_BOOT_URL
        result = self.ilo.get_http_boot_url()
        self.assertTrue(
            'http://10.10.1.30:8081/startup.nsh' in
            result['UefiShellStartupUrl']
            )

    @mock.patch.object(ris.RISOperations, '_change_bios_setting')
    def test_set_http_boot_url(self, change_bios_setting_mock):
        change_bios_setting_mock.return_value = ris_constants.SET_HTTP_BOOT_URL
        self.ilo.set_http_boot_url('http://10.10.1.30:8081/startup.nsh')
        change_bios_setting_mock.assert_called_once_with({
            "UefiShellStartupUrl": "http://10.10.1.30:8081/startup.nsh"
            })
