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

from sushy import exceptions
from sushy.resources import base
from sushy.resources import common

from proliantutils import exception
from proliantutils import log


VALID_DEVICES = {'FLOPPY': 'floppy',
                 'CDROM': 'cd'}

LOG = log.get_logger(__name__)


def get_vm_device(device, members):
    """Returns the given virtual media device object.

    :param  device: virtual media device to be queried
    :param members: list of virtual media objects
    :returns virtual media device object.
    :raises: IloInvalidInputError if device provided is not a valid
        vmedia device.
    """

    # Check if the input is valid
    if device not in VALID_DEVICES:
        msg = "Invalid device. Valid devices: FLOPPY or CDROM."
        LOG.debug(msg)
        raise exception.IloInvalidInputError(msg)

    for vmedia_device in members:
        if (VALID_DEVICES[device] in
                [item.lower() for item in vmedia_device.media_types]):
            return vmedia_device


class ActionsField(base.CompositeField):
    insert_vmedia = common.ResetActionField(
        '#HpeiLOVirtualMedia.InsertVirtualMedia')

    eject_vmedia = common.ResetActionField(
        '#HpeiLOVirtualMedia.EjectVirtualMedia')


class VirtualMedia(base.ResourceBase):

    media_types = base.Field('MediaTypes')
    """A list of allowed media types for the instance."""

    inserted = base.Field('Inserted')
    """A boolean value which represents vmedia is inserted or not."""

    _actions = ActionsField(['Oem', 'Hpe', 'Actions'], required=True)

    def _get_action_element(self, action_type):
        """Helper method to return the action object."""
        action = eval("self._actions." + action_type + "_vmedia")

        if not action:
            if action_type == "insert":
                action_path = '#HpeiLOVirtualMedia.InsertVirtualMedia'
            else:
                action_path = '#HpeiLOVirtualMedia.EjectVirtualMedia'

            raise exceptions.MissingActionError(
                action=action_path,
                resource=self._path)

        return action

    def insert_vmedia(self, url):
        """Inserts Virtual Media to the device

        :param url: URL to image.
        :raises: SushyError, on an error from iLO.
        """
        target_uri = self._get_action_element('insert').target_uri
        data = {'Image': url}
        self._conn.post(target_uri, data=data)

    def eject_vmedia(self):
        """Ejects Virtual Media from the device

        :raises: SushyError, on an error from iLO.
        """
        target_uri = self._get_action_element('eject').target_uri
        data = {}
        self._conn.post(target_uri, data=data)

    def set_vm_status(self, boot_on_next_reset):
        """Set the Virtual Media drive status.

        :param boot_on_next_reset: boolean value
        :raises: SushyError, on an error from iLO.
        """
        data = {
            "Oem": {
                "Hpe": {
                    "BootOnNextServerReset": boot_on_next_reset
                    }
                }
            }
        self._conn.patch(self.path, data=data)


class VirtualMediaCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return VirtualMedia
