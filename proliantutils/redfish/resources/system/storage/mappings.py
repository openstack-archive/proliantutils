# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sushy import utils

from proliantutils.redfish.resources.system.storage import constants

DEVICE_PROTOCOLS_MAP = {
    'PCIe': constants.PROTOCOL_PCIe,
    'AHCI': constants.PROTOCOL_AHCI,
    'UHCI': constants.PROTOCOL_UHCI,
    'SAS': constants.PROTOCOL_SAS,
    'SATA': constants.PROTOCOL_SATA,
    'USB': constants.PROTOCOL_USB,
    'NVMe': constants.PROTOCOL_NVMe,
    'FC': constants.PROTOCOL_FC,
    'iSCSI': constants.PROTOCOL_iSCSI,
    'FCoE': constants.PROTOCOL_FCoE,
    'FCP': constants.PROTOCOL_FCP,
    'FICON': constants.PROTOCOL_FICON,
    'NVMeOverFabrics': constants.PROTOCOL_NVMeOverFabrics,
    'SMB': constants.PROTOCOL_SMB,
    'NFSv3': constants.PROTOCOL_NFSv3,
    'NFSv4': constants.PROTOCOL_NFSv4,
    'HTTP': constants.PROTOCOL_HTTP,
    'HTTPS': constants.PROTOCOL_HTTPS,
    'FTP': constants.PROTOCOL_FTP,
    'SFTP': constants.PROTOCOL_SFTP
}

MEDIA_TYPE_MAP = {
    'SSD': constants.MEDIA_TYPE_SSD,
    'HDD': constants.MEDIA_TYPE_HDD
}

VOLUME_TYPE_MAP = {
    'RawDevice': constants.RAW_DEVICE,
    'NonRedundant': constants.NON_REDUNDANT,
    'Mirrored': constants.MIRRORED,
    'StripedWithParity': constants.STRIPED_WITH_PARITY,
    'SpannedMirrors': constants.SPANNED_MIRRORS,
    'SpannedStripesWithParity': constants.SPANNED_STRIPES_WITH_PARITY
}

MAP_VOLUME_TYPE_TO_RAID_LEVELS = {
    constants.NON_REDUNDANT: "0",
    constants.MIRRORED: "1",
    constants.STRIPED_WITH_PARITY: "5",
    constants.SPANNED_MIRRORS: "10",
    constants.SPANNED_STRIPES_WITH_PARITY: "50"
}

RAID_LEVEL_MAP = {
    '0': constants.RAID_0,
    '1': constants.RAID_1,
    '5': constants.RAID_5,
    '10': constants.RAID_1_0,
    '50': constants.RAID_5_0
}

RAID_LEVEL_MAP_REV = (
    utils.revert_dictionary(RAID_LEVEL_MAP))
