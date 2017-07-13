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

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)

BOOT_SOURCE_TARGET_TO_PARTIAL_STRING_MAP = {
    sushy.BOOT_SOURCE_TARGET_CD: ('HPE Virtual CD-ROM',),
    sushy.BOOT_SOURCE_TARGET_PXE: ('NIC', 'PXE'),
    sushy.BOOT_SOURCE_TARGET_UEFI_TARGET: ('ISCSI',),
    sushy.BOOT_SOURCE_TARGET_HDD: ('Logical Drive', 'HDD', 'Storage', 'LogVol')
}


class BIOSSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)

    sriov_enabled = base.MappedField(['Attributes', 'Sriov'],
                                     mappings.SRIOV_MAP)

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
                self._conn,
                utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]),
                redfish_version=self.redfish_version)

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
                    self, ["Oem", "Hpe", "Links", "Boot"]),
                redfish_version=self.redfish_version)

        return self._boot_settings


class BIOSPendingSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)


class BIOSBootSettings(base.ResourceBase):

    boot_sources = base.Field("BootSources", adapter=list)
    persistent_boot_config_order = base.Field("PersistentBootConfigOrder",
                                              adapter=list)

    def get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        """
        boot_string = None
        if not self.persistent_boot_config_order or not self.boot_sources:
            msg = ('Boot sources or persistent boot config order not found')
            LOG.debug(msg)
            raise exception.IloError(msg)

        preferred_boot_device = self.persistent_boot_config_order[0]
        for boot_source in self.boot_sources:
            if ((boot_source.get("StructuredBootString") is not None) and (
                    preferred_boot_device ==
                    boot_source.get("StructuredBootString"))):
                boot_string = boot_source["BootString"]
                break
        else:
            msg = (('Persistent boot device failed, as no matched boot '
                    'sources found for device: %(persistent_boot_device)s')
                   % {'persistent_boot_device': preferred_boot_device})
            LOG.debug(msg)
            raise exception.IloError(msg)

        for key, value in BOOT_SOURCE_TARGET_TO_PARTIAL_STRING_MAP.items():
            for val in value:
                if val in boot_string:
                    return key
        return sushy.BOOT_SOURCE_TARGET_NONE
