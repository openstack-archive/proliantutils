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
from proliantutils.ilo import common
from sushy.resources import base
from sushy.resources import common as sushycommon


class ActionsField(base.CompositeField):
    update_firmware = (sushycommon.
                       ResetActionField('#UpdateService.SimpleUpdate'))


class HPEUpdateService(base.ResourceBase):
    """Class that extends the functionality of Base resource class

    This class extends the functionality of Base resource class
    from sushy
    """
    firmware_state = base.Field(['Oem', 'Hpe', 'State'])
    firmware_percentage = base.Field(['Oem', 'Hpe', 'FlashProgressPercent'])
    _actions = ActionsField(['Actions'], required=True)

    def _get_firmware_update_element(self):
        fw_update_action = self._actions.update_firmware
        if not fw_update_action:
            raise (exceptions.
                   MissingActionError(action='#UpdateService.SimpleUpdate',
                                      resource=self._path))
        return fw_update_action

    def flash_firmware_update(self, data):
        """Perform firmware update on a redfish system

        :param data: dict providing path to FW bits.
        :returns: response object of the post operation
        """
        if data is not None:
            target_uri = self._get_firmware_update_element().target_uri
            return self._conn.post(target_uri, data=data)

    @staticmethod
    def wait_for_redfish_firmware_update_to_complete(redfish_object):
        """Continuously polls for iLO firmware update to complete."""

        p_state = ['Idle']
        c_state = ['Idle']

        def has_firmware_flash_completed():
            """Checks for completion status of firmware update operation

            The below table shows the conditions for which the firmware update
            will be considered as DONE (be it success or error)::

            +-----------------------------------+-----------------------------+
            |    Previous state                 |   Current state             |
            +===================================+=============================+
            |    Idle                           |   Error, Complete           |
            +-----------------------------------+-----------------------------+
            |    Updating, Verifying,           |   Complete, Error,          |
            |    Uploading, Writing             |   Unknown, Idle             |
            +-----------------------------------+-----------------------------+
            """
            curr_state, curr_percent = (redfish_object.
                                        get_firmware_update_progress())
            p_state[0] = c_state[0]
            c_state[0] = curr_state
            if (((p_state[0] in ['Updating', 'Verifying',
                                 'Uploading', 'Writing'])
                    and (c_state[0] in ['Complete', 'Error',
                                        'Unknown', 'Idle']))
                    or (p_state[0] == 'Idle' and (c_state[0] in
                                                  ['Complete', 'Error']))):
                return True
            return False

        common.wait_for_operation_to_complete(
            has_firmware_flash_completed,
            delay_bw_retries=30,
            failover_msg='iLO firmware update has failed.'
        )
        common.wait_for_ilo_after_reset(redfish_object)
