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
"""IloClient module"""

import functools

from proliantutils.ilo import ipmi
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils import log

SUPPORTED_RIS_METHODS = [
    'activate_license',
    'clear_secure_boot_keys',
    'eject_virtual_media',
    'get_current_boot_mode',
    'get_host_power_status',
    'get_http_boot_url',
    'get_ilo_firmware_version_as_major_minor',
    'get_one_time_boot',
    'get_pending_boot_mode',
    'get_persistent_boot_device',
    'get_product_name',
    'get_secure_boot_mode',
    'get_server_capabilities',
    'get_vm_status',
    'hold_pwr_btn',
    'insert_virtual_media',
    'press_pwr_btn',
    'reset_bios_to_default',
    'reset_ilo_credential',
    'reset_secure_boot_keys',
    'reset_server',
    'set_host_power',
    'set_http_boot_url',
    'set_one_time_boot',
    'set_pending_boot_mode',
    'set_secure_boot_mode',
    'get_server_capabilities',
    'set_iscsi_boot_info',
    'set_vm_status',
    'update_firmware',
    'update_persistent_boot',
    ]

LOG = log.get_logger(__name__)


class IloClient:

    def __init__(self, host, login, password, timeout=60, port=443,
                 bios_password=None, cacert=None):
        self.ribcl = ribcl.RIBCLOperations(host, login, password, timeout,
                                           port, cacert=cacert)
        self.ris = ris.RISOperations(host, login, password,
                                     bios_password=bios_password,
                                     cacert=cacert)
        self.info = {'address': host, 'username': login, 'password': password}
        self.host = host
        self.model = self.ribcl.get_product_name()
        LOG.debug(self._("IloClient object created. "
                         "Model: %(model)s"), {'model': self.model})

    def _(self, msg):
        """Prepends host information if available to msg and returns it."""
        try:
            return "[iLO %s] %s" % (self.host, msg)
        except AttributeError:
            return "[iLO <unknown>] %s" % msg

    def _call_method(self, method_name, *args, **kwargs):
        """Call the corresponding method using either RIBCL or RIS."""
        the_operation_object = self.ribcl
        if ('Gen9' in self.model) and (method_name in SUPPORTED_RIS_METHODS):
            the_operation_object = self.ris
        method = getattr(the_operation_object, method_name)

        LOG.debug(self._("Using %(class)s for method %(method)s."),
                  {'class': type(the_operation_object).__name__,
                   'method': method_name})

        return method(*args, **kwargs)

    def __getattr__(self, method):
        """Default method called when instance method not found."""
        return functools.partial(self._call_method, method)

    def get_server_capabilities(self):
        """Get hardware properties which can be used for scheduling

        :return: a dictionary of server capabilities.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        capabilities = self._call_method('get_server_capabilities')
        major_minor = (
            self._call_method('get_ilo_firmware_version_as_major_minor'))

        # NOTE(vmud213): Even if it is None, pass it on to get_nic_capacity
        # as we still want to try getting nic capacity through ipmitool
        # irrespective of what firmware we are using.
        nic_capacity = ipmi.get_nic_capacity(self.info, major_minor)
        if nic_capacity:
            capabilities.update({'nic_capacity': nic_capacity})
        if capabilities:
            return capabilities
