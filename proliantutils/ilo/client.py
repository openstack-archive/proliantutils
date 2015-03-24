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

from proliantutils.ilo import ribcl
from proliantutils.ilo import ris


class IloClient(object):

    def __new__(self, host, login, password, timeout=60, port=443,
                bios_password=None):
        # Object is created based on the server model
        client = ribcl.RIBCLOperations(host, login, password, timeout, port)
        model = client.get_product_name()
        if 'Gen9' in model:
            client = ris.RISOperations(host, login, password, timeout=timeout,
                                       port=port, bios_password=bios_password)
        return client