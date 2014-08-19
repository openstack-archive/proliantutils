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

INTERFACE_TYPE_SAS = 'SAS'
INTERFACE_TYPE_SCSI = 'SCSI'
INTERFACE_TYPE_SATA = 'SATA'

DISK_TYPE_HDD = 'HDD'
DISK_TYPE_SSD = 'SSD'

RAID_0 = '0'
RAID_1 = '1'
RAID_1_ADM = '1ADM'
RAID_10 = '10'
RAID_10_ADM = '10ADM'
RAID_5 = '5'
RAID_6 = '6'
RAID_50 = '50'
RAID_60 = '60'


INTERFACE_TYPE_MAP = {'SCSI': INTERFACE_TYPE_SCSI,
                      'SAS': INTERFACE_TYPE_SAS,
                      'SATA': INTERFACE_TYPE_SATA,
                      'SATASSD': INTERFACE_TYPE_SATA,
                      'SASSSD': INTERFACE_TYPE_SAS}

DISK_TYPE_MAP = {'SCSI': DISK_TYPE_HDD,
                 'SAS': DISK_TYPE_HDD,
                 'SATA': DISK_TYPE_HDD,
                 'SATASSD': DISK_TYPE_SSD,
                 'SASSSD': DISK_TYPE_SSD}


def get_interface_type(ssa_interface):
    return INTERFACE_TYPE_MAP[ssa_interface]


def get_disk_type(ssa_interface):
    return DISK_TYPE_MAP[ssa_interface]
