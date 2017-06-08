# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import mock
from sushy import connector
import testtools

from proliantutils.redfish import main
from proliantutils.redfish.resources.system import system


class HPESushyTestCase(testtools.TestCase):

    @mock.patch.object(connector, 'Connector', autospec=True)
    def setUp(self, connector_mock):
        super(HPESushyTestCase, self).setUp()
        self.hpe_sushy = main.HPESushy('https://1.2.3.4',
                                       username='foo',
                                       password='bar')

    @mock.patch.object(system, 'HPESystem', autospec=True)
    def test_get_system(self, mock_system):
        sys_inst = self.hpe_sushy.get_system('1234')
        self.assertTrue(isinstance(sys_inst,
                                   system.HPESystem.__class__))
        mock_system.assert_called_once_with(self.hpe_sushy._conn,
                                            '1234',
                                            self.hpe_sushy.redfish_version)
