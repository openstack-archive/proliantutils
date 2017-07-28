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

# Push power button action constants

PUSH_POWER_BUTTON_PRESS = 'press'
PUSH_POWER_BUTTON_PRESS_AND_HOLD = 'press and hold'

# BIOS Settings boot mode constants

BIOS_BOOT_MODE_LEGACY_BIOS = 'legacy bios'
BIOS_BOOT_MODE_UEFI = 'uefi'

# Persistent boot device for set

BOOT_SOURCE_TARGET_CD = 'Cd'
BOOT_SOURCE_TARGET_PXE = 'Pxe'
BOOT_SOURCE_TARGET_UEFI_TARGET = 'UefiTarget'
BOOT_SOURCE_TARGET_HDD = 'Hdd'

# BIOS Sriov constants

SRIOV_ENABLED = 'sriov enabled'
SRIOV_DISABLED = 'sriov disabled'

# Secure Boot current boot constants

SECUREBOOT_CURRENT_BOOT_ENABLED = 'enabled'
SECUREBOOT_CURRENT_BOOT_DISABLED = 'disabled'

# Secure Boot reset keys constants

SECUREBOOT_RESET_KEYS_DEFAULT = 'default'
SECUREBOOT_RESET_KEYS_DELETE_ALL = 'delete all'
SECUREBOOT_RESET_KEYS_DELETE_PK = 'delete pk'

TPM_PRESENT_ENABLED = 'Tpm present enabled'
TPM_PRESENT_DISABLED = 'Tpm present disabled'
TPM_NOT_PRESENT = 'Tpm not present'

# BIOS Cpu Virtualisation contants

CPUVT_ENABLED = 'cpu_vt enabled'
CPUVT_DISABLED = 'cpu_vt disabled'

# System supported boot mode contants

SUPPORTED_LEGACY_BIOS_ONLY = 'legacy bios only'
SUPPORTED_UEFI_ONLY = 'uefi only'
SUPPORTED_LEGACY_BIOS_AND_UEFI = 'legacy bios and uefi'

# Health related constants
HEALTH_STATE_ENABLED = 'enabled'
HEALTH_STATE_DISABLED = 'disabled'
HEALTH_OK = 'ok'
HEALTH_WARNING = 'warning'
HEALTH_CRITICAL = 'critical'

# StorageControllers' supported device protocols
PROTOCOL_PCIe = "PCI Express (Vendor Proprietary)."
PROTOCOL_AHCI = "Advanced Host Controller Interface."
PROTOCOL_UHCI = "Universal Host Controller Interface."
PROTOCOL_SAS = "Serial Attached SCSI."
PROTOCOL_SATA = "Serial AT Attachment."
PROTOCOL_USB = "Universal Serial Bus."
PROTOCOL_NVMe = "Non-Volatile Memory Express."
PROTOCOL_FC = "Fibre Channel."
PROTOCOL_iSCSI = "Internet SCSI."
PROTOCOL_FCoE = "Fibre Channel over Ethernet."
PROTOCOL_FCP = "Fibre Channel Protocol for SCSI."
PROTOCOL_FICON = "FIbre CONnection (FICON)."
PROTOCOL_NVMeOverFabrics = "NVMe over Fabrics."
PROTOCOL_SMB = "Server Message Block (aka CIFS Common Internet File System)."
PROTOCOL_NFSv3 = "Network File System version 3."
PROTOCOL_NFSv4 = "Network File System version 4."
PROTOCOL_HTTP = "Hypertext Transport Protocol."
PROTOCOL_HTTPS = "Secure Hypertext Transport Protocol."
PROTOCOL_FTP = "File Transfer Protocol."
PROTOCOL_SFTP = "Secure File Transfer Protocol."

# Media types
MEDIA_TYPE_SSD = "SSD device"
MEDIA_TYPE_HDD = "HDD device"

# Volume type
RAW_DEVICE = "raw physical device"
NON_REDUNDANT = "volume is non-redundant"
MIRRORED = "Mirrored Volume"
STRIPED_WITH_PARITY = "volume striped with parity"
SPANNED_MIRRORS = "volume with spanned mirrors"
SPANNED_STRIPES_WITH_PARITY = "volume with spanned stripes with parity"

# RAID level constants
RAID_0 = 'raid 0'
RAID_1 = 'raid 1'
RAID_5 = 'raid 5'
RAID_1_0 = 'raid 1+0'
RAID_5_0 = 'raid 5+0'
