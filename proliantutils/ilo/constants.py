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

DEVICE_CDROM = 'CDROM'
DEVICE_FLOPPY = 'FLOPPY'
DEVICE_DISK = 'HDD'
DEVICE_NETWORK = 'NETWORK'
DEVICE_ONE_TIME_BOOT_NORMAL = 'Normal'
ACCEPTED_BOOT_DEVICES = [DEVICE_CDROM, DEVICE_FLOPPY,
                         DEVICE_DISK, DEVICE_NETWORK]

POWER_STATE_OFF = 'OFF'
POWER_STATE_ON = 'ON'
ACCEPTED_POWER_STATES = [POWER_STATE_OFF, POWER_STATE_ON]

BOOT_OPTION_BOOT_ONCE = 'BOOT_ONCE'

BOOT_MODE_BIOS = 'legacy'
BOOT_MODE_UEFI = 'uefi'
ACCEPTED_BOOT_MODES = [BOOT_MODE_BIOS, BOOT_MODE_UEFI]
