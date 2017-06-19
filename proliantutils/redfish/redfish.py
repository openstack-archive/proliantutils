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
from proliantutils.redfish import main
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

DEVICE_COMMON_TO_REDFISH = {
    'NETWORK': sys_cons.BOOT_SOURCE_TARGET_PXE,
    'HDD': sys_cons.BOOT_SOURCE_TARGET_HDD,
    'CDROM': sys_cons.BOOT_SOURCE_TARGET_CD,
    'ISCSI': sys_cons.BOOT_SOURCE_TARGET_UEFI_TARGET
}

DEVICE_REDFISH_TO_COMMON = {v: k for k, v in DEVICE_COMMON_TO_REDFISH.items()}

POWER_RESET_MAP = {
    'ON': sushy.RESET_ON,
    'OFF': sushy.RESET_FORCE_OFF,
}

# Assuming only one sushy_system present as part of collection,
# as we are dealing with iLO's here.
PROLIANT_SYSTEM_ID = '1'

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

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode of the server.

        Gets the boot mode to be set on next reset.
        :returns: either LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        bios_settings = sushy_system.bios_settings
        boot_mode = bios_settings.BootMode
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        return boot_mode.upper()

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
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)

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
        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        try:
            # Return boot device if it is persistent.
            if sushy_system.boot['enabled'] == 'Continuous':
                device = sushy_system.boot['target']
                if device in BOOT_DEVICE_MAP_REV:
                    return BOOT_DEVICE_MAP_REV[device]
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

    def _update_persistent_boot(self, device_type=[], persistent=False,
                                mac=None):
        """Changes the persistent boot device order in BIOS boot mode for host

        Note: It uses first boot device from the device_type and ignores rest.

        :param device_type: ordered list of boot devices
        :param persistent: Boolean flag to indicate if the device to be set as
                           a persistent boot device
        :param mac: intiator mac address, mandotory for iSCSI uefi boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        if persistent:
            tenure = 'Continuous'
        else:
            tenure = 'Once'

        new_device = device_type[0]
        if device_type[0].upper() in DEVICE_COMMON_TO_REDFISH:
            new_device = DEVICE_COMMON_TO_REDFISH[device_type[0].upper()]

        sushy_system = self._get_sushy_system(PROLIANT_SYSTEM_ID)
        boot_settings = sushy_system.bios_boot_settings
        systems_uri = sushy_system.system_odataid
        # Need to set this option first if device is 'UefiTarget'
        if new_device is 'UefiTarget':
            if not mac:
                msg = ('Mac is needed for iscsi uefi boot')
                raise exception.IloInvalidInputError(msg)
            # Get the Boot resource and Mappings resource.
            structured_boot_string = None
            for boot_setting in boot_settings.BootSources:
                if(mac.upper() in boot_setting['UEFIDevicePath'] and
                   'iSCSI' in boot_setting['UEFIDevicePath']):
                    structured_boot_string = boot_setting[
                        'StructuredBootString']
                    break
            if not structured_boot_string:
                msg = ('MAC provided is Invalid "%s"' % mac)
                raise exception.IloInvalidInputError(msg)

            new_boot_settings = {}
            new_boot_settings['Boot'] = {'UefiTargetBootSourceOverride':
                                         structured_boot_string}
            sushy_system._change_system_settings(systems_uri,
                                                 new_boot_settings)

        new_boot_settings = {}
        new_boot_settings['Boot'] = {'BootSourceOverrideEnabled': tenure,
                                     'BootSourceOverrideTarget': new_device}
        sushy_system._change_system_settings(systems_uri, new_boot_settings)

    def update_persistent_boot(self, device_type=[], mac=None):
        """Changes the persistent boot device order for the host

        :param device_type: ordered list of boot devices
        :param mac: intiator mac address, mandatory for iSCSI uefi boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        import pdb
        pdb.set_trace()
        # Check if the input is valid
        for item in device_type:
            if item.upper() not in DEVICE_COMMON_TO_REDFISH:
                raise exception.IloInvalidInputError("Invalid input. Valid "
                                                     "devices: NETWORK, HDD,"
                                                     " ISCSI or CDROM.")
        self._update_persistent_boot(device_type, persistent=True, mac=mac)
