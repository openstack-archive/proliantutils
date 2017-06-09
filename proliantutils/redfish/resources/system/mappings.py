# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
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

from sushy import utils

from proliantutils.redfish.resources.system import constants

PUSH_POWER_BUTTON_VALUE_MAP = {
    'Press': constants.PUSH_POWER_BUTTON_PRESS,
    'PressAndHold': constants.PUSH_POWER_BUTTON_PRESS_AND_HOLD,
}

PUSH_POWER_BUTTON_VALUE_MAP_REV = (
    utils.revert_dictionary(PUSH_POWER_BUTTON_VALUE_MAP))
