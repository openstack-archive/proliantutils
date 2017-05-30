# Copyright 2017 Hewlett Packard Enterprise Development LP
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

__author__ = 'HPE'

from six.moves.urllib import parse
import sushy

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import operations
from proliantutils import log
from proliantutils.redfish.hpe_sushy import HPESushy
import proliantutils.redfish.resources.system.secure_boot as secure_boot


"""
Class specific for Redfish APIs.
"""

GET_POWER_STATE_MAP = {
    sushy.SYSTEM_POWER_STATE_ON: 'ON',
    sushy.SYSTEM_POWER_STATE_POWERING_ON: 'ON',
    sushy.SYSTEM_POWER_STATE_OFF: 'OFF',
    sushy.SYSTEM_POWER_STATE_POWERING_OFF: 'OFF'
}

DEVICE_COMMON_TO_REDFISH = {'NETWORK': 'Pxe',
                            'CDROM': 'Cd',
                            'HDD': 'Hdd',
                            'ISCSI': 'UefiTarget'}
DEVICE_REDFISH_TO_COMMON = dict(
    (v, k) for (k, v) in DEVICE_COMMON_TO_REDFISH.items())

LOG = log.get_logger(__name__)


class RedfishOperations(operations.IloOperations):
    """Operations supported on redfish based hardware.

    This is the list of APIs which are currently supported via Redfish mode
    of operation. This is a growing list which needs to be updated as and when
    the existing API/s (of its cousin RIS and RIBCL interfaces) are migrated.

    --- START ---

    * get_product_name(self)
    * get_host_power_status(self)

    --- END ---

    """

    def __init__(self, redfish_controller_ip, username, password,
                 bios_password=None, cacert=None, root_prefix='/redfish/v1/'):
        """A class representing supported RedfishOperations

        :param redfish_controller_ip: The ip address of the Redfish controller.
        :param username: User account with admin/server-profile access
            privilege
        :param password: User account password
        :param bios_password: bios password
        :param cacert: a path to a CA_BUNDLE file or directory with
            certificates of trusted CAs. If set to None, the driver will
            ignore verifying the SSL certificate; if it's a path the driver
            will use the specified certificate or one of the certificates in
            the directory. Defaults to None.
        :param root_prefix: The default URL prefix. This part includes
            the root service and version. Defaults to /redfish/v1
        """
        super(RedfishOperations, self).__init__()
        address = ('https://' + redfish_controller_ip)
        LOG.debug('Redfish address: %s', address)
        verify = False if cacert is None else cacert

        # for error reporting purpose
        self.host = redfish_controller_ip
        self._root_prefix = root_prefix

        try:
            self._sushy = HPESushy(
                address, username=username, password=password,
                root_prefix=root_prefix, verify=verify)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller at "%(controller)s" has '
                          'thrown error. Error %(error)s') %
                   {'controller': address, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloConnectionError(msg)

    def _get_system_collection_path(self):
        """Helper function to find the SystemCollection path"""
        systems_col = self._sushy.json.get('Systems')
        if not systems_col:
            raise exception.MissingAttributeError(attribute='Systems',
                                                  resource=self._root_prefix)
        return systems_col.get('@odata.id')

    def _get_sushy_system(self, system_id):
        """Get the sushy system for system_id

        :param system_id: The identity of the System resource
        :returns: the Sushy system instance
        :raises: IloError
        """
        system_url = parse.urljoin(self._get_system_collection_path(),
                                   system_id)
        try:
            return self._sushy.get_system(system_url)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish System "%(system)s" was not found. '
                          'Error %(error)s') %
                   {'system': system_id, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        """
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        sushy_system = self._get_sushy_system('1')
        return sushy_system.json.get('Model')

    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """
        # Assuming only one sushy_system present as part of collection,
        # as we are dealing with iLO's here.
        sushy_system = self._get_sushy_system('1')
        return GET_POWER_STATE_MAP.get(sushy_system.power_state)

    def get_secure_boot_mode(self):
        """Get the status of secure boot.

        :returns: True, if enabled, else False
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        sushy_system = self._get_sushy_system('1')
        secure_boot_res = sushy_system.secure_boot_resource
        secure_current = secure_boot_res.secure_boot_current
        #secure_enabled = secure_boot_res.secure_boot_enable
        if secure_current:
            LOG.debug("Secure boot is Enabled")
            return True

        LOG.debug("Secure boot is Disabled")
        return False

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server.

        :param secure_boot_enable: True, if secure boot needs to be enabled for next boot, else False.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported on the server.
        """
        if secure_boot_enable not in secure_boot.SECURE_BOOT_ENABLE_REV_MAP:
            LOG.error("Option not supported")
            print("Option not supported")
        else:
            #if self._is_boot_mode_uefi():
            sushy_system = self._get_sushy_system('1')
            data = {'SecureBootEnable' : secure_boot.SECURE_BOOT_ENABLE_REV_MAP[secure_boot_enable]}
            sushy_system.secure_boot_config(data)

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode of the server.

        Gets the boot mode to be set on next reset.
        :returns: either LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system('1')
        bios_settings = sushy_system.bios_settings
        boot_mode = bios_settings.BootMode
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        return boot_mode.upper()

    def get_current_boot_mode(self):
        """Retrieves the current boot mode of the server.

        :returns: Current boot mode, LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system('1')
        bios_resource = sushy_system.bios_resource
        boot_mode = bios_resource.BootMode 
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        return boot_mode.upper()

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot.

        :returns: Returns the first boot device that would be used in next
                  boot. Returns 'Normal' is no device is set.
        """
        sushy_system = self._get_sushy_system('1')
        if (sushy_system.boot['enabled'] == 'Once'):
            device = sushy_system.boot['target']
            if device in DEVICE_REDFISH_TO_COMMON:
                return DEVICE_REDFISH_TO_COMMON[device]
            return device
        else:
            return 'Normal'

    def _is_boot_mode_uefi(self):
        """Checks if the system is in uefi boot mode.

        :return: 'True' if the boot mode is uefi else 'False'
        :raises: IloError, on an error from iLO.
        """
        boot_mode = self.get_current_boot_mode()
        if boot_mode == 'UEFI':
            return True
        else:
            return False

    def _get_persistent_boot_devices(self):
        """Get details of persistent boot devices, its order

        :returns: List of dictionary of boot sources and
                  list of boot device order
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        sushy_system = self._get_sushy_system('1')

        # Get the Boot resource.
        boot_settings = sushy_system.bios_boot_settings

        # Get the BootSources resource
        try:
            boot_sources = boot_settings.BootSources
        except KeyError:
            msg = ("BootSources resource not found.")
            raise exception.IloError(msg)

        try:
            boot_order = boot_settings.PersistentBootConfigOrder
        except KeyError:
            msg = ("PersistentBootConfigOrder resource not found.")
            raise exception.IloCommandNotSupportedError(msg)

        return boot_sources, boot_order

    def get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system('1')
        try:
            # Return boot device if it is persistent.
            if sushy_system.boot['enabled'] == 'Continuous':
                device = sushy_system.boot['target']
                if device in DEVICE_REDFISH_TO_COMMON:
                    return DEVICE_REDFISH_TO_COMMON[device]
                return device
        except KeyError as e:
            msg = "get_persistent_boot_device failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        # Check if we are in BIOS boot mode.
        # There is no resource to fetch boot device order for BIOS boot mode
        if not self._is_boot_mode_uefi():
            return None

        # Get persistent boot device order for UEFI
        boot_sources, boot_devices = self._get_persistent_boot_devices()

        boot_string = ""
        try:
            for source in boot_sources:
                if (source["StructuredBootString"] == boot_devices[0]):
                    boot_string = source["BootString"]
                    break
        except KeyError as e:
            msg = "get_persistent_boot_device failed with the KeyError:%s"
            raise exception.IloError((msg) % e)

        if 'iLO Virtual CD-ROM' in boot_string:
            return 'CDROM'

        elif ('NIC' in boot_string or
              'PXE' in boot_string or
              "iSCSI" in boot_string):
            return 'NETWORK'

        elif common.isDisk(boot_string):
            return 'HDD'

        else:
            return None

    def get_http_boot_url(self):
        """Request the http boot url from system in uefi boot mode.

        :returns: URL for http boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._is_boot_mode_uefi() is True):
            sushy_system = self._get_sushy_system('1')
            bios_settings = sushy_system.bios_settings
            return bios_settings.json['Attributes']['UefiShellStartupUrl']
        else:
            msg = 'get_http_boot_url is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)
