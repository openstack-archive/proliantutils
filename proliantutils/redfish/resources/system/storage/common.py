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
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)


def _get_attribute_value_of(resource, attribute_name, value=None):
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
    logical_max_mib = 0
    volume_max_bytes = 0
    physical_max_mib = 0
    drives_max_bytes = 0
    simple_max_bytes = 0

    # Gets the resources and properties
    # its quite possible for a system to lack the resource, hence its
    # URI may also be lacking.

    # Check if smart_storage resource exist at the system
    smart_resource = _get_attribute_value_of(system_obj, 'smart_storage')
    if smart_resource is not None:
        logical_max_mib = _get_attribute_value_of(
            smart_resource, 'logical_drives_maximum_size_mib', value=0)
        physical_max_mib = _get_attribute_value_of(
            smart_resource, 'physical_drives_maximum_size_mib', value=0)

    # Check if storage resource exist at the system
    storage_resource = _get_attribute_value_of(system_obj, 'storages')
    if storage_resource is not None:
        volume_max_bytes = _get_attribute_value_of(
            storage_resource, 'volumes_maximum_size_bytes', value=0)
        drives_max_bytes = _get_attribute_value_of(
            storage_resource, 'drives_maximum_size_bytes', value=0)

    # Check if the SimpleStorage resource exist at the system.
    simple_resource = _get_attribute_value_of(system_obj, 'simple_storages')
    if simple_resource is not None:
        simple_max_bytes = _get_attribute_value_of(
            simple_resource, 'maximum_size_bytes', value=0)

    # Get the largest volume from the system.
    local_max_bytes = utils.max_safe([(logical_max_mib * 1024 * 1024),
                                     volume_max_bytes])
    # if volume is not found, then traverse through the possible disk drives
    # and get the biggest disk.

    if local_max_bytes == 0:
        local_max_bytes = utils.max_safe([(physical_max_mib * 1024 * 1024),
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


def has_ssd(sys_obj):
    return (sys_obj.smart_storage.array_controllers.physical_drive.has_ssd
            or sys_obj.storage.drive.has_ssd)


def has_rotational(sys_obj):
    v = sys_obj.smart_storage.array_controllers.physical_drive.has_rotational
    return (v or sys_obj.storage.drive.has_rotational)


def drive_rotational_speed_rpm(sys_obj):
    rpm = {}
    rpm.update(sys_obj.smart_storage.array_controllers.
               physical_drive.drive_rotational_speed_rpm)
    rpm.update(sys_obj.storage.drive.drive_rotational_speed_rpm)
    return rpm if len(rpm.keys()) > 0 else None


def logical_raid_levels(sys_obj):
    raid = {}
    raid.update(sys_obj.smart_storage.array_controllers.
                logical_drive.logical_raid_level)
    raid.update(sys_obj.storage.volume.logical_raid_level)
    return raid if len(raid.keys()) > 0 else None


def has_nvme_ssd(sys_obj):
    return (sys_obj.smart_storage.array_controllers.physical_drive.has_nvme_ssd
            or sys_obj.storage.drive.has_nvme_ssd)
