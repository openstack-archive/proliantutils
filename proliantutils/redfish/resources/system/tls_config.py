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

from sushy.resources import base

from proliantutils.redfish import utils


class TLSConfig(base.ResourceBase):
    """Class that represents the TLS Configuration.

    This class extends the functionality of base resource class
    from sushy.
    """
    iscsi_initiator = base.Field("iSCSIInitiatorName")

    _tls_config_settings = None

    def is_iscsi_boot_supported(self):
        """Checks whether iscsi boot is supported or not.

        To find the iscsi boot support, check whether the PATCH
        operation is allowed on the iscsi 'settings' uri.
        :returns: True if it is supported else False
        """
        return utils.is_operation_allowed(
            'PATCH', self,
            ['@Redfish.Settings', 'SettingsObject'])

    @property
    def tls_config_settings(self):
        """Property to provide reference to TLS configuration settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._tls_config_settings is None:
            self._tls_config_settings = TLSConfigSettings(
                self._conn,
                utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]),
                redfish_version=self.redfish_version)

        self._tls_config_settings.refresh(force=False)
        return self._tls_config_settings

    def _do_refresh(self, force):
        """Do custom resource specific refresh activities

        On refresh, all sub-resources are marked as stale, i.e.
        greedy-refresh not done for them unless forced by ``force``
        argument.
        """
        if self._tls_config_settings is not None:
            self._tls_config_settings.invalidate(force)


class TLSConfigSettings(base.ResourceBase):
    """Class that represents the TLS configuration settings.

    This class extends the functionality of base resource class
    from sushy.
    """

    def upload_tls_certificate(self, cert_data):
        """Update tls certificate

        :param data: default tls certs data
        """
        self._conn.put(self.path, data=cert_data)
