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

from proliantutils.ilo import ipmi
from proliantutils.ilo import operations
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
    'get_one_time_boot',
    'get_pending_boot_mode',
    'get_persistent_boot_device',
    'get_product_name',
    'get_secure_boot_mode',
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


class IloClient(operations.IloOperations):

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

    def set_iscsi_boot_info(self, mac, target_name, lun, ip_address,
                            port='3260', auth_method=None, username=None,
                            password=None):
        """Set iscsi details of the system in uefi boot mode.

        The iSCSI initiator is identified by the MAC provided.
        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param mac: MAC address of initiator.
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
        return self._call_method('set_iscsi_boot_info', mac, target_name, lun,
                                 ip_address, port, auth_method, username,
                                 password)

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
        return self._call_method('get_essential_properties')

    def get_server_capabilities(self):
        """Get hardware properties which can be used for scheduling

        :return: a dictionary of server capabilities.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        capabilities = {}
        if 'Gen9' in self.model:
            capabilities = self.ris.get_server_capabilities()
            data = self.ribcl.get_host_health_data()
            gpu = self.ribcl._get_number_of_gpu_devices_connected(data)
            capabilities.update(gpu)
            major_minor = self.ris.get_ilo_firmware_version_as_major_minor()
        else:
            capabilities = self.ribcl.get_server_capabilities()
            major_minor = self.ribcl.get_ilo_firmware_version_as_major_minor()

        # NOTE(vmud213): Even if it is None, pass it on to get_nic_capacity
        # as we still want to try getting nic capacity through ipmitool
        # irrespective of what firmware we are using.
        nic_capacity = ipmi.get_nic_capacity(self.info, major_minor)
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
