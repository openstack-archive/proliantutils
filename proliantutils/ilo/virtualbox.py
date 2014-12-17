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
import ConfigParser
import urllib2
import shutil
import random

from pyremotevbox import vbox

from proliantutils.ilo import operations


VBOX_ILO_POWER_MAP = {
                      vbox.STATE_POWERED_OFF: 'OFF',
                      vbox.STATE_POWERED_ON: 'ON',
                      vbox.STATE_ERROR: 'ERROR'
                     }
ILO_VBOX_POWER_MAP = {v: k
                      for k, v in VBOX_ILO_POWER_MAP.items()}

VBOX_ILO_BOOT_DEVICE_MAP = {
                            vbox.DEVICE_NETWORK: 'NETWORK',
                            vbox.DEVICE_CDROM: 'CDROM',
                            vbox.DEVICE_DISK: 'HDD',
                            vbox.DEVICE_FLOPPY: 'FLOPPY',
                           }
ILO_VBOX_BOOT_DEVICE_MAP = {v: k
                            for k, v in VBOX_ILO_BOOT_DEVICE_MAP.items()}

VBOX_ILO_BOOT_MODE_MAP = {
                          vbox.FIRMWARE_BIOS: 'LEGACY',
                          vbox.FIRMWARE_EFI: 'UEFI'
                         }
ILO_VBOX_BOOT_MODE_MAP = {v: k
                          for k, v in VBOX_ILO_BOOT_MODE_MAP.items()}


def _get_mock_property(prop):

    conf_file = os.path.join(os.getenv('HOME'), 'proliantutils.conf')
    Config = ConfigParser.ConfigParser()
    Config.read(conf_file)
    if 'mock' in Config.sections():
        try:
            value = Config.get('mock', prop)
            return value
        except Exception:
            return None
    return None



class VirtualBoxOperations(operations.IloOperations):

    def __init__(self, host, login, password, timeout=60, port=18083):

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
        shared_root = _get_mock_property('shared_root')
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

        host_root = _get_mock_property('host_share_location')
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
            shared_root = _get_mock_property('shared_root')
            full_path = os.path.join(shared_root, local_file)
            try:
                os.remove(full_path)
            except OSError:
                pass

        self.vm.detach_device(vbox_device)

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
            self.pending_set_boot_device = values[0]
            return

        self.set_one_time_boot(device_type[0])

    def get_product_name(self):
        return 'VirtualBox VM'
