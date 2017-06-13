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

from sushy.resources.manager.manager import Manager

from proliantutils import exception
from proliantutils.redfish.resources.manager import virtual_media


class HPEManager(Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """

    _vmedia_resources = None

    def _get_vmedia_collection_path(self):
        """Helper function to find the VirtualMediaCollection path"""
        vmedia_col = self.json.get('VirtualMedia')
        if not vmedia_col:
            raise exception.MissingAttributeError(attribute='VirtualMedia',
                                                  resource=self._path)
        return vmedia_col.get('@odata.id')

    @property
    def vmedia_resources(self):
        """Property to provide reference to `VirtualMediaCollection` instance.

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._vmedia_resources is None:
            self._vmedia_resources = virtual_media.VirtualMediaCollection(
                self._conn,
                self._get_vmedia_collection_path(),
                redfish_version=self.redfish_version)

        return self._vmedia_resources

    def eject_vmedia(self, device):
        """Ejects the Virtual Media image if one is inserted.

        :param device: virual media device
        :raises: IloError, on an error from iLO.
        """
        vmedia_device = self._get_vm_device(device)

        if vmedia_device.is_vmedia_inserted is False:
            return

        response = vmedia_device.eject_vmedia()

        if response.status_code >= 300:
            msg = ("%s is not a valid response code received "
                   % response.status_code)
            raise exception.IloError(msg)

    def insert_vmedia(self, url, device):
        """Inserts the Virtual Media image to the device.

        :param url: URL to image
        :param device: virual media device
        :raises: IloError, on an error from iLO.
        """
        vmedia_device = self._get_vm_device(device)

        if vmedia_device.is_vmedia_inserted is True:
            self.eject_vmedia(device)

        response = vmedia_device.insert_vmedia(url)

        if response.status_code >= 300:
            msg = ("%s is not a valid response code received "
                   % response.status_code)
            raise exception.IloError(msg)

    def _get_vm_device(self, device):
        """Returns the given virtual media device object.

        :param  device: virtual media device to be queried
        :returns virtual media device object.
        :raises: IloInvalidInputError if device provided is not a valid
            vmedia device.
        """

        valid_devices = {'FLOPPY': 'floppy',
                         'CDROM': 'cd'}

        # Check if the input is valid
        if device not in valid_devices:
                raise exception.IloInvalidInputError(
                    "Invalid device. Valid devices: FLOPPY or CDROM.")

        for vmedia_device in self.vmedia_resources.get_members():
            if (valid_devices[device] in
                    [item.lower() for item in vmedia_device.media_types]):
                return vmedia_device
