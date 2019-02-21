# Copyright 2018 Hewlett-Packard Development Company, L.P.
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

import netaddr
from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import ipmi
from proliantutils.ilo import operations
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.ilo.snmp import snmp_cpqdisk_sizes as snmp
from proliantutils import log
from proliantutils.redfish import redfish

SUPPORTED_RIS_METHODS = [
    'activate_license',
    'clear_secure_boot_keys',
    'create_raid_configuration',
    'delete_raid_configuration',
    'eject_virtual_media',
    'get_bios_settings_result',
    'get_current_bios_settings',
    'get_current_boot_mode',
    'get_host_post_state',
    'get_default_bios_settings',
    'get_host_power_status',
    'get_http_boot_url',
    'get_ilo_firmware_version_as_major_minor',
    'get_one_time_boot',
    'get_pending_bios_settings',
    'get_pending_boot_mode',
    'get_persistent_boot_device',
    'get_product_name',
    'get_secure_boot_mode',
    'get_server_capabilities',
    'get_supported_boot_mode',
    'get_vm_status',
    'hold_pwr_btn',
    'inject_nmi',
    'insert_virtual_media',
    'press_pwr_btn',
    'read_raid_configuration',
    'reset_bios_to_default',
    'reset_ilo_credential',
    'reset_secure_boot_keys',
    'reset_server',
    'set_bios_settings',
    'set_host_power',
    'set_http_boot_url',
    'set_one_time_boot',
    'set_pending_boot_mode',
    'set_secure_boot_mode',
    'set_iscsi_boot_info',
    'set_iscsi_info',
    'unset_iscsi_boot_info',
    'unset_iscsi_info',
    'get_iscsi_initiator_info',
    'set_iscsi_initiator_info',
    'set_vm_status',
    'update_firmware',
    'update_persistent_boot',
    ]

SUPPORTED_REDFISH_METHODS = [
    'create_raid_configuration',
    'delete_raid_configuration',
    'get_product_name',
    'get_host_post_state',
    'get_host_power_status',
    'set_host_power',
    'reset_server',
    'press_pwr_btn',
    'hold_pwr_btn',
    'get_bios_settings_result',
    'get_current_bios_settings',
    'get_default_bios_settings',
    'get_pending_bios_settings',
    'set_bios_settings',
    'get_one_time_boot',
    'get_pending_boot_mode',
    'get_current_boot_mode',
    'activate_license',
    'eject_virtual_media',
    'inject_nmi',
    'insert_virtual_media',
    'set_vm_status',
    'update_firmware',
    'get_persistent_boot_device',
    'set_one_time_boot',
    'update_persistent_boot',
    'set_pending_boot_mode',
    'read_raid_configuration',
    'reset_ilo_credential',
    'reset_bios_to_default',
    'get_secure_boot_mode',
    'set_secure_boot_mode',
    'reset_secure_boot_keys',
    'clear_secure_boot_keys',
    'get_server_capabilities',
    'get_supported_boot_mode',
    'get_essential_properties',
    'set_iscsi_boot_info',
    'set_iscsi_info',
    'unset_iscsi_boot_info',
    'unset_iscsi_info',
    'get_iscsi_initiator_info',
    'set_iscsi_initiator_info'
]

LOG = log.get_logger(__name__)


class IloClient(operations.IloOperations):

    def __init__(self, host, login, password, timeout=60, port=443,
                 bios_password=None, cacert=None, snmp_credentials=None,
                 use_redfish_only=False):

        # IPv6 Check
        # TODO(paresh) Need to test with Global IPv6 address
        # IPMI supports IPv6 without square brackets
        self.ipmi_host_info = {'address': host, 'username': login,
                               'password': password}

        if netaddr.valid_ipv6(host.split('%')[0]):
            host = '[' + host + ']'

        self.ribcl = ribcl.RIBCLOperations(host, login, password, timeout,
                                           port, cacert=cacert)
        self.host = host
        self.use_redfish_only = use_redfish_only

        if use_redfish_only:
            self._init_redfish_object(None, host, login, password,
                                      bios_password=bios_password,
                                      cacert=cacert)
            LOG.debug(self._("Forced to use 'redfish' way to interact "
                             "with iLO. Model: %(model)s"),
                      {'model': self.model})
        else:
            try:
                self.model = self.ribcl.get_product_name()
            except exception.IloError:
                # Note(deray): This can be a potential scenario where
                # RIBCL is disabled on a Gen10 (iLO 5) hardware.
                # So, trying out the redfish operation object instantiation.
                # If that passes we know that our assumption is right.
                # If that errors out, then alas! we are left with no other
                # choice.
                self._init_redfish_object(False, host, login, password,
                                          bios_password=bios_password,
                                          cacert=cacert)
            else:
                self.ribcl.init_model_based_tags(self.model)
                if ('Gen10' in self.model):
                    self._init_redfish_object(True, host, login, password,
                                              bios_password=bios_password,
                                              cacert=cacert,
                                              should_set_model=False)
                else:
                    # Gen9
                    self.ris = ris.RISOperations(
                        host, login, password, bios_password=bios_password,
                        cacert=cacert)

        self.snmp_credentials = snmp_credentials
        self._validate_snmp()
        LOG.debug(self._("IloClient object created. "
                         "Model: %(model)s"), {'model': self.model})

    def _init_redfish_object(self, is_ribcl_enabled, redfish_controller_ip,
                             username, password, bios_password=None,
                             cacert=None, should_set_model=True):
        self.redfish = redfish.RedfishOperations(
            redfish_controller_ip, username, password,
            bios_password=bios_password, cacert=cacert)
        self.is_ribcl_enabled = is_ribcl_enabled
        if should_set_model:
            self.model = self.redfish.get_product_name()

    def _validate_snmp(self):
        """Validates SNMP credentials.

        :raises exception.IloInvalidInputError
        """
        cred = self.snmp_credentials
        if cred is not None:
            if cred.get('snmp_inspection') is True:
                if not all([cred.get('auth_user'),
                           cred.get('auth_prot_pp'),
                           cred.get('auth_priv_pp')]):
                    msg = self._('Either few or all mandatory '
                                 'SNMP credentials '
                                 'are missing.')
                    LOG.error(msg)
                    raise exception.IloInvalidInputError(msg)
                try:
                    auth_protocol = cred['auth_protocol']
                    if auth_protocol not in ["SHA", "MD5"]:
                        msg = self._('Invalid SNMP auth protocol '
                                     'provided. '
                                     'Valid values are SHA or MD5')
                        LOG.error(msg)
                        raise exception.IloInvalidInputError(msg)
                except KeyError:
                    msg = self._('Auth protocol not provided by user. '
                                 'The default value of MD5 will '
                                 'be considered.')
                    LOG.debug(msg)
                    pass
                try:
                    priv_protocol = cred['priv_protocol']
                    if priv_protocol not in ["AES", "DES"]:
                        msg = self._('Invalid SNMP privacy protocol '
                                     'provided. '
                                     'Valid values are AES or DES')
                        LOG.error(msg)
                        raise exception.IloInvalidInputError(msg)
                except KeyError:
                    msg = self._('Privacy protocol not provided '
                                 'by user. '
                                 'The default value of DES will '
                                 'be considered.')
                    LOG.debug(msg)
                    pass
            else:
                LOG.debug(self._('snmp_inspection set to False. SNMP'
                                 'inspection will not be performed.'))
        else:
            LOG.debug(self._('SNMP credentials not provided. SNMP '
                             'inspection will not be performed.'))

    def _call_method(self, method_name, *args, **kwargs):
        """Call the corresponding method using RIBCL, RIS or REDFISH

        Make the decision to invoke the corresponding method using RIBCL,
        RIS or REDFISH way. In case of none, throw out ``NotImplementedError``
        """
        if self.use_redfish_only:
            if method_name in SUPPORTED_REDFISH_METHODS:
                the_operation_object = self.redfish
            else:
                raise NotImplementedError()
        else:
            the_operation_object = self.ribcl
            if 'Gen10' in self.model:
                if method_name in SUPPORTED_REDFISH_METHODS:
                    the_operation_object = self.redfish
                else:
                    if (self.is_ribcl_enabled is not None
                            and not self.is_ribcl_enabled):
                        raise NotImplementedError()
            elif ('Gen9' in self.model) and (method_name in
                                             SUPPORTED_RIS_METHODS):
                the_operation_object = self.ris

        method = getattr(the_operation_object, method_name)

        LOG.debug(self._("Using %(class)s for method %(method)s."),
                  {'class': type(the_operation_object).__name__,
                   'method': method_name})

        return method(*args, **kwargs)

    def get_all_licenses(self):
        """Retrieve license type, key, installation date, etc."""
        return self._call_method('get_all_licenses')

    def get_product_name(self):
        """Get the model name of the queried server."""
        return self._call_method('get_product_name')

    def get_host_power_status(self):
        """Request the power state of the server."""
        return self._call_method('get_host_power_status')

    def get_http_boot_url(self):
        """Request the http boot url.

        :returns: URL for http boot.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('get_http_boot_url')

    def set_http_boot_url(self, url):
        """Set the url to the UefiShellStartupUrl.

        :param url: URL for http boot.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('set_http_boot_url', url)

    def set_iscsi_info(self, target_name, lun, ip_address,
                       port='3260', auth_method=None, username=None,
                       password=None):
        """Set iscsi details of the system in uefi boot mode.

        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param target_name: Target Name for iscsi.
        :param lun: logical unit number.
        :param ip_address: IP address of the target.
        :param port: port of the target.
        :param auth_method : either None or CHAP.
        :param username: CHAP Username for authentication.
        :param password: CHAP secret.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        return self._call_method('set_iscsi_info', target_name, lun,
                                 ip_address, port, auth_method, username,
                                 password)

    def set_iscsi_boot_info(self, mac, target_name, lun, ip_address,
                            port='3260', auth_method=None, username=None,
                            password=None):
        """Set iscsi details of the system in uefi boot mode.

        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param mac: The MAC of the NIC to be set with iSCSI information
        :param target_name: Target Name for iscsi.
        :param lun: logical unit number.
        :param ip_address: IP address of the target.
        :param port: port of the target.
        :param auth_method : either None or CHAP.
        :param username: CHAP Username for authentication.
        :param password: CHAP secret.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        LOG.warning("'set_iscsi_boot_info' is deprecated. The 'MAC' parameter"
                    "passed in is ignored. Use 'set_iscsi_info' instead.")
        return self._call_method('set_iscsi_info', target_name, lun,
                                 ip_address, port, auth_method, username,
                                 password)

    def unset_iscsi_info(self):
        """Disable iscsi boot option of the system in uefi boot mode.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        return self._call_method('unset_iscsi_info')

    def unset_iscsi_boot_info(self, mac):
        """Disable iscsi boot option of the system in uefi boot mode.

        :param mac: The MAC of the NIC to be set with iSCSI information.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        LOG.warning("'unset_iscsi_boot_info' is deprecated. The 'MAC' "
                    "parameter passed in is ignored. Use 'unset_iscsi_info' "
                    "instead.")
        return self._call_method('unset_iscsi_info')

    def get_iscsi_initiator_info(self):
        """Returns iSCSI initiator information of iLO.

        :returns: iSCSI initiator information.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        return self._call_method('get_iscsi_initiator_info')

    def set_iscsi_initiator_info(self, initiator_iqn):
        """Set iSCSI initiator information in iLO.

        :param initiator_iqn: Initiator iqn for iLO.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        return self._call_method('set_iscsi_initiator_info', initiator_iqn)

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot."""
        return self._call_method('get_one_time_boot')

    def get_vm_status(self, device='FLOPPY'):
        """Returns the virtual media drive status like url, is connected, etc.

        """
        return self._call_method('get_vm_status', device)

    def reset_server(self):
        """Resets the server."""
        return self._call_method('reset_server')

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button."""
        return self._call_method('press_pwr_btn')

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button."""
        return self._call_method('hold_pwr_btn')

    def set_host_power(self, power):
        """Toggle the power button of server.

        :param power: 'ON' or 'OFF'
        """
        return self._call_method('set_host_power', power)

    def set_one_time_boot(self, value):
        """Configures a single boot from a specific device."""
        return self._call_method('set_one_time_boot', value)

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image."""
        return self._call_method('insert_virtual_media', url, device)

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted."""
        return self._call_method('eject_virtual_media', device)

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status and allows the

        boot options for booting from the virtual media.
        """
        return self._call_method('set_vm_status', device, boot_option,
                                 write_protect)

    def get_current_boot_mode(self):
        """Retrieves the current boot mode settings."""
        return self._call_method('get_current_boot_mode')

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode settings."""
        return self._call_method('get_pending_boot_mode')

    def get_supported_boot_mode(self):
        """Retrieves the supported boot mode."""
        return self._call_method('get_supported_boot_mode')

    def set_pending_boot_mode(self, value):
        """Sets the boot mode of the system for next boot."""
        return self._call_method('set_pending_boot_mode', value)

    def get_persistent_boot_device(self):
        """Get the current persistent boot device set for the host."""
        return self._call_method('get_persistent_boot_device')

    def update_persistent_boot(self, device_type=[]):
        """Updates persistent boot based on the boot mode."""
        return self._call_method('update_persistent_boot', device_type)

    def get_secure_boot_mode(self):
        """Get the status if secure boot is enabled or not."""
        return self._call_method('get_secure_boot_mode')

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server."""
        return self._call_method('set_secure_boot_mode', secure_boot_enable)

    def reset_secure_boot_keys(self):
        """Reset secure boot keys to manufacturing defaults."""
        return self._call_method('reset_secure_boot_keys')

    def clear_secure_boot_keys(self):
        """Reset all keys."""
        return self._call_method('clear_secure_boot_keys')

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
             on the server.
        """
        return self._call_method('reset_ilo_credential', password)

    def reset_ilo(self):
        """Resets the iLO.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('reset_ilo')

    def reset_bios_to_default(self):
        """Resets the BIOS settings to default values.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('reset_bios_to_default')

    def get_host_uuid(self):
        """Request host UUID of the server.

        :returns: the host UUID of the server
        :raises: IloConnectionError if failed connecting to the iLO.
        """
        return self._call_method('get_host_uuid')

    def get_host_health_data(self, data=None):
        """Request host health data of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the embedded health data.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_data', data)

    def get_host_health_present_power_reading(self, data=None):
        """Request the power consumption of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_present_power_reading', data)

    def get_host_health_power_supplies(self, data=None):
        """Request the health power supply information.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power supply information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_power_supplies', data)

    def get_host_health_fan_sensors(self, data=None):
        """Get the health Fan Sensor Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the fan sensor information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_fan_sensors', data)

    def get_host_health_temperature_sensors(self, data=None):
        """Get the health Temp Sensor report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the temperature sensors
            information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_temperature_sensors', data)

    def get_host_health_at_a_glance(self, data=None):
        """Get the health at a glance Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the health at a glance information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_health_at_a_glance', data)

    def get_host_power_readings(self):
        """Retrieves the host power readings.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        return self._call_method('get_host_power_readings')

    def get_essential_properties(self):
        """Get the essential scheduling properties

        :returns: a dictionary containing memory size, disk size,
                  number of cpus, cpu arch, port numbers and
                  mac addresses.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        data = self._call_method('get_essential_properties')
        if (data['properties']['local_gb'] == 0):
            cred = self.snmp_credentials
            if cred and cred.get('snmp_inspection'):
                disksize = snmp.get_local_gb(self.host, cred)
                if disksize:
                    data['properties']['local_gb'] = disksize
                else:
                    msg = self._('SNMP inspection failed to '
                                 'get the disk size. Returning '
                                 'local_gb as 0.')
                    LOG.debug(msg)
            else:
                msg = self._("SNMP credentials were not set and "
                             "RIBCL/Redfish failed to get the disk size. "
                             "Returning local_gb as 0.")
                LOG.debug(msg)
        return data

    def get_server_capabilities(self):
        """Get hardware properties which can be used for scheduling

        :return: a dictionary of server capabilities.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        capabilities = self._call_method('get_server_capabilities')
        # TODO(nisha): Assumption is that Redfish always see the pci_device
        # member name field populated similarly to IPMI.
        # If redfish is not able to get nic_capacity, we can fall back to
        # IPMI way of retrieving nic_capacity in the future. As of now
        # the IPMI is not tested on Gen10, hence assuming that
        # Redfish will always be able to give the data.
        if ('Gen10' not in self.model):
            major_minor = (
                self._call_method('get_ilo_firmware_version_as_major_minor'))
            ilo_fw_str = common.get_ilo_version(major_minor)

            # NOTE(vmud213): Even if it is None, pass it on to get_nic_capacity
            # as we still want to try getting nic capacity through ipmitool
            # irrespective of what firmware we are using.
            nic_capacity = ipmi.get_nic_capacity(self.ipmi_host_info,
                                                 ilo_fw_str)
            if nic_capacity:
                capabilities.update({'nic_capacity': nic_capacity})

        if capabilities:
            return capabilities

    def activate_license(self, key):
        """Activates iLO license.

        :param key: iLO license key.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('activate_license', key)

    def delete_raid_configuration(self):
        """Deletes the logical drives from the system

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('delete_raid_configuration')

    def create_raid_configuration(self, raid_config):
        """Create the raid configuration on the hardware.

        :param raid_config: A dictionary containing target raid configuration
                            data. This data stucture should be as follows:
                            raid_config = {'logical_disks': [{'raid_level': 1,
                            'size_gb': 100, 'physical_disks': ['6I:1:5'],
                            'controller': 'HPE Smart Array P408i-a SR Gen10'},
                            <info-for-logical-disk-2>]}
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server
        """
        return self._call_method('create_raid_configuration', raid_config)

    def read_raid_configuration(self, raid_config=None):
        """Read the logical drives from the system.

        :param raid_config: None in case of post-delete read or in case of
                            post-create a dictionary containing target raid
                            configuration data. This data stucture should be as
                            follows:
                            raid_config = {'logical_disks': [{'raid_level': 1,
                            'size_gb': 100, 'physical_disks': ['6I:1:5'],
                            'controller': 'HPE Smart Array P408i-a SR Gen10'},
                            <info-for-logical-disk-2>]}
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        :returns: A dictionary containing list of logical disks
        """
        return self._call_method('read_raid_configuration', raid_config)

    def update_firmware(self, firmware_url, component_type):
        """Updates the given firmware on the server

        :param firmware_url: location of the firmware
        :param component_type: Type of component to be applied to.
        :raises: InvalidInputError, if the validation of the input fails
        :raises: IloError, on an error from iLO
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        return self._call_method(
            'update_firmware', firmware_url, component_type)

    def inject_nmi(self):
        """Inject NMI, Non Maskable Interrupt.

        Inject NMI (Non Maskable Interrupt) for a node immediately.

        :raises: IloError, on an error from iLO
        :raises: IloConnectionError, if not able to reach iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        return self._call_method('inject_nmi')

    def get_host_post_state(self):
        """Request the current state of system POST.

        Retrieves current state of system POST.

        :raises: IloError, on an error from iLO
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        return self._call_method('get_host_post_state')

    def get_current_bios_settings(self, only_allowed_settings=True):
        """Get current BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be returned. If False, All the BIOS settings supported
                by iLO are returned.
        :return: a dictionary of current BIOS settings is returned. Depending
                 on the 'only_allowed_settings', either only the allowed
                 settings are returned or all the supported settings are
                 returned.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('get_current_bios_settings',
                                 only_allowed_settings)

    def get_pending_bios_settings(self, only_allowed_settings=True):
        """Get current BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be returned. If False, All the BIOS settings supported
                by iLO are returned.
        :return: a dictionary of pending BIOS settings. Depending
                 on the 'only_allowed_settings', either only the allowed
                 settings are returned or all the supported settings are
                 returned.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('get_pending_bios_settings',
                                 only_allowed_settings)

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
        return self._call_method('set_bios_settings', data,
                                 only_allowed_settings)

    def get_default_bios_settings(self, only_allowed_settings=True):
        """Get default BIOS settings.

        :param: only_allowed_settings: True when only allowed BIOS settings
                are to be returned. If False, All the BIOS settings supported
                by iLO are returned.
        :return: a dictionary of default BIOS settings(factory settings).
                 Depending on the 'only_allowed_settings', either only
                 the allowed settings are returned or all the supported
                 settings are returned.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        return self._call_method('get_default_bios_settings',
                                 only_allowed_settings)

    def get_bios_settings_result(self):
        """Gets the result of the bios settings applied

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server.
        """
        return self._call_method('get_bios_settings_result')
