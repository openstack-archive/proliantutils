# Copyright 2018 Hewlett Packard Enterprise Development LP
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

import json

from six.moves.urllib import parse
import sushy
from sushy import auth
from sushy.resources.system import mappings as sushy_map
from sushy import utils

from proliantutils import exception
from proliantutils.ilo import common as common
from proliantutils.ilo import constants as ilo_cons
from proliantutils.ilo import firmware_controller
from proliantutils.ilo import operations
from proliantutils import log
from proliantutils.redfish import main
from proliantutils.redfish.resources.manager import constants as mgr_cons
from proliantutils.redfish.resources.system import constants as sys_cons
from proliantutils.redfish.resources.system.storage \
    import common as common_storage
from proliantutils.redfish import utils as rf_utils
from proliantutils import utils as common_utils

"""
Class specific for Redfish APIs.
"""

GET_POWER_STATE_MAP = {
    sushy.SYSTEM_POWER_STATE_ON: 'ON',
    sushy.SYSTEM_POWER_STATE_POWERING_ON: 'ON',
    sushy.SYSTEM_POWER_STATE_OFF: 'OFF',
    sushy.SYSTEM_POWER_STATE_POWERING_OFF: 'OFF'
}

POWER_RESET_MAP = {
    'ON': sushy.RESET_ON,
    'OFF': sushy.RESET_FORCE_OFF,
}

DEVICE_COMMON_TO_REDFISH = {
    'NETWORK': sushy.BOOT_SOURCE_TARGET_PXE,
    'HDD': sushy.BOOT_SOURCE_TARGET_HDD,
    'CDROM': sushy.BOOT_SOURCE_TARGET_CD,
    'ISCSI': sushy.BOOT_SOURCE_TARGET_UEFI_TARGET,
    'NONE': sushy.BOOT_SOURCE_TARGET_NONE
}

DEVICE_REDFISH_TO_COMMON = {v: k for k, v in DEVICE_COMMON_TO_REDFISH.items()}

BOOT_MODE_MAP = {
    sys_cons.BIOS_BOOT_MODE_LEGACY_BIOS: 'LEGACY',
    sys_cons.BIOS_BOOT_MODE_UEFI: 'UEFI'
}

BOOT_MODE_MAP_REV = (
    utils.revert_dictionary(BOOT_MODE_MAP))

PERSISTENT_BOOT_MAP = {
    sushy.BOOT_SOURCE_TARGET_PXE: 'NETWORK',
    sushy.BOOT_SOURCE_TARGET_HDD: 'HDD',
    sushy.BOOT_SOURCE_TARGET_CD: 'CDROM',
    sushy.BOOT_SOURCE_TARGET_UEFI_TARGET: 'NETWORK',
    sushy.BOOT_SOURCE_TARGET_NONE: 'NONE'
}

GET_SECUREBOOT_CURRENT_BOOT_MAP = {
    sys_cons.SECUREBOOT_CURRENT_BOOT_ENABLED: True,
    sys_cons.SECUREBOOT_CURRENT_BOOT_DISABLED: False
}

GET_POST_STATE_MAP = {
    sys_cons.POST_STATE_NULL: 'Null',
    sys_cons.POST_STATE_UNKNOWN: 'Unknown',
    sys_cons.POST_STATE_RESET: 'Reset',
    sys_cons.POST_STATE_POWEROFF: 'PowerOff',
    sys_cons.POST_STATE_INPOST: 'InPost',
    sys_cons.POST_STATE_INPOSTDISCOVERY: 'InPostDiscoveryComplete',
    sys_cons.POST_STATE_FINISHEDPOST: 'FinishedPost'
}

# Assuming only one system and one manager present as part of
# collection, as we are dealing with iLO's here.
PROLIANT_MANAGER_ID = '1'
PROLIANT_SYSTEM_ID = '1'

BOOT_OPTION_MAP = {'BOOT_ONCE': True,
                   'BOOT_ALWAYS': False,
                   'NO_BOOT': False}

VIRTUAL_MEDIA_MAP = {'FLOPPY': mgr_cons.VIRTUAL_MEDIA_FLOPPY,
                     'CDROM': mgr_cons.VIRTUAL_MEDIA_CD}

SUPPORTED_BOOT_MODE_MAP = {
    sys_cons.SUPPORTED_LEGACY_BIOS_ONLY: (
        ilo_cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY),
    sys_cons.SUPPORTED_UEFI_ONLY: ilo_cons.SUPPORTED_BOOT_MODE_UEFI_ONLY,
    sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI: (
        ilo_cons.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI)
}

LOG = log.get_logger(__name__)


class RedfishOperations(operations.IloOperations):
    """Operations supported on redfish based hardware.

    This class holds APIs which are currently supported via Redfish mode
    of operation. This is a growing list which needs to be updated as and when
    the existing API/s (of its cousin RIS and RIBCL interfaces) are migrated.
    For operations currently supported on the client object, please refer:
    *proliantutils.ilo.client.SUPPORTED_REDFISH_METHODS*
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
        self._username = username
        self._password = password

        try:
            basic_auth = auth.BasicAuth(username=username, password=password)
            self._sushy = main.HPESushy(
                address, root_prefix=root_prefix, verify=verify,
                auth=basic_auth)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller at "%(controller)s" has '
                          'thrown error. Error %(error)s') %
                   {'controller': address, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloConnectionError(msg)

    def _get_sushy_system(self, system_id):
        """Get the sushy system for system_id

        :param system_id: The identity of the System resource
        :returns: the Sushy system instance
        :raises: IloError
        """
        system_url = parse.urljoin(self._sushy.get_system_collection_path(),
                                   system_id)
        try:
            return self._sushy.get_system(system_url)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish System "%(system)s" was not found. '
                          'Error %(error)s') %
                   {'system': system_id, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def _get_sushy_manager(self, manager_id):
        """Get the sushy Manager for manager_id

        :param manager_id: The identity of the Manager resource
        :returns: the Sushy Manager instance
        :raises: IloError
        """
        manager_url = parse.urljoin(self._sushy.get_manager_collection_path(),
                                    manager_id)
        try:
            return self._sushy.get_manager(manager_url)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish Manager "%(manager)s" was not found. '
                          'Error %(error)s') %
                   {'manager': manager_id, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def _get_sushy_session(self):
        """Get the sushy Manager for manager_id

        :param manager_id: The identity of the Manager resource
        :returns: the Sushy Manager instance
        :raises: IloError
        """
        try:
            return self._sushy.get_session_service()
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish SessionService was not found. '
                          'Error %(error)s') % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        return sushy_system.model

    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        return GET_POWER_STATE_MAP.get(sushy_system.power_state)

    def reset_server(self):
        """Resets the server.

        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            sushy_system.reset_system(sushy.RESET_FORCE_RESTART)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to reset server. '
                          'Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def set_host_power(self, target_value):
        """Sets the power state of the system.

        :param target_value: The target value to be set. Value can be:
            'ON' or 'OFF'.
        :raises: IloError, on an error from iLO.
        :raises: InvalidInputError, if the target value is not
            allowed.
        """
        if target_value not in POWER_RESET_MAP:
            msg = ('The parameter "%(parameter)s" value "%(target_value)s" is '
                   'invalid. Valid values are: %(valid_power_values)s' %
                   {'parameter': 'target_value', 'target_value': target_value,
                    'valid_power_values': POWER_RESET_MAP.keys()})
            raise exception.InvalidInputError(msg)

        # Check current power status, do not act if it's in requested state.
        current_power_status = self.get_host_power_status()
        if current_power_status == target_value:
            LOG.debug(self._("Node is already in '%(target_value)s' power "
                             "state."), {'target_value': target_value})
            return

        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            sushy_system.reset_system(POWER_RESET_MAP[target_value])
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to set power state '
                          'of server to %(target_value)s. Error %(error)s') %
                   {'target_value': target_value, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button.

        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            sushy_system.push_power_button(sys_cons.PUSH_POWER_BUTTON_PRESS)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to press power button'
                          ' of server. Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button.

        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            sushy_system.push_power_button(
                sys_cons.PUSH_POWER_BUTTON_PRESS_AND_HOLD)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to press and hold '
                          'power button of server. Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def activate_license(self, key):
        """Activates iLO license.

        :param key: iLO license key.
        :raises: IloError, on an error from iLO.
        """
        sushy_manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        try:
            sushy_manager.set_license(key)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to update '
                          'the license. Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot.

        :returns: Returns boot device that would be used in next
                  boot. Returns 'Normal' if no device is set.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        if (sushy_system.boot.enabled == sushy.BOOT_SOURCE_ENABLED_ONCE):
            return DEVICE_REDFISH_TO_COMMON.get(sushy_system.boot.target)
        else:
            # value returned by RIBCL if one-time boot setting are absent
            return 'Normal'

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode of the server.

        Gets the boot mode to be set on next reset.
        :returns: either LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            return BOOT_MODE_MAP.get(
                sushy_system.bios_settings.pending_settings.boot_mode)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The pending BIOS Settings was not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_current_boot_mode(self):
        """Retrieves the current boot mode of the server.

        :returns: Current boot mode, LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            return BOOT_MODE_MAP.get(sushy_system.bios_settings.boot_mode)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The current BIOS Settings was not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def _validate_virtual_media(self, device):
        """Check if the device is valid device.

        :param device: virtual media device
        :raises: IloInvalidInputError, if the device is not valid.
        """
        if device not in VIRTUAL_MEDIA_MAP:
            msg = (self._("Invalid device '%s'. Valid devices: FLOPPY or "
                          "CDROM.")
                   % device)
            LOG.debug(msg)
            raise exception.IloInvalidInputError(msg)

    def eject_virtual_media(self, device):
        """Ejects the Virtual Media image if one is inserted.

        :param device: virual media device
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the device is not valid.
        """
        self._validate_virtual_media(device)
        manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        try:
            vmedia_device = (
                manager.virtual_media.get_member_device(
                    VIRTUAL_MEDIA_MAP[device]))
            if not vmedia_device.inserted:
                LOG.debug(self._("No media available in the device '%s' to "
                                 "perform eject operation.") % device)
                return

            LOG.debug(self._("Ejecting the media image '%(url)s' from the "
                             "device %(device)s.") %
                      {'url': vmedia_device.image, 'device': device})
            vmedia_device.eject_media()
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller failed to eject the virtual"
                          " media device '%(device)s'. Error %(error)s.") %
                   {'device': device, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def insert_virtual_media(self, url, device):
        """Inserts the Virtual Media image to the device.

        :param url: URL to image
        :param device: virual media device
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the device is not valid.
        """
        self._validate_virtual_media(device)
        manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        try:
            vmedia_device = (
                manager.virtual_media.get_member_device(
                    VIRTUAL_MEDIA_MAP[device]))
            if vmedia_device.inserted:
                vmedia_device.eject_media()

            LOG.debug(self._("Inserting the image url '%(url)s' to the "
                             "device %(device)s.") %
                      {'url': url, 'device': device})
            vmedia_device.insert_media(url)
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller failed to insert the media "
                          "url %(url)s in the virtual media device "
                          "'%(device)s'. Error %(error)s.") %
                   {'url': url, 'device': device, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status

        It sets the boot option for virtual media device.
        Note: boot option can be set only for CD device.

        :param device: virual media device
        :param boot_option: boot option to set on the virtual media device
        :param write_protect: set the write protect flag on the vmedia device
                              Note: It's ignored. In Redfish it is read-only.
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the device is not valid.
        """
        # CONNECT is a RIBCL call. There is no such property to set in Redfish.
        if boot_option == 'CONNECT':
            return

        self._validate_virtual_media(device)

        if boot_option not in BOOT_OPTION_MAP:
            msg = (self._("Virtual media boot option '%s' is invalid.")
                   % boot_option)
            LOG.debug(msg)
            raise exception.IloInvalidInputError(msg)

        manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        try:
            vmedia_device = (
                manager.virtual_media.get_member_device(
                    VIRTUAL_MEDIA_MAP[device]))
            vmedia_device.set_vm_status(BOOT_OPTION_MAP[boot_option])
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller failed to set the virtual "
                          "media status for '%(device)s'. Error %(error)s") %
                   {'device': device, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    @firmware_controller.check_firmware_update_component
    def update_firmware(self, file_url, component_type):
        """Updates the given firmware on the server for the given component.

        :param file_url: location of the raw firmware file. Extraction of the
                         firmware file (if in compact format) is expected to
                         happen prior to this invocation.
        :param component_type: Type of component to be applied to.
        :raises: IloError, on an error from iLO.
        """
        try:
            update_service_inst = self._sushy.get_update_service()
            update_service_inst.flash_firmware(self, file_url)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to update firmware '
                          'with firmware %(file)s Error %(error)s') %
                   {'file': file_url, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def _is_boot_mode_uefi(self):
        """Checks if the system is in uefi boot mode.

        :return: 'True' if the boot mode is uefi else 'False'
        """
        boot_mode = self.get_current_boot_mode()
        return (boot_mode == BOOT_MODE_MAP.get(sys_cons.BIOS_BOOT_MODE_UEFI))

    def get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        # Return boot device if it is persistent.
        if ((sushy_system.
             boot.enabled) == sushy.BOOT_SOURCE_ENABLED_CONTINUOUS):
            return PERSISTENT_BOOT_MAP.get(sushy_system.boot.target)
        # Check if we are in BIOS boot mode.
        # There is no resource to fetch boot device order for BIOS boot mode
        if not self._is_boot_mode_uefi():
            return None

        try:
            boot_device = (sushy_system.bios_settings.boot_settings.
                           get_persistent_boot_device())
            return PERSISTENT_BOOT_MAP.get(boot_device)
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is unable to get "
                          "persistent boot device. Error %(error)s") %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def set_pending_boot_mode(self, boot_mode):
        """Sets the boot mode of the system for next boot.

        :param boot_mode: either 'uefi' or 'legacy'.
        :raises: IloInvalidInputError, on an invalid input.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)

        if boot_mode.upper() not in BOOT_MODE_MAP_REV.keys():
            msg = (('Invalid Boot mode: "%(boot_mode)s" specified, valid boot '
                    'modes are either "uefi" or "legacy"')
                   % {'boot_mode': boot_mode})
            raise exception.IloInvalidInputError(msg)

        try:
            sushy_system.bios_settings.pending_settings.set_pending_boot_mode(
                BOOT_MODE_MAP_REV.get(boot_mode.upper()))
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to set '
                          'pending boot mode to %(boot_mode)s. '
                          'Error: %(error)s') %
                   {'boot_mode': boot_mode, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def update_persistent_boot(self, devices=[]):
        """Changes the persistent boot device order for the host

        :param devices: ordered list of boot devices
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the given input is not valid.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        # Check if the input is valid
        for item in devices:
            if item.upper() not in DEVICE_COMMON_TO_REDFISH:
                msg = (self._('Invalid input "%(device)s". Valid devices: '
                              'NETWORK, HDD, ISCSI or CDROM.') %
                       {'device': item})
                raise exception.IloInvalidInputError(msg)

        try:
            sushy_system.update_persistent_boot(
                devices, persistent=True)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to update '
                          'persistent boot device %(devices)s.'
                          'Error: %(error)s') %
                   {'devices': devices, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def set_one_time_boot(self, device):
        """Configures a single boot from a specific device.

        :param device: Device to be set as a one time boot device
        :raises: IloError, on an error from iLO.
        :raises: IloInvalidInputError, if the given input is not valid.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        # Check if the input is valid
        if device.upper() not in DEVICE_COMMON_TO_REDFISH:
            msg = (self._('Invalid input "%(device)s". Valid devices: '
                          'NETWORK, HDD, ISCSI or CDROM.') %
                   {'device': device})
            raise exception.IloInvalidInputError(msg)

        try:
            sushy_system.update_persistent_boot(
                [device], persistent=False)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to set '
                          'one time boot device %(device)s. '
                          'Error: %(error)s') %
                   {'device': device, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        """
        try:
            acc_service = self._sushy.get_account_service()
            member = acc_service.accounts.get_member_details(self._username)
            if member is None:
                msg = (self._("No account found with username: %s")
                       % self._username)
                LOG.debug(msg)
                raise exception.IloError(msg)
            member.update_credentials(password)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to update '
                          'credentials for %(username)s. Error %(error)s') %
                   {'username': self._username, 'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_supported_boot_mode(self):
        """Get the system supported boot modes.

        :return: any one of the following proliantutils.ilo.constants:

            SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY,
            SUPPORTED_BOOT_MODE_UEFI_ONLY,
            SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI
        :raises: IloError, if account not found or on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            return SUPPORTED_BOOT_MODE_MAP.get(
                sushy_system.supported_boot_mode)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to get the '
                          'supported boot modes. Error: %s') % e)
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_server_capabilities(self):
        """Returns the server capabilities

        raises: IloError on an error from iLO.
        """
        capabilities = {}

        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        sushy_manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        try:
            count = len(sushy_system.pci_devices.gpu_devices)
            boot_mode = rf_utils.get_supported_boot_mode(
                sushy_system.supported_boot_mode)
            capabilities.update(
                {'pci_gpu_devices': count,
                 'ilo_firmware_version': sushy_manager.firmware_version,
                 'rom_firmware_version': sushy_system.rom_version,
                 'server_model': sushy_system.model,
                 'nic_capacity': sushy_system.pci_devices.max_nic_capacity,
                 'boot_mode_bios': boot_mode.boot_mode_bios,
                 'boot_mode_uefi': boot_mode.boot_mode_uefi})

            tpm_state = sushy_system.bios_settings.tpm_state
            all_key_to_value_expression_tuples = [
                ('sriov_enabled',
                 sushy_system.bios_settings.sriov == sys_cons.SRIOV_ENABLED),
                ('cpu_vt',
                 sushy_system.bios_settings.cpu_vt == (
                     sys_cons.CPUVT_ENABLED)),
                ('trusted_boot',
                 (tpm_state == sys_cons.TPM_PRESENT_ENABLED
                  or tpm_state == sys_cons.TPM_PRESENT_DISABLED)),
                ('secure_boot', self._has_secure_boot()),
                ('iscsi_boot',
                 (sushy_system.bios_settings.iscsi_resource.
                  is_iscsi_boot_supported())),
                ('hardware_supports_raid',
                 len(sushy_system.smart_storage.array_controllers.
                     members_identities) > 0),
                ('has_ssd',
                 common_storage.has_ssd(sushy_system)),
                ('has_rotational',
                 common_storage.has_rotational(sushy_system)),
                ('has_nvme_ssd',
                 common_storage.has_nvme_ssd(sushy_system))
                ]

            all_key_to_value_expression_tuples += (
                [('logical_raid_level_' + x, True)
                 for x in sushy_system.smart_storage.logical_raid_levels])

            all_key_to_value_expression_tuples += (
                [('drive_rotational_' + str(x) + '_rpm', True)
                 for x in
                 common_storage.get_drive_rotational_speed_rpm(sushy_system)])

            capabilities.update(
                {key: 'true'
                 for (key, value) in all_key_to_value_expression_tuples
                 if value})

            memory_data = sushy_system.memory.details()

            if memory_data.has_nvdimm_n:
                capabilities.update(
                    {'persistent_memory': (
                     json.dumps(memory_data.has_persistent_memory)),
                     'nvdimm_n': (
                     json.dumps(memory_data.has_nvdimm_n)),
                     'logical_nvdimm_n': (
                     json.dumps(memory_data.has_logical_nvdimm_n))})

        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is unable to get "
                          "resource or its members. Error "
                          "%(error)s)") % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
        return capabilities

    def reset_bios_to_default(self):
        """Resets the BIOS settings to default values.

        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            sushy_system.bios_settings.update_bios_to_default()
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is unable to update bios "
                          "settings to default Error %(error)s") %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_secure_boot_mode(self):
        """Get the status of secure boot.

        :returns: True, if enabled, else False
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            secure_boot_enabled = GET_SECUREBOOT_CURRENT_BOOT_MAP.get(
                sushy_system.secure_boot.current_boot)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to provide '
                          'information about secure boot on the server. '
                          'Error: %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloCommandNotSupportedError(msg)

        if secure_boot_enabled:
            LOG.debug(self._("Secure boot is Enabled"))
        else:
            LOG.debug(self._("Secure boot is Disabled"))
        return secure_boot_enabled

    def _has_secure_boot(self):
        try:
            self._get_sushy_system(PROLIANT_SYSTEM_ID).secure_boot
        except (exception.MissingAttributeError, sushy.exceptions.SushyError):
            return False
        return True

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server.

        Resetting the server post updating this settings is needed
        from the caller side to make this into effect.
        :param secure_boot_enable: True, if secure boot needs to be
               enabled for next boot, else False.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
            try:
                sushy_system.secure_boot.enable_secure_boot(secure_boot_enable)
            except exception.InvalidInputError as e:
                msg = (self._('Invalid input. Error %(error)s')
                       % {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
            except sushy.exceptions.SushyError as e:
                msg = (self._('The Redfish controller failed to set secure '
                              'boot settings on the server. Error: %(error)s')
                       % {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
        else:
            msg = (self._('System is not in UEFI boot mode. "SecureBoot" '
                          'related resources cannot be changed.'))
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def reset_secure_boot_keys(self):
        """Reset secure boot keys to manufacturing defaults.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
            try:
                sushy_system.secure_boot.reset_keys(
                    sys_cons.SECUREBOOT_RESET_KEYS_DEFAULT)
            except sushy.exceptions.SushyError as e:
                msg = (self._('The Redfish controller failed to reset secure '
                              'boot keys on the server. Error %(error)s')
                       % {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
        else:
            msg = (self._('System is not in UEFI boot mode. "SecureBoot" '
                          'related resources cannot be changed.'))
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def clear_secure_boot_keys(self):
        """Reset all keys.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if self._is_boot_mode_uefi():
            sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
            try:
                sushy_system.secure_boot.reset_keys(
                    sys_cons.SECUREBOOT_RESET_KEYS_DELETE_ALL)
            except sushy.exceptions.SushyError as e:
                msg = (self._('The Redfish controller failed to clear secure '
                              'boot keys on the server. Error %(error)s')
                       % {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
        else:
            msg = (self._('System is not in UEFI boot mode. "SecureBoot" '
                          'related resources cannot be changed.'))
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def get_essential_properties(self):
        """Constructs the dictionary of essential properties

        Constructs the dictionary of essential properties, named
        cpu, cpu_arch, local_gb, memory_mb. The MACs are also returned
        as part of this method.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            # TODO(nisha): Add local_gb here and return after
            # local_gb changes are merged.
            # local_gb = sushy_system.storage_summary
            prop = {'memory_mb': (sushy_system.memory_summary.size_gib * 1024),
                    'cpus': sushy_system.processors.summary.count,
                    'cpu_arch': sushy_map.PROCESSOR_ARCH_VALUE_MAP_REV.get(
                    sushy_system.processors.summary.architecture),
                    'local_gb': common_storage.get_local_gb(sushy_system)}
            return {'properties': prop,
                    'macs': sushy_system.ethernet_interfaces.summary}
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to get the '
                          'resource data. Error %(error)s')
                   % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def _change_iscsi_target_settings(self, iscsi_info):
        """Change iSCSI target settings.

        :param iscsi_info: A dictionary that contains information of iSCSI
                           target like target_name, lun, ip_address, port etc.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            pci_settings_map = (
                sushy_system.bios_settings.bios_mappings.pci_settings_mappings)
            nics = []
            for mapping in pci_settings_map:
                for subinstance in mapping['Subinstances']:
                    for association in subinstance['Associations']:
                        if 'NicBoot' in association:
                            nics.append(association)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to get the '
                          'bios mappings. Error %(error)s')
                   % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

        if not nics:
            msg = ('No nics were found on the system')
            raise exception.IloError(msg)

        # Set iSCSI info to all nics
        iscsi_infos = []
        for nic in nics:
            data = iscsi_info.copy()
            data['iSCSIAttemptName'] = nic
            data['iSCSINicSource'] = nic
            data['iSCSIAttemptInstance'] = nics.index(nic) + 1
            iscsi_infos.append(data)

        iscsi_data = {'iSCSISources': iscsi_infos}
        try:
            (sushy_system.bios_settings.iscsi_resource.
             iscsi_settings.update_iscsi_settings(iscsi_data))
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is failed to update iSCSI "
                          "settings. Error %(error)s") %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def set_iscsi_info(self, target_name, lun, ip_address,
                       port='3260', auth_method=None, username=None,
                       password=None):
        """Set iSCSI details of the system in UEFI boot mode.

        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param target_name: Target Name for iSCSI.
        :param lun: logical unit number.
        :param ip_address: IP address of the target.
        :param port: port of the target.
        :param auth_method : either None or CHAP.
        :param username: CHAP Username for authentication.
        :param password: CHAP secret.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._is_boot_mode_uefi()):
            iscsi_info = {}
            iscsi_info['iSCSITargetName'] = target_name
            iscsi_info['iSCSILUN'] = lun
            iscsi_info['iSCSITargetIpAddress'] = ip_address
            iscsi_info['iSCSITargetTcpPort'] = int(port)
            iscsi_info['iSCSITargetInfoViaDHCP'] = False
            iscsi_info['iSCSIConnection'] = 'Enabled'
            if (auth_method == 'CHAP'):
                iscsi_info['iSCSIAuthenticationMethod'] = 'Chap'
                iscsi_info['iSCSIChapUsername'] = username
                iscsi_info['iSCSIChapSecret'] = password
            self._change_iscsi_target_settings(iscsi_info)
        else:
            msg = 'iSCSI boot is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def unset_iscsi_info(self):
        """Disable iSCSI boot option in UEFI boot mode.

        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the BIOS boot mode.
        """
        if(self._is_boot_mode_uefi()):
            iscsi_info = {'iSCSIConnection': 'Disabled'}
            self._change_iscsi_target_settings(iscsi_info)
        else:
            msg = 'iSCSI boot is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def set_iscsi_initiator_info(self, initiator_iqn):
        """Set iSCSI initiator information in iLO.

        :param initiator_iqn: Initiator iqn for iLO.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the BIOS boot mode.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        if(self._is_boot_mode_uefi()):
            iscsi_data = {'iSCSIInitiatorName': initiator_iqn}
            try:
                (sushy_system.bios_settings.iscsi_resource.
                 iscsi_settings.update_iscsi_settings(iscsi_data))
            except sushy.exceptions.SushyError as e:
                msg = (self._("The Redfish controller has failed to update "
                              "iSCSI settings. Error %(error)s") %
                       {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
        else:
            msg = 'iSCSI initiator cannot be updated in BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def get_iscsi_initiator_info(self):
        """Give iSCSI initiator information of iLO.

        :returns: iSCSI initiator information.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the BIOS boot mode.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        if(self._is_boot_mode_uefi()):
            try:
                iscsi_initiator = (
                    sushy_system.bios_settings.iscsi_resource.iscsi_initiator)
            except sushy.exceptions.SushyError as e:
                msg = (self._('The Redfish controller has failed to get the '
                              'iSCSI initiator. Error %(error)s')
                       % {'error': str(e)})
                LOG.debug(msg)
                raise exception.IloError(msg)
            return iscsi_initiator
        else:
            msg = 'iSCSI initiator cannot be retrieved in BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def inject_nmi(self):
        """Inject NMI, Non Maskable Interrupt.

        Inject NMI (Non Maskable Interrupt) for a node immediately.

        :raises: IloError, on an error from iLO
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        if sushy_system.power_state != sushy.SYSTEM_POWER_STATE_ON:
            raise exception.IloError("Server is not in powered on state.")

        try:
            sushy_system.reset_system(sushy.RESET_NMI)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The Redfish controller failed to inject nmi to '
                          'server. Error %(error)s') % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_host_post_state(self):
        """Get the current state of system POST.

        Retrieves current state of system POST.

        :returns: POST state of the server. The valida states are:-
                  null, Unknown, Reset, PowerOff, InPost,
                  InPostDiscoveryComplete and FinishedPost.
        :raises: IloError, on an error from iLO
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        return GET_POST_STATE_MAP.get(sushy_system.post_state)

    def read_raid_configuration(self, raid_config=None):
        """Read the logical drives from the system

        :param raid_config: None in case of post-delete read or in case of
                            post-create a dictionary containing target raid
                            configuration data. This data stucture should be as
                            follows:
                            raid_config = {'logical_disks': [{'raid_level': 1,
                            'size_gb': 100, 'physical_disks': ['6I:1:5'],
                            'controller': 'HPE Smart Array P408i-a SR Gen10'},
                            <info-for-logical-disk-2>]}
        :raises: IloError, on an error from iLO.
        :returns: A dictionary containing list of logical disks
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        return sushy_system.read_raid(raid_config=raid_config)

    def delete_raid_configuration(self):
        """Delete the raid configuration on the hardware."""
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        sushy_system.delete_raid()

    def get_current_bios_settings(self, only_allowed_settings=True):
        """Get current BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be returned. If False, All the BIOS settings supported
                by iLO are returned.
        :return: a dictionary of current BIOS settings is returned. Depending
                 on the 'only_allowed_settings', either only the allowed
                 settings are returned or all the supported settings are
                 returned.
        :raises: IloError, on an error from iLO
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            current_settings = sushy_system.bios_settings.json
        except sushy.exceptions.SushyError as e:
            msg = (self._('The current BIOS Settings were not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

        attributes = current_settings.get("Attributes")
        if only_allowed_settings and attributes:
            return common_utils.apply_bios_properties_filter(
                attributes, ilo_cons.SUPPORTED_REDFISH_BIOS_PROPERTIES)
        return attributes

    def get_pending_bios_settings(self, only_allowed_settings=True):
        """Get pending BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings are
                to be returned. If False, All the BIOS settings supported by
                iLO are returned.
        :return: a dictionary of pending BIOS settings is returned. Depending
                 on the 'only_allowed_settings', either only the allowed
                 settings are returned or all the supported settings are
                 returned.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            settings = sushy_system.bios_settings.pending_settings.json
        except sushy.exceptions.SushyError as e:
            msg = (self._('The pending BIOS Settings were not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

        attributes = settings.get("Attributes")
        if only_allowed_settings and attributes:
            return common_utils.apply_bios_properties_filter(
                attributes, ilo_cons.SUPPORTED_REDFISH_BIOS_PROPERTIES)
        return attributes

    def set_bios_settings(self, data=None, only_allowed_settings=True):
        """Sets current BIOS settings to the provided data.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be set. If False, all the BIOS settings supported by
                iLO and present in the 'data' are set.
        :param: data: a dictionary of BIOS settings to be applied. Depending
                on the 'only_allowed_settings', either only the allowed
                settings are set or all the supported settings that are in the
                'data' are set.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if not data:
            raise exception.IloError("Could not apply settings with"
                                     " empty data")

        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        if only_allowed_settings:
            unsupported_settings = [key for key in data if key not in (
                ilo_cons.SUPPORTED_REDFISH_BIOS_PROPERTIES)]
            if unsupported_settings:
                msg = ("Could not apply settings as one or more settings are"
                       " not supported. Unsupported settings are %s."
                       " Supported settings are %s." % (
                           unsupported_settings,
                           ilo_cons.SUPPORTED_REDFISH_BIOS_PROPERTIES))
                raise exception.IloError(msg)
        try:
            settings_required = sushy_system.bios_settings.pending_settings
            settings_required.update_bios_data_by_patch(data)
        except sushy.exceptions.SushyError as e:
            msg = (self._('The pending BIOS Settings resource not found.'
                          ' Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_default_bios_settings(self, only_allowed_settings=True):
        """Get default BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be returned. If False, All the BIOS settings supported
                by iLO are returned.
        :return: a dictionary of default BIOS settings(factory settings).
                 Depending on the 'only_allowed_settings', either only the
                 allowed settings are returned or all the supported settings
                 are returned.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            settings = sushy_system.bios_settings.default_settings
        except sushy.exceptions.SushyError as e:
            msg = (self._('The default BIOS Settings were not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
        if only_allowed_settings:
            return common_utils.apply_bios_properties_filter(
                settings, ilo_cons.SUPPORTED_REDFISH_BIOS_PROPERTIES)
        return settings

    def create_raid_configuration(self, raid_config):
        """Create the raid configuration on the hardware.

        Based on user raid_config input, it will create raid

        :param raid_config: A dictionary containing target raid configuration
                            data. This data stucture should be as follows:
                            raid_config = {'logical_disks': [{'raid_level': 1,
                            'size_gb': 100, 'physical_disks': ['6I:1:5'],
                            'controller': 'HPE Smart Array P408i-a SR Gen10'},
                            <info-for-logical-disk-2>]}
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        sushy_system.create_raid(raid_config)

    def get_bios_settings_result(self):
        """Gets the result of the bios settings applied

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            settings_result = sushy_system.bios_settings.messages
        except sushy.exceptions.SushyError as e:
            msg = (self._('The BIOS Settings results were not found. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
        status = "failed" if len(settings_result) > 1 else "success"
        return {"status": status, "results": settings_result}

    def get_ilo_firmware_version_as_major_minor(self):
        """Gets iLO firmware version string in major minor release combination.

        :raises: IloError, on an error from iLO.
        :returns iLO firmware major minor release combination as a string.
        """
        sushy_manager = self._get_sushy_manager(PROLIANT_MANAGER_ID)
        ilo_fw_str = sushy_manager.firmware_version
        major_minor = common.get_major_minor(ilo_fw_str)
        return major_minor

    def create_session(self):
        """Create a session.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server.
        """
        sushy_session = self._get_sushy_session()
        try:
            (key, uri) = sushy_session.create_session(
                self._username, self._password)
            return (key, uri)
        except sushy.exceptions.SushyError as e:
            msg = (self._('Session creation failed. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def close_session(self, session_uri):
        """Closes/Deletes a session.

        :param: session_uri: Tsession URI which is to be deleted.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server.
        """
        sushy_session = self._get_sushy_session()
        try:
            sushy_session.close_session(session_uri)
        except sushy.exceptions.SushyError as e:
            msg = (self._('Session could not be closed. Error '
                          '%(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)
