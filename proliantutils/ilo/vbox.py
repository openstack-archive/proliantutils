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
import random
import shutil
import urllib2

from oslo_config import cfg
from oslo_concurrency import processutils
from pyremotevbox import vbox

from proliantutils import exception
from proliantutils.ilo import operations


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
        return 'VirtualBox Advanced License'

    def get_host_power_status(self):
        return VBOX_ILO_POWER_MAP[self.vm.get_power_status()]

    def get_one_time_boot(self):
        return VBOX_ILO_BOOT_DEVICE_MAP[self.vm.get_boot_device()]

    def get_vm_status(self, device='FLOPPY'):
        # N/A
        return

    def reset_server(self):
        self.vm.stop()
        self.set_host_power('ON')

    def press_pwr_btn(self):
        self.vm.stop()

    def hold_pwr_btn(self):
        self.vm.stop()

    def set_host_power(self, power):
        if power == 'ON':

            if self.get_host_power_status() == 'OFF':
                for device in self.pending_detach.keys():
                    self.eject_virtual_media(device)

                for device, url in self.pending_attach.iteritems():
                    self.eject_virtual_media(device)
                    self.attach_virtual_media(device, url)

                if self.pending_set_boot_device:
                    self.set_one_time_boot(self.pending_set_boot_device)

            self.vm.start()
        elif power == 'OFF':
            self.vm.stop()

    def set_one_time_boot(self, value):
        if self.get_host_power_status() == 'ON':
            self.pending_set_boot_device = value
            return

        self.vm.set_boot_device(ILO_VBOX_BOOT_DEVICE_MAP[value])

    def insert_virtual_media(self, url, device='FLOPPY'):

        if self.get_host_power_status() == 'ON':
            self.pending_attach[device] = url
            return

        self.eject_virtual_media(device)
        shared_root = CONF.vbox_emulator.shared_root
        inf = urllib2.urlopen(url)
        characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        filename = ''.join(random.choice(characters) for _ in range(32))
        if device == 'CDROM':
            filename = '%s.iso' % filename
        else:
            filename = '%s.dsk' % filename
        out_file = os.path.join(shared_root, filename)
        outf = open(out_file, 'w')
        shutil.copyfileobj(inf, outf)
        outf.close()

        if device == "FLOPPY":
            vdi_filename = "%s.vdi" % out_file
            processutils.execute("qemu-img", "convert", "-f", "raw",
                                 "-O", "vdi", out_file, vdi_filename)
            os.remove(out_file)
            filename = "%s.vdi" % filename

        host_root = CONF.vbox_emulator.host_share_location
        host_filename = '\\'.join([host_root, filename])
        device_type = ILO_VBOX_BOOT_DEVICE_MAP[device]
        self.vm.attach_device(device_type, host_filename)

    def eject_virtual_media(self, device='FLOPPY'):

        if self.get_host_power_status() == 'ON':
            self.pending_detach[device] = True
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
        return

    def get_current_boot_mode(self):
        return VBOX_ILO_BOOT_MODE_MAP[self.vm.get_firmware_type()]

    def get_pending_boot_mode(self):
        return self.get_current_boot_mode()

    def get_supported_boot_mode(self):
        return 'LEGACY_UEFI'

    def set_pending_boot_mode(self, value):
        self.vm.set_firmware_type(ILO_VBOX_BOOT_MODE_MAP[value])

    def get_persistent_boot(self):
        return self.get_one_time_boot()

    def set_persistent_boot(self, values=[]):
        if self.get_host_power_status() == 'ON':
            self.pending_set_boot_device = values[0]
            return

        self.set_one_time_boot(values[0])

    def update_persistent_boot(self, device_type=[]):
        if self.get_host_power_status() == 'ON':
            self.pending_set_boot_device = device_type[0]
            return

        self.set_one_time_boot(device_type[0])

    def get_product_name(self):
        return 'VirtualBox VM'
