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
from sushy import utils

from proliantutils import exception
from proliantutils.ilo import firmware_controller
from proliantutils.ilo import operations
from proliantutils import log
from proliantutils.redfish import main
from proliantutils.redfish.resources.manager import constants as mgr_cons
from proliantutils.redfish.resources.system import constants as sys_cons

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
# Assuming only one sushy_system and sushy_manager present as part of
# collection, as we are dealing with iLO's here.
PROLIANT_MANAGER_ID = '1'
PROLIANT_SYSTEM_ID = '1'

BOOT_OPTION_MAP = {'BOOT_ONCE': True,
                   'BOOT_ALWAYS': False,
                   'NO_BOOT': False}

VIRTUAL_MEDIA_MAP = {'FLOPPY': mgr_cons.VIRTUAL_MEDIA_FLOPPY,
                     'CDROM': mgr_cons.VIRTUAL_MEDIA_CD}

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

        try:
            self._sushy = main.HPESushy(
                address, username=username, password=password,
                root_prefix=root_prefix, verify=verify)
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

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        return sushy_system.json.get('Model')

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
                      {'url': vmedia_device.image_url, 'device': device})
            vmedia_device.eject_vmedia()
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
                vmedia_device.eject_vmedia()

            LOG.debug(self._("Inserting the image url '%(url)s' to the "
                             "device %(device)s.") %
                      {'url': url, 'device': device})
            vmedia_device.insert_vmedia(url)
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
                          "persistent boot device.' Error %(error)s") %
                   {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

    def get_server_capabilities(self):
        """Returns the server capabilities"""

        capabilities = {}
        capabilities.update(self._get_number_of_gpu_devices_connected())
        capabilities.update(self._get_sriov_enabled())
        return capabilities

    def _get_sriov_enabled(self):
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            return {'sriov_enabled': sushy_system.bios_settings.sriov_enabled}
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is unable to get "
                          "Sriov attribute. Error %(error)s)")
                   % {'error': str(e)})
            LOG.debug(msg)

    def _get_number_of_gpu_devices_connected(self):
        """Gets the number of GPU devices connected"""
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            count = sushy_system.pci_devices.gpu_devices
        except sushy.exceptions.SushyError as e:
            msg = (self._("The Redfish controller is unable to get "
                          "PCIDevice resource or its members. Error"
                          "%(error)s)") % {'error': str(e)})
            LOG.debug(msg)
        return {'pci_gpu_devices': count}
