# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

INTERFACE_TYPE_SAS = 'sas'
INTERFACE_TYPE_SCSI = 'scsi'
INTERFACE_TYPE_SATA = 'sata'

DISK_TYPE_HDD = 'hdd'
DISK_TYPE_SSD = 'ssd'

RAID_0 = '0'
RAID_1 = '1'
RAID_10 = '1+0'
RAID_5 = '5'
RAID_6 = '6'
RAID_50 = '5+0'
RAID_60 = '6+0'
# Below are not supported in Ironic now.
RAID_1_ADM = '1ADM'
RAID_10_ADM = '10ADM'

RAID_LEVEL_INPUT_TO_HPSSA_MAPPING = {RAID_50: '50', RAID_60: '60'}
RAID_LEVEL_HPSSA_TO_INPUT_MAPPING = {
    v: k for k, v in RAID_LEVEL_INPUT_TO_HPSSA_MAPPING.items()}

INTERFACE_TYPE_MAP = {'SCSI': INTERFACE_TYPE_SCSI,
                      'SAS': INTERFACE_TYPE_SAS,
                      'SATA': INTERFACE_TYPE_SATA,
                      'SATASSD': INTERFACE_TYPE_SATA,
                      'SASSSD': INTERFACE_TYPE_SAS,
                      'Solid State SAS': INTERFACE_TYPE_SAS}

DISK_TYPE_MAP = {'SCSI': DISK_TYPE_HDD,
                 'SAS': DISK_TYPE_HDD,
                 'SATA': DISK_TYPE_HDD,
                 'SATASSD': DISK_TYPE_SSD,
                 'SASSSD': DISK_TYPE_SSD,
                 'Solid State SAS': DISK_TYPE_SSD}

RAID_LEVEL_MIN_DISKS = {RAID_0: 1,
                        RAID_1: 2,
                        RAID_1_ADM: 3,
                        RAID_5: 3,
                        RAID_6: 4,
                        RAID_10: 4,
                        RAID_50: 6,
                        RAID_60: 8}


MINIMUM_DISK_SIZE = 1


def get_interface_type(ssa_interface):
    return INTERFACE_TYPE_MAP[ssa_interface]


def get_disk_type(ssa_interface):
    return DISK_TYPE_MAP[ssa_interface]
