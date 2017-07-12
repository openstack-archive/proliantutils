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

from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')


class LinkField(base.CompositeField):
    array_controllers = base.Field(['ArrayControllers', '@odata.id'])
    host_bus_adapters = base.Field(['HostBusAdapters', '@odata.id'])


class SmartStorage(base.ResourceBase):

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    status = HealthStatusField('Status')

    links = LinkField('Links')
