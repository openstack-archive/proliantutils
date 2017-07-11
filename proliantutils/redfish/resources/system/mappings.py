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

from proliantutils.redfish.resources.system import constants

PUSH_POWER_BUTTON_VALUE_MAP = {
    'Press': constants.PUSH_POWER_BUTTON_PRESS,
    'PressAndHold': constants.PUSH_POWER_BUTTON_PRESS_AND_HOLD,
}

PUSH_POWER_BUTTON_VALUE_MAP_REV = (
    utils.revert_dictionary(PUSH_POWER_BUTTON_VALUE_MAP))

# BIOS Settings boot mode mappings
GET_BIOS_BOOT_MODE_MAP = {
    'LegacyBios': constants.BIOS_BOOT_MODE_LEGACY_BIOS,
    'Uefi': constants.BIOS_BOOT_MODE_UEFI
}

GET_BIOS_BOOT_MODE_MAP_REV = (
    utils.revert_dictionary(GET_BIOS_BOOT_MODE_MAP))

# BIOS Sriov mappings

SRIOV_MAP = {
    'Enabled': constants.SRIOV_ENABLED,
    'Disabled': constants.SRIOV_DISABLED
}

SECUREBOOT_CURRENT_BOOT_MAP = {
    'Enabled': constants.SECUREBOOT_CURRENT_BOOT_ENABLED,
    'Disabled': constants.SECUREBOOT_CURRENT_BOOT_DISABLED,
}

SECUREBOOT_CURRENT_BOOT_MAP_REV = (
    utils.revert_dictionary(SECUREBOOT_CURRENT_BOOT_MAP))

SECUREBOOT_RESET_KEYS_MAP = {
    'ResetAllKeysToDefault': constants.SECUREBOOT_RESET_KEYS_DEFAULT,
    'DeleteAllKeys': constants.SECUREBOOT_RESET_KEYS_DELETE_ALL,
    'DeletePK': constants.SECUREBOOT_RESET_KEYS_DELETE_PK,
}

SECUREBOOT_RESET_KEYS_MAP_REV = (
    utils.revert_dictionary(SECUREBOOT_RESET_KEYS_MAP))

TPM_MAP = {
    'PresentEnabled': constants.TPM_PRESENT_ENABLED,
    'PresentDisabled': constants.TPM_PRESENT_DISABLED,
    'NotPresent': constants.TPM_NOT_PRESENT
}
