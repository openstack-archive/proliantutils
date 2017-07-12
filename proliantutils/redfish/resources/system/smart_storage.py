# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import logging

from proliantutils.redfish.resources.system import array_controller
from proliantutils.redfish import utils
from sushy.resources import base

LOG = logging.getLogger(__name__)


class SmartStorage(base.ResourceBase):

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    _array_controllers = None

    @property
    def array_controllers(self):
        """This property gets the list of instances for array controllers

        This property gets the list of instances for array controllers
        :returns: a list of instances of array controllers.
        """
        if self._array_controllers is None:
            self._array_controllers = (
                array_controller.ArrayControllerCollection(
                    self._conn, utils.get_subresource_path_by(
                        self, ['Links', 'ArrayControllers']),
                    redfish_version=self.redfish_version))
        return self._array_controllers

    def refresh(self):
        super(SmartStorage, self).refresh()
        self._array_controllers = None
