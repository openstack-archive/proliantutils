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
from sushy.resources import common

from proliantutils import exception


class ActionsField(base.CompositeField):
    insert_vmedia = common.ResetActionField(
        '#HpeiLOVirtualMedia.InsertVirtualMedia')

    eject_vmedia = common.ResetActionField(
        '#HpeiLOVirtualMedia.EjectVirtualMedia')


class VirtualMedia(base.ResourceBase):

    media_types = base.Field('MediaTypes')
    """A list of allowed media types for the instance."""

    is_vmedia_inserted = base.Field('Inserted')
    """A boolean value which represents vmedia is inserted or not."""

    _actions = ActionsField(['Oem', 'Hpe', 'Actions'], required=True)

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a VirtualMedia Resource.

        :param connector: A Connector instance
        :param identity: The identity of the VirtualMedia
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(VirtualMedia, self).__init__(connector, identity,
                                           redfish_version)

    def _get_insert_action_element(self):
        insert_action = self._actions.insert_vmedia

        if not insert_action:
            raise exception.MissingActionError(
                action='#HpeiLOVirtualMedia.InsertVirtualMedia',
                resource=self._path)

        return insert_action

    def _get_eject_action_element(self):
        eject_action = self._actions.eject_vmedia

        if not eject_action:
            raise exception.MissingActionError(
                action='#HpeiLOVirtualMedia.EjectVirtualMedia',
                resource=self._path)

        return eject_action

    def insert_vmedia(self, url):
        """Inserts Virtual Media to the device."""
        target_uri = self._get_insert_action_element().target_uri
        data = {'Image': url}
        return self._conn.post(target_uri, data=data)

    def eject_vmedia(self):
        """Ejects Virtual Media from the device"""
        target_uri = self._get_eject_action_element().target_uri
        data = {}
        return self._conn.post(target_uri, data=data)


class VirtualMediaCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return VirtualMedia
