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


def _get_attribute_value_of(resource, attribute_name, default=None):
    """Gets the value of attribute_name from the resource

    It catches the exception, if any, while retrieving the
    value of attribute_name from resource and returns default.

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
        return default


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
    # Check if storage resource exist at the system
    storage_resource = _get_attribute_value_of(system_obj, 'storages')

    if smart_resource is not None:
        logical_max_mib = _get_attribute_value_of(
            smart_resource, 'logical_drives_maximum_size_mib', default=0)
    if storage_resource is not None:
        volume_max_bytes = _get_attribute_value_of(
            storage_resource, 'volumes_maximum_size_bytes', default=0)

    # Get the largest volume from the system.
    local_max_bytes = utils.max_safe([(logical_max_mib * 1024 * 1024),
                                     volume_max_bytes])
    # if volume is not found, then traverse through the possible disk drives
    # and get the biggest disk.
    if local_max_bytes == 0:
        if smart_resource is not None:
            physical_max_mib = _get_attribute_value_of(
                smart_resource, 'physical_drives_maximum_size_mib', default=0)

        if storage_resource is not None:
            drives_max_bytes = _get_attribute_value_of(
                storage_resource, 'drives_maximum_size_bytes', default=0)

        # Check if the SimpleStorage resource exist at the system.
        simple_resource = _get_attribute_value_of(system_obj,
                                                  'simple_storages')
        if simple_resource is not None:
            simple_max_bytes = _get_attribute_value_of(
                simple_resource, 'maximum_size_bytes', default=0)

        local_max_bytes = utils.max_safe([(physical_max_mib * 1024 * 1024),
                                         drives_max_bytes, simple_max_bytes])
    # Convert the received size to GB and reduce the value by 1 Gb as
    # ironic requires the local_gb to be returned 1 less than actual size.
    local_gb = 0
    if local_max_bytes > 0:
        local_gb = int(local_max_bytes / (1024 * 1024 * 1024)) - 1
    else:
        msg = ('The maximum size for the hard disk or logical '
               'volume could not be determined.')
        LOG.debug(msg)
    return local_gb


def has_ssd(system_obj):
    """Gets if the system has any drive as SSD drive

    :param system_obj: The HPESystem object.
    :returns True if system has SSD drives.
    """
    smart_value = False
    storage_value = False
    smart_resource = _get_attribute_value_of(system_obj, 'smart_storage')
    if smart_resource is not None:
        smart_value = _get_attribute_value_of(
            smart_resource, 'has_ssd', default=False)

    storage_resource = _get_attribute_value_of(system_obj, 'storages')
    if storage_resource is not None:
        storage_value = _get_attribute_value_of(
            storage_resource, 'has_ssd', default=False)

    return (smart_value or storage_value)


def has_rotational(system_obj):
    """Gets if the system has any drive as HDD drive

    :param system_obj: The HPESystem object.
    :returns True if system has HDD drives.
    """
    smart_value = False
    storage_value = False
    smart_resource = _get_attribute_value_of(system_obj, 'smart_storage')
    if smart_resource is not None:
        smart_value = _get_attribute_value_of(
            smart_resource, 'has_rotational', default=False)

    storage_resource = _get_attribute_value_of(system_obj, 'storages')
    if storage_resource is not None:
        storage_value = _get_attribute_value_of(
            storage_resource, 'has_rotational', default=False)

    return (smart_value or storage_value)


def has_nvme_ssd(system_obj):
    """Gets if the system has any drive as SSD drive

    :param system_obj: The HPESystem object.
    :returns True if system has SSD drives and protocol is NVMe.
    """
    storage_value = False
    storage_resource = _get_attribute_value_of(system_obj, 'storages')
    if storage_resource is not None:
        storage_value = _get_attribute_value_of(
            storage_resource, 'has_nvme_ssd', default=False)

    return storage_value


def logical_raid_levels(system_obj):
    """Gets the list of raid levels configured.

    :param system_obj: The HPESystem object.
    :returns the dictionary of such key-value pair
        {'logical_raid_level_<raid_level>' : 'true'}
    """
    smart_value = []
    smart_resource = _get_attribute_value_of(system_obj, 'smart_storage')
    if smart_resource is not None:
        smart_value = _get_attribute_value_of(
            smart_resource, 'logical_raid_levels', default=[])
    raid = {}
    for raid_level in smart_value:
        raid_var = 'logical_raid_level_' + str(raid_level)
        raid.update({raid_var: 'true'})
    return raid


def drive_rotational_speed_rpm(system_obj):
    """Gets the dictionary of rotational speed rpms of the disks.

    :param system_obj: The HPESystem object.
    :returns the dictionary of such key-value pair
        {'drive_rotational_<speed>_rpm' : 'true'}
    """
    smart_value = []
    storage_value = []
    smart_resource = _get_attribute_value_of(system_obj, 'smart_storage')
    if smart_resource is not None:
        smart_value = _get_attribute_value_of(
            smart_resource, 'drive_rotational_speed_rpm', default=[])
    storage_resource = _get_attribute_value_of(system_obj, 'storages')
    if storage_resource is not None:
        storage_value = _get_attribute_value_of(
            storage_resource, 'drive_rotational_speed_rpm', default=[])
    speed_dict = {}
    for speed in smart_value:
        speed_var = 'drive_rotational_' + str(speed) + '_rpm'
        speed_dict.update({speed_var: 'true'})
    for speed in storage_value:
        speed_var = 'drive_rotational_' + str(speed) + '_rpm'
        speed_dict.update({speed_var: 'true'})
    return speed_dict
