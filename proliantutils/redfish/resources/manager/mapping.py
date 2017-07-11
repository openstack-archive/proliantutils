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

from sushy import utils

from proliantutils.redfish.resources.manager import constants as cons

VIRTUAL_MEDIA_TYPES_MAP = {
    'CD': cons.VIRTUAL_MEDIA_CD,
    'DVD': cons.VIRTUAL_MEDIA_DVD,
    'Floppy': cons.VIRTUAL_MEDIA_FLOPPY,
    'USBStick': cons.VIRTUAL_MEDIA_USB_STICK
}

VIRTUAL_MEDIA_TYPES_MAP_REV = utils.revert_dictionary(VIRTUAL_MEDIA_TYPES_MAP)
