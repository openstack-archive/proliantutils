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

from proliantutils import exception
from proliantutils import log

LOG = log.get_logger(__name__)


def _get_attribute_value_of(resource, attribute_name, value=0):
    """Gets the value of attribute_name from the resource

    It catches the exception, if any, while retrieving the
    value of attribute_name from resource and returns zero.

    :param resource: The resource object
    :attribute_name: Property of the resource
    :returns the property value if no error encountered
        else return 0.
    """
    try:
        return getattr(resource, attribute_name)
    except (sushy.exceptions.SushyError,
            exception.MissingAttributeError) as e:
        msg = (('The Redfish controller failed to get the '
                'attribute %(attribute)s from resource %(resource)s. '
                'Error %(error)s') % {'error': str(e),
                                      'attribute': attribute_name,
                                      'resource':
                                      resource.__class__.__name__})
        LOG.debug(msg)
        return value


def get_local_gb(system_obj):
    """Gets the largest volume or the largest disk

    :param system_obj: The HPESystem object.
    :returns the size in GB
    """
    local_max_bytes = 0
    # Get the largest volume from the system.

    logical_max_mib = _get_attribute_value_of(
        system_obj.smart_storage, 'logical_drives_maximum_size_mib')
    volume_max_bytes = _get_attribute_value_of(
        system_obj.storages, 'volumes_maximum_size_bytes')
    local_max_bytes = max([(logical_max_mib * 1024 * 1024),
                          volume_max_bytes])
    # if volume is not found, then traverse through the possible disk drives
    # and get the biggest disk.

    if local_max_bytes == 0:
        physical_max_mib = _get_attribute_value_of(
            system_obj.smart_storage, 'physical_drives_maximum_size_mib')
        drives_max_bytes = _get_attribute_value_of(
            system_obj.storages, 'drives_maximum_size_bytes')
        simple_max_bytes = _get_attribute_value_of(
            system_obj.simple_storages, 'maximum_size_bytes')
        local_max_bytes = max([(physical_max_mib * 1024 * 1024),
                              drives_max_bytes, simple_max_bytes])
    # Convert the received size to GB and reduce the value by 1 Gb as
    # ironic requires the local_gb to be returned 1 less than actual size.
    local_gb = 0
    if local_max_bytes > 0:
        local_gb = int(local_max_bytes / (1024 * 1024 * 1024)) - 1
    else:
        msg = (('The maximum size for the hard disk or logical '
                'volume could not be determined.'))
        LOG.debug(msg)
    return local_gb
