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

import sushy

from sushy.resources import base
from sushy.resources import common as sushy_common

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils import log


LOG = log.get_logger(__name__)


class ActionsField(base.CompositeField):
    update_firmware = (sushy_common.
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
        """Get the url for firmware update

        :returns: firmware update url
        :raises: Missing resource error on missing url
        """
        fw_update_action = self._actions.update_firmware
        if not fw_update_action:
            raise (sushy.exceptions.
                   MissingActionError(action='#UpdateService.SimpleUpdate',
                                      resource=self._path))
        return fw_update_action

    def flash_firmware(self, redfish_inst,  file_url):
        """Perform firmware flashing on a redfish system

        :param file_url: url to firmware bits.
        :param redfish_inst: redfish instance
        :raises: IloError, on an error from iLO.
        """
        action_data = {
            'ImageURI': file_url,
        }
        target_uri = self._get_firmware_update_element().target_uri
        try:
            self._conn.post(target_uri, data=action_data)
        except sushy.exceptions.SushyError as e:
            msg = (('The Redfish controller failed to update firmware '
                    'with file %(file)s Error %(error)s') %
                   {'file': file_url, 'error': str(e)})
            LOG.debug(msg)  # noqa
            raise exception.IloError(msg)

        self.wait_for_redfish_firmware_update_to_complete(redfish_inst)
        try:
            state, percent = self.get_firmware_update_progress()
        except sushy.exceptions.SushyError as e:
            msg = ('Failed to get firmware progress update '
                   'Error %(error)s' % {'error': str(e)})
            LOG.debug(msg)
            raise exception.IloError(msg)

        if state == "Error":
            msg = 'Unable to update firmware'
            LOG.debug(msg)  # noqa
            raise exception.IloError(msg)
        elif state == "Unknown":
            msg = 'Status of firmware update not known'
            LOG.debug(msg)  # noqa
        else:  # "Complete" | "Idle"
            LOG.info('Flashing firmware file: %s ... done', file_url)

    def wait_for_redfish_firmware_update_to_complete(self, redfish_object):
        """Continuously polls for iLO firmware update to complete.

        :param redfish_object: redfish instance
        """
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

            :returns: True upon firmware update completion otherwise False
            """
            curr_state, curr_percent = self.get_firmware_update_progress()
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

    def get_firmware_update_progress(self):
        """Get the progress of the firmware update.

        :returns: firmware update state, one of the following values:
                  "Idle","Uploading","Verifying","Writing",
                  "Updating","Complete","Error".
                  If the update resource is not found, then "Unknown".
        :returns: firmware update progress percent
        """
        # perform refresh
        try:
            self.refresh()
        except sushy.exceptions.SushyError as e:
            msg = (('Progress of firmware update not known. '
                    'Error %(error)s') %
                   {'error': str(e)})
            LOG.debug(msg)
            return "Unknown", "Unknown"

        # NOTE: Percentage is returned None after firmware flash is completed.
        return (self.firmware_state, self.firmware_percentage)
