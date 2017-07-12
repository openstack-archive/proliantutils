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

__author__ = 'HPE'

from sushy.resources import base
from sushy.resources.system import system

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import bios
from proliantutils.redfish.resources.system import drives
from proliantutils.redfish.resources.system import ethernetinterface
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish.resources.system import simplestorage
from proliantutils.redfish.resources.system import storage
from proliantutils.redfish.resources.system import volumes
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)


class PowerButtonActionField(base.CompositeField):
    allowed_values = base.Field('PushType@Redfish.AllowableValues',
                                adapter=list)

    target_uri = base.Field('target', required=True)


class HpeActionsField(base.CompositeField):
    computer_system_ext_powerbutton = (
        PowerButtonActionField('#HpeComputerSystemExt.PowerButton'))


class HpeEthernetInterface(base.CompositeField):
    eth_interface_path = base.Field(['EthernetInterface', '@odata.id'])


class HPESystem(system.System):
    """Class that extends the functionality of System resource class

    This class extends the functionality of System resource class
    from sushy
    """

    _hpe_actions = HpeActionsField(['Oem', 'Hpe', 'Actions'], required=True)

    """Oem specific system extensibility actions"""

    _bios_settings = None
    _simple_storage_path = base.Field(['SimpleStorage', '@odata.id'])
    _storage_path = base.Field(['Storage', '@odata.id'])

    _local_gb = None
    _simplestorage = None
    _storage = None
    _volume = None

    _connected_mac_addresses = None
    _hpe_eth_interface = HpeEthernetInterface(['Oem', 'Hpe',
                                               'EthernetInterfaces'])

    def _get_hpe_push_power_button_action_element(self):
        push_action = self._hpe_actions.computer_system_ext_powerbutton
        if not push_action:
            raise exception.MissingAttributeError(
                attribute='Oem/Hpe/Actions/#HpeComputerSystemExt.PowerButton',
                resource=self.path)

        return push_action

    def push_power_button(self, target_value):
        """Reset the system in hpe exclusive manner.

        :param target_value: The target value to be set.
        :raises: InvalidInputError, if the target value is not
            allowed.
        :raises: SushyError, on an error from iLO.
        """
        if target_value not in mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV:
            msg = ('The parameter "%(parameter)s" value "%(target_value)s" is '
                   'invalid. Valid values are: %(valid_power_values)s' %
                   {'parameter': 'target_value', 'target_value': target_value,
                    'valid_power_values': (
                        mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV.keys())})
            raise exception.InvalidInputError(msg)

        value = mappings.PUSH_POWER_BUTTON_VALUE_MAP_REV[target_value]
        target_uri = (
            self._get_hpe_push_power_button_action_element().target_uri)

        self._conn.post(target_uri, data={'PushType': value})

    @property
    def bios_settings(self):
        """Property to provide reference to bios_settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._bios_settings is None:
            self._bios_settings = bios.BIOSSettings(
                self._conn, utils.get_subresource_path_by(self, 'Bios'),
                redfish_version=self.redfish_version)

        return self._bios_settings

    def _get_hpe_sub_resource_collection_path(self, sub_resource):
        """Gets the path to the EthernetInterfaces"""
        eth_collection = None
        try:
            eth_collection = utils.get_subresource_path_by(self, sub_resource)
        except exception.MissingAttributeError:
            if self._hpe_eth_interface:
                eth_collection = self._hpe_eth_interface.eth_interface_path
                if not eth_collection:
                    raise exception.MissingAttributeError(
                        attribute=sub_resource, resource=self._path)
        return eth_collection

    @property
    def ethernet_interfaces(self):
        """Provide reference to EthernetInterfacesCollection instance"""
        if self._connected_mac_addresses is None:
            sub_res = 'EthernetInterfaces'
            self._connected_mac_addresses = (
                ethernetinterface.EthernetInterfaceCollection(
                    self._conn,
                    self._get_hpe_sub_resource_collection_path(sub_res),
                    redfish_version=self.redfish_version))

        return self._connected_mac_addresses

    @property
    def simplestorage(self):
        path = self._simple_storage_path
        if path:
            self._simplestorage = simplestorage.SimpleStorageCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._simplestorage

    @property
    def storage(self):
        path = self._storage_path
        if path:
            self._storage = storage.StorageCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._storage

    @property
    def volume(self, path):
        path = self._storage.volumes.get('@odata.id')
        if path:
            self._volume = volumes.VolumesCollection(
                self._conn, path, redfish_version=self.redfish_version)
        return self._volume

    @property
    def storage_summary(self):
        """Gets the storage size.

        Redfish standards supports the disk data in following possible ways:
        1. /redfish/v1/Systems/<System_id>/SimpleStorage - simple collection
        2. /redfish/v1/Systems/<System_id>/Storage - Storage collection
        3. /redfish/v1/Systems/<System_id>/Storage/<storage_id>/Volumes -
           Volume collection.
        4. /redfish/v1/Systems/<System_id>/Storage/<storage_id>/<Drive_id>
           - Drive URIs.
           or
          /redfish/v1/Chassis/<Chassis_id>/<Drive_id> - drive URIs

        The algorithm followed is:
        1. Get the biggest size from SimpleStorage if SimpleStorage is present.
        2. If the volume is present, get the biggest volume size else get the
           biggest disk size(DAS).
        3. Compares the disk size returned in 1 and 2 above.

        There is a possibility that the system does not have "SimpleStorage"
        and "Storage" URIs both and has the vendor specific storage URI.
        """
        size = 0
        if self._simple_storage_path:
            members = self.simplestorage.get_members()
            if members:
                for mem in members:
                    for device in mem.Devices:
                        if size < device.get("CapacityBytes"):
                            size = device.get("CapacityBytes")
        size_2 = self.get_disk_size_from_storage_uri()
        if size_2:
            self._local_gb = size_2
        else:
            self._local_gb = size
        self._local_gb = (self._local_gb / (1024 * 1024 * 1024))
        return self._local_gb

    def get_disk_size_from_storage_uri(self):
        """Gets volume/disk size.

        The pseudo algo followed is:
            1. Get members from Storage collection.
            2. Check if ['Volumes'] is present in each of the Storage member.
            3. If present, get Volumes collection given in the Storage member
               data.
            4. parse through each volume member and get the max volume size.
            5. If ['Volumes'] is not present in any of the Storage, then
               check if the ['Drives'] is present.(DAS case)
            6. if '5' is yes, then traverse through each drive URI and get the
               disk with greatest size.(drive URI may or may not be part of
               Storage collection).
            7. Follow steps 2 to 6 for each member of Storage collection.
        """
        size = 0
        if self._storage_path:
            members = self.storage.get_members()
            if members:
                for mem in members:
                    vol = mem.volumes
                    if vol is not None:
                        vol_collection_uri = vol.get('@odata.id')
                        vol_members = self.volumes_members(vol_collection_uri)
                        for vol_mem in vol_members:
                            if size < vol_mem.capacity_bytes:
                                size = vol_mem.capacity_bytes
                    else:
                        drives_list = mem.drives
                        if drives_list is not None:
                            dr_size = self._get_size_by_drives(drives_list)
                            if size < dr_size:
                                size = dr_size
        return size

    def _get_size_by_drives(self, drives_list):
        """Gets the disk of greatest size.

        :param: drives_list: A list of drives as
            [{'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'},
            {'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'},
            {'@odata.id':
                '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_id>'},
            {'@odata.id':
                '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_id>'},
            {'@odata.id':
                '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_id>'}]
        Note: There is no collection as "Drives", hence if tried to get
        data for '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives'
        or '</redfish/v1/Chassis/<chassis_id>/Drives' will lead to no data or
        invalid URI. The links can be even as follows:
        '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_type>/<drive_id>'
        or
        '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_type>/<Dr_id>'.
        In these cases the URIs,
        '</redfish/v1/Systems/<System_id>/Storage/<St_id>/Drives/<Dr_type>/'
        or
        '</redfish/v1/Chassis/<chassis_id>/Drives/<Drive_type>/'
        gives no data and is invalid URI.

        """

        size = 0
        for drive_mem in drives_list:
            drive_uri = drive_mem.get('@odata.id')
            dr_obj = drives.Drives(self._conn, drive_uri,
                                   self.redfish_version)
            if size < dr_obj.capacity_bytes:
                size = dr_obj.capacity_bytes
        return size
