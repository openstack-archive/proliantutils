# Copyright 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

import mock
from oslo_utils import importutils
import six

from proliantutils.ilo import operations

pyremotevbox = importutils.try_import("pyremotevbox")
if not pyremotevbox:
    vbox = mock.MagicMock(spec=operations.IloOperations)
    pyremotevbox = mock.MagicMock(spec=['vbox'], vbox=vbox)

    vbox.STATE_POWERED_OFF = 'PoweredOff'
    vbox.STATE_POWERED_ON = 'Running'
    vbox.STATE_ERROR = 'Error'

    vbox.DEVICE_NETWORK = 'Network'
    vbox.DEVICE_FLOPPY = 'Floppy'
    vbox.DEVICE_CDROM = 'DVD'
    vbox.DEVICE_DISK = 'HardDisk'

    vbox.FIRMWARE_BIOS = 'BIOS'
    vbox.FIRMWARE_EFI = 'EFI'

    vbox.VirtualBoxHost = mock.MagicMock()
    sys.modules['pyremotevbox'] = pyremotevbox
    sys.modules['pyremotevbox.vbox'] = vbox

if 'proliantutils.ilo.vbox' in sys.modules:
    six.moves.reload_module(sys.modules['proliantutils.ilo.vbox'])
