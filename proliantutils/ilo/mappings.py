# Copyright 2017 Hewlett Packard Enterprise Development LP
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

from proliantutils.ilo import constants


# Supported boot mode mappings
GET_SUPPORTED_BOOT_MODE_RIBCL_MAP = {
    'LEGACY_ONLY': constants.SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY,
    'UEFI_ONLY': constants.SUPPORTED_BOOT_MODE_UEFI_ONLY,
    'LEGACY_UEFI': constants.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI,
}

GET_SUPPORTED_BOOT_MODE_RIS_MAP = {
    0: constants.SUPPORTED_BOOT_MODE_LEGACY_BIOS_ONLY,
    3: constants.SUPPORTED_BOOT_MODE_UEFI_ONLY,
    2: constants.SUPPORTED_BOOT_MODE_LEGACY_BIOS_AND_UEFI,
}
