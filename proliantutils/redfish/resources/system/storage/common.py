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

from proliantutils import log

LOG = log.get_logger(__name__)


def get_local_gb(system_obj):
    local_gb = 0
    try:
        log_max = system_obj.smart_storage.logical_drives_maximum_size_mib
    except sushy.exceptions.SushyError as e:
        msg = (('The Redfish controller failed to get the '
                'resource data. Error %(error)s')
               % {'error': str(e)})
        LOG.debug(msg)
        log_max = 0
    try:
        volume_max = system_obj.storages.volumes_maximum_size_bytes
    except sushy.exceptions.SushyError as e:
        msg = (('The Redfish controller failed to get the '
                'resource data. Error %(error)s')
               % {'error': str(e)})
        LOG.debug(msg)
        volume_max = 0
    local_gb = max([(log_max * 1024 * 1024), volume_max])
    if local_gb == 0 or local_gb is None:
        try:
            phy_max = system_obj.smart_storage.physical_drives_maximum_size_mib
        except sushy.exceptions.SushyError as e:
            msg = (('The Redfish controller failed to get the '
                    'resource data. Error %(error)s')
                   % {'error': str(e)})
            LOG.debug(msg)
            phy_max = 0

        try:
            drives_max = system_obj.storages.drives_maximum_size_bytes
        except sushy.exceptions.SushyError as e:
            msg = (('The Redfish controller failed to get the '
                    'resource data. Error %(error)s')
                   % {'error': str(e)})
            LOG.debug(msg)
            drives_max = 0
        try:
            simple_max = system_obj.simple_storages.maximum_size_bytes
        except sushy.exceptions.SushyError as e:
            msg = (('The Redfish controller failed to get the '
                    'resource data. Error %(error)s')
                   % {'error': str(e)})
            LOG.debug(msg)
            simple_max = 0
        local_gb = max([(phy_max * 1024 * 1024), drives_max, simple_max])
    # Convert the received size to GB
    if local_gb is not None and local_gb > 0:
        local_gb = int(local_gb / (1024 * 1024 * 1024)) - 1
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
