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

from proliantutils import exception

ERRMSG = "The specified operation is not supported on current platform."


class IloOperations(object):
    """iLO class for performing iLO Operations.

    This class provides an OO interface for retrieving information
    and managing iLO. It implements the same interface in
    python as described in HP iLO 4 Scripting and Command Line Guide.

    """
    def _(self, msg):
        """Prepends host information if available to msg and returns it."""
        try:
            return "[iLO %s] %s" % (self.host, msg)
        except AttributeError:
            return "[iLO <unknown>] %s" % msg

    def get_all_licenses(self):
        """Retrieve license type, key, installation date, etc."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_product_name(self):
        """Get the model name of the queried server."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_power_status(self):
        """Request the power state of the server."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_http_boot_url(self):
        """Request the http boot url.

        :returns: URL for http boot.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_http_boot_url(self, url):
        """Set the url to the UefiShellStartupUrl.

        :param url: URL for http boot.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

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
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def unset_iscsi_info(self):
        """Disable iscsi boot option of the system in uefi boot mode.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the system is
                 in the bios boot mode.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_iscsi_initiator_info(self):
        """Give iSCSI initiator information of iLO.

        :returns: iSCSI initiator information.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the system is
                 in the bios boot mode.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_iscsi_initiator_info(self, initiator_iqn):
        """Set iSCSI initiator information in iLO.

        :param initiator_iqn: Initiator iqn for iLO.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the system is
                 in the bios boot mode.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_vm_status(self, device='FLOPPY'):
        """Returns the virtual media drive status like url, is connected, etc.

        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def reset_server(self):
        """Resets the server."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_host_power(self, power):
        """Toggle the power button of server.

        :param power: 'ON' or 'OFF'
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_one_time_boot(self, value):
        """Configures a single boot from a specific device."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status and allows the

        boot options for booting from the virtual media.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_current_boot_mode(self):
        """Retrieves the current boot mode settings."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode settings."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_supported_boot_mode(self):
        """Retrieves the supported boot mode."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_pending_boot_mode(self, value):
        """Sets the boot mode of the system for next boot."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_persistent_boot(self):
        """Retrieves the boot order of the host."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_persistent_boot_device(self):
        """Get the current persistent boot device set for the host."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_persistent_boot(self, values=[]):
        """Configures to boot from a specific device."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def update_persistent_boot(self, device_type=[]):
        """Updates persistent boot based on the boot mode."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_secure_boot_mode(self):
        """Get the status if secure boot is enabled or not."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def reset_secure_boot_keys(self):
        """Reset secure boot keys to manufacturing defaults."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def clear_secure_boot_keys(self):
        """Reset all keys."""
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
             on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def reset_ilo(self):
        """Resets the iLO.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def reset_bios_to_default(self):
        """Resets the BIOS settings to default values.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_uuid(self):
        """Request host UUID of the server.

        :returns: the host UUID of the server
        :raises: IloConnectionError if failed connecting to the iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_health_data(self, data=None):
        """Request host health data of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the embedded health data.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_health_present_power_reading(self, data=None):
        """Request the power consumption of the server.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_health_power_supplies(self, data=None):
        """Request the health power supply information.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power supply information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_health_fan_sensors(self, data=None):
        """Get the health Fan Sensor Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the fan sensor information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """

    def get_host_health_temperature_sensors(self, data=None):
        """Get the health Temp Sensor report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the temperature sensors
            information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_health_at_a_glance(self, data=None):
        """Get the health at a glance Report.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the health at a glance information.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_power_readings(self):
        """Retrieves the host power readings.

        :param: the data to retrieve from the server, defaults to None.
        :returns: the dictionary containing the power readings.
        :raises: IloConnectionError if failed connecting to the iLO.
        :raises: IloError, on an error from iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_essential_properties(self):
        """Get the essential scheduling properties

        :returns: a dictionary containing memory size, disk size,
                  number of cpus, cpu arch, port numbers and
                  mac addresses.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_server_capabilities(self):
        """Get hardware properties which can be used for scheduling

        :return: a dictionary of server capabilities.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def activate_license(self, key):
        """Activates iLO license.

        :param key: iLO license key.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def update_firmware(self, firmware_url, component_type):
        """Updates the given firmware on the server

        :param firmware_url: location of the firmware file
        :param component_type: Type of component to be applied to.
        :raises: InvalidInputError, if the validation of the input fails
        :raises: IloError, on an error from iLO
        :raises: IloConnectionError, if not able to reach iLO.
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def inject_nmi(self):
        """Inject NMI, Non Maskable Interrupt.

        Inject NMI (Non Maskable Interrupt) for a node immediately.

        :raises: IloError, on an error from iLO
        :raises: IloConnectionError, if not able to reach iLO.
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)

    def get_host_post_state(self):
        """Request the current state of system POST

        Retrieves current state of system POST.

        :raises: IloError, on an error from iLO
        :raises: IloCommandNotSupportedError, if the command is
                 not supported on the server
        """
        raise exception.IloCommandNotSupportedError(ERRMSG)
