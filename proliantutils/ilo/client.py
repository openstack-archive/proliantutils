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

from proliantutils.ilo import operations
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris

SUPPORTED_RIS_METHODS = ['get_product_name', 'get_http_boot_url',
                         'set_http_boot_url', 'get_host_power_status',
                         'get_current_boot_mode', 'set_pending_boot_mode',
                         'reset_ilo', 'reset_ilo_credential',
                         'reset_secure_keys', 'clear_secure_boot_keys',
                         'get_secure_boot_mode', 'set_secure_boot_mode',
                         'reset_bios_to_default', 'get_server_capabilities']


class IloClient(operations.IloOperations):

    def __init__(self, host, login, password, timeout=60, port=443,
                 bios_password=None):
        self.ribcl = ribcl.RIBCLOperations(host, login, password, timeout,
                                           port)
        self.ris = ris.RISOperations(host, login, password, bios_password)
        self.model = self.ribcl.get_product_name()

    def _call_method(self, method_name, *args, **kwargs):
        """Call the corresponding method using either RIBCL or RIS."""
        object = self.ribcl
        if ('Gen9' in self.model) and (method_name in SUPPORTED_RIS_METHODS):
            object = self.ris
        method = getattr(object, method_name)
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
        return self._call_method('set_http_boot_url')

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

    def get_persistent_boot(self):
        """Retrieves the boot order of the host."""
        return self._call_method('get_persistent_boot')

    def get_persistent_boot_device(self):
        """Get the current persistent boot device set for the host."""
        return self._call_method('get_persistent_boot_device')

    def set_persistent_boot(self, values=[]):
        """Configures to boot from a specific device."""
        return self._call_method('set_persistent_boot', values)

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
        if 'Gen9' in self.model:
            capabilities = self.ris.get_server_capabilities()
            gpu = self.ribcl._get_number_of_gpu_devices_connected()
            capabilities.update(gpu)
            return capabilities
        else:
            return self.ribcl.get_server_capabilities()
