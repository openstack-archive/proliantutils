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

class HPEUpdateService(base.ResourceBase):
    """Class that extends the functionality of Base resource class

    This class extends the functionality of Base resource class
    from sushy
    """
    def flash_firmware_update(self, fw_update_uri, action_data):
        """Perform firmware update on a redfish system

        :param fw_update_uri: Firmware update uri
        :param action_data: dict providing path to FW bits.
        :returns: response object of the post operation
        """  
        if fw_update_uri is not None:
            return self._conn.post(fw_update_uri, data=action_data)
