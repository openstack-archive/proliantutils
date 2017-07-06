# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import sushy
from sushy.resources import base
from sushy import utils as sushy_utils

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)

BOOT_STRING_MAP = {
    'HPE Virtual CD-ROM': sushy.BOOT_SOURCE_TARGET_CD,
    'NIC': sushy.BOOT_SOURCE_TARGET_PXE,
    'PXE': sushy.BOOT_SOURCE_TARGET_PXE,
    'ISCSI': sushy.BOOT_SOURCE_TARGET_UEFI_TARGET,
    'Logical Drive': sushy.BOOT_SOURCE_TARGET_HDD,
    'HDD': sushy.BOOT_SOURCE_TARGET_HDD,
    'Storage': sushy.BOOT_SOURCE_TARGET_HDD,
    'LogVol': sushy.BOOT_SOURCE_TARGET_HDD
}

BOOT_STRING_MAP_REV = (
    sushy_utils.revert_dictionary(BOOT_STRING_MAP))


class BIOSSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)
    _pending_settings = None
    _boot_settings = None

    @property
    def pending_settings(self):
        """Property to provide reference to bios_pending_settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._pending_settings is None:
            self._pending_settings = BIOSPendingSettings(
                self._conn, utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]))

        return self._pending_settings

    @property
    def boot_settings(self):
        """Property to provide reference to bios boot instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._boot_settings is None:
            self._boot_settings = BIOSBootSettings(
                self._conn,
                utils.get_subresource_path_by(
                    self, ["Oem", "Hpe", "Links", "Boot"]))

        return self._boot_settings


class BIOSPendingSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)


class BIOSBootSettings(base.ResourceBase):

    boot_sources = base.Field(["BootSources"], adapter=list)
    persistent_boot_config_order = base.Field(["PersistentBootConfigOrder"],
                                              adapter=list)

    def _get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        """
        try:
            boot_order = self.persistent_boot_config_order
            for source in self.boot_sources:
                if (source["StructuredBootString"] == boot_order[0]):
                    boot_string = source["BootString"]
                    break
        except (sushy.exceptions.SushyError, KeyError) as e:
            msg = ('Get persistent boot device failed with the error. '
                   'Error %(error)s') % {'error': str(e)}
            LOG.debug(msg)
            raise exception.IloError(msg)

        for string in BOOT_STRING_MAP.keys():
            if string in boot_string:
                return BOOT_STRING_MAP[string]
        return sushy.BOOT_SOURCE_TARGET_NONE
