# Copyright 2017 Hewlett Packard Enterprise Development LP
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

# TODO(deray): Need to remove this hack sooner

import sys

import mock
from oslo_utils import importutils
import six


SUSHY_MANAGER_PACKAGE_SPEC = ('manager',)

sushy = importutils.try_import('sushy')
if sushy:
    sushy_resources_manager = mock.MagicMock(
        spec_set=SUSHY_MANAGER_PACKAGE_SPEC)
    sys.modules['sushy.resources.manager'] = sushy_resources_manager
    sushy.resources.common = mock.MagicMock()
    sushy_resources_manager.manager.Manager = type(
        'Manager', (sushy.resources.base.ResourceBase,), {})
    sushy.resources.common.ResetActionField = type(
        'ResetActionField', (sushy.resources.base.CompositeField,),
        {"target_uri": sushy.resources.base.Field('target', required=True)})
    if 'proliantutils.redfish' in sys.modules:
        six.moves.reload_module(sys.modules['proliantutils.redfish'])
