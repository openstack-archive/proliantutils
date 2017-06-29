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

# Memory related constants
MEMORY_TYPE_NVDIMM_N = "nvdimm_n"
MEMORY_TYPE_DRAM = "dram"
MEMORY_DEVICE_TYPE_LOGICAL = "logical"
MEMORY_DEVICE_TYPE_DDR4 = "ddr4"
