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

import ConfigParser
import os

from proliantutils.ilo import ribcl
# Commenting to satisfy pep8
# from proliantutils.ilo import ris


def _is_mock_enabled():

    conf_file = os.path.join(os.getenv('HOME'), 'proliantutils.conf')
    Config = ConfigParser.ConfigParser()
    Config.read(conf_file)
    if 'mock' in Config.sections():
        try:
            value = Config.get('mock', 'enable')
            return bool(value)
        except Exception:
            return False
    return False


class IloClient(object):

    def __new__(self, host, login, password, timeout=60, port=443,
                bios_password=None):

        # Mock support with VirtualBox
        if _is_mock_enabled():
            from proliantutils.ilo import virtualbox
            return virtualbox.VirtualBoxOperations(host,
                                                   login,
                                                   password,
                                                   timeout,
                                                   port)

        # Object is created based on the server model
        client = ribcl.RIBCLOperations(host, login, password, timeout, port)

        # Till the full RIS Integration is done, disabling the automatic switch
        # between RIS and RIBCL CLient. Defaulting it to RIBCL for now.
        # TODO(Anusha): Uncomment when full RIS library is available.
#         model = client.get_product_name()
#
#         if 'Gen9' in model:
#             client = ris.RISOperations(host, login, password, bios_password)
        return client
