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

import os
import shutil

from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_utils import uuidutils
from pyremotevbox import vbox
import requests

from proliantutils import exception
from proliantutils.ilo import operations
from proliantutils import log


VBOX_ILO_POWER_MAP = {vbox.STATE_POWERED_OFF: 'OFF',
                      vbox.STATE_POWERED_ON: 'ON',
                      vbox.STATE_ERROR: 'ERROR'}
ILO_VBOX_POWER_MAP = {v: k
                      for k, v in VBOX_ILO_POWER_MAP.items()}
VBOX_ILO_BOOT_DEVICE_MAP = {vbox.DEVICE_NETWORK: 'NETWORK',
                            vbox.DEVICE_CDROM: 'CDROM',
                            vbox.DEVICE_DISK: 'HDD',
                            vbox.DEVICE_FLOPPY: 'FLOPPY'}
ILO_VBOX_BOOT_DEVICE_MAP = {'NETWORK': vbox.DEVICE_NETWORK,
                            'CDROM': vbox.DEVICE_CDROM,
                            'HDD': vbox.DEVICE_DISK,
                            'FLOPPY': vbox.DEVICE_DISK}

VBOX_ILO_BOOT_MODE_MAP = {vbox.FIRMWARE_BIOS: 'LEGACY',
                          vbox.FIRMWARE_EFI: 'UEFI'}
ILO_VBOX_BOOT_MODE_MAP = {v: k
                          for k, v in VBOX_ILO_BOOT_MODE_MAP.items()}

CONF = cfg.CONF
CONF.register_opts([cfg.StrOpt('host_share_location',
                               help=('The location of the shared folder in '
                                     'the VirtualBox Host.')),
                    cfg.StrOpt('shared_root',
                               help=('The location of the shared root in '
                                     'the cloud controller.'))],
                   group='vbox_emulator')

LOG = log.get_logger(__name__)


class VirtualBoxOperations(operations.IloOperations):

    def __init__(self, host, login, password, timeout=60, port=18083):

        if not CONF.vbox_emulator.host_share_location:
            raise exception.VirtualBoxEmulatorError(
                "[vbox_emulator]host_share_location is not set.")

        if not CONF.vbox_emulator.shared_root:
            raise exception.VirtualBoxEmulatorError(
                "[vbox_emulator]shared_root is not set.")

        vbox_host = vbox.VirtualBoxHost()
        self.vm = vbox_host.find_vm(host)
        self.pending_attach = {}
        self.pending_detach = {}
        self.pending_set_boot_device = None

    def get_all_licenses(self):
        """Retrieve license type, key, installation date, etc."""
        return 'VirtualBox Advanced License'

    def get_host_power_status(self):
        """Request the power state of the server."""
        return VBOX_ILO_POWER_MAP.get(self.vm.get_power_status(), 'ERROR')

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot."""
        return VBOX_ILO_BOOT_DEVICE_MAP[self.vm.get_boot_device()]

    def reset_server(self):
        """Resets the server."""
        self.vm.stop()
        self.vm.start()

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button."""
        self.vm.stop()

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button."""
        self.vm.stop()

    def set_host_power(self, power):
        """Toggle the power button of server.

        :param power: 'ON' or 'OFF'
        """
        if power == 'ON':
            self.vm.start()
        elif power == 'OFF':
            self.vm.stop()

    def set_one_time_boot(self, value):
        """Configures a single boot from a specific device."""
        self.vm.set_boot_device(ILO_VBOX_BOOT_DEVICE_MAP[value])

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image."""
        self.eject_virtual_media(device)
        shared_root = CONF.vbox_emulator.shared_root
        inf = requests.get(url, stream=True).raw
        filename = uuidutils.generate_uuid()
        if device == 'CDROM':
            filename = '%s.iso' % filename
        else:
            filename = '%s.dsk' % filename
        out_file = os.path.join(shared_root, filename)
        with open(out_file, 'w') as outf:
            shutil.copyfileobj(inf, outf)

        if device == "FLOPPY":
            vdi_filename = "%s.vdi" % out_file[0:-4]
            processutils.execute("qemu-img", "convert", "-f", "raw",
                                 "-O", "vdi", out_file, vdi_filename)
            os.remove(out_file)
            filename = os.path.basename(vdi_filename)

        host_root = CONF.vbox_emulator.host_share_location
        host_filename = '\\'.join([host_root, filename])
        device_type = ILO_VBOX_BOOT_DEVICE_MAP[device]
        self.vm.attach_device(device_type, host_filename)

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted."""
        # NOTE(rameshg87): VirtualBox doesn't allow to eject virtual media
        # when VM is powered on. So just return silently for now. It is
        # required to check because Ironic calls set_persistent_boot()
        # when bare metal is powered on.
        if self.get_host_power_status() == 'ON':
            LOG.warning(self._(
                "Cannot eject virtual media %s as VM is powered on"),
                device)
            return

        vbox_device = ILO_VBOX_BOOT_DEVICE_MAP[device]
        local_file = self.vm.get_attached_device(vbox_device)
        if local_file:
            local_file = local_file.split('\\')[-1]
            shared_root = CONF.vbox_emulator.shared_root
            full_path = os.path.join(shared_root, local_file)
            try:
                os.remove(full_path)
            except OSError:
                pass

        try:
            self.vm.detach_device(vbox_device)
        except Exception:
            pass

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status."""
        return

    def get_current_boot_mode(self):
        """Retrieves the current boot mode settings."""
        return VBOX_ILO_BOOT_MODE_MAP[self.vm.get_firmware_type()]

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode settings."""
        return self.get_current_boot_mode()

    def get_supported_boot_mode(self):
        """Retrieves the supported boot mode."""
        return 'LEGACY_UEFI'

    def set_pending_boot_mode(self, value):
        """Sets the boot mode of the system for next boot."""
        self.vm.set_firmware_type(ILO_VBOX_BOOT_MODE_MAP[value])

    def get_persistent_boot(self):
        """Retrieves the boot order of the host."""
        return self.get_one_time_boot()

    def set_persistent_boot(self, values=[]):
        """Configures to boot from a specific device."""
        # NOTE(rameshg87): VirtualBox doesn't allow to eject virtual media
        # when VM is powered on. So just return silently for now. It is
        # required to check because Ironic calls set_persistent_boot()
        # when bare metal is powered on.
        if self.get_host_power_status() == 'ON':
            LOG.warning(self._(
                "Cannot set persistent boot device to %s as VM is powered on"),
                values)
            return

        self.set_one_time_boot(values[0])

    def update_persistent_boot(self, device_type=[]):
        """Updates persistent boot based on the boot mode."""
        self.set_persistent_boot(device_type)

    def get_product_name(self):
        """Get the model name of the queried server."""
        return 'VirtualBox VM'
