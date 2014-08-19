# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

from proliantutils.hpssa import exception
from proliantutils.hpssa import objects


def _check_logical_disk(logical_disk_info):
    """Checks whether the logical disk info is valid."""

    if not isinstance(logical_disk_info, dict):
        msg = "Encountered logical disk info which is not a dictionary"
        raise exception.InvalidInputError(reason=msg)

    if not ('raid_level' in logical_disk_info and
            'size_gb' in logical_disk_info):
        msg = "Encountered logical disk without size or raid level."
        raise exception.InvalidInputError(reason=msg)

    controller = logical_disk_info.get('controller')
    physical_disks = logical_disk_info.get('physical_disks')

    if bool(controller) != bool(physical_disks):
        msg = "'controller' and 'physical_disks' must be present together."
        raise exception.InvalidInputError(reason=msg)

    if physical_disks and not isinstance(physical_disks, list):
        msg = "'physical_disks' must be a list"
        raise exception.InvalidInputError(reason=msg)


def _compare_logical_disks(ld1, ld2):
    """Compares the two logical disks provided based on size."""

    return ld1['size_gb'] - ld2['size_gb']


def _find_physical_disks(logical_disk, server):

    # To be implemented
    pass


def create_configuration(raid_info):
    """Create a RAID configuration on this server.

    This method creates the given RAID configuration on the
    server based on the input passed.
    :param raid_info:
    :raises exception.InvalidInputError, if input is invalid.
    """
    if not ('logical_disks' in raid_info and
            isinstance(raid_info['logical_disks'], list)):
        msg = ("Either 'logical_disks' key doesn't exist within raid_info "
               "or it isn't a list.")
        raise exception.InvalidInputError(reason=msg)

    for logical_disk in raid_info['logical_disks']:
        _check_logical_disk(logical_disk)

    server = objects.Server()
    logical_disks_sorted = sorted(raid_info['logical_disks'],
                                  cmp=_compare_logical_disks)

    for logical_disk in logical_disks_sorted:

        if 'physical_disks' not in logical_disk:
            _find_physical_disks(logical_disk, server)

        controller_id = logical_disk['controller']

        controller = server.get_controller_by_id(controller_id)
        if not controller:
            msg = ("Unable to find controller named '%s'" % controller_id)
            raise exception.InvalidInputError(reason=msg)

        for physical_disk in logical_disk['physical_disks']:
            disk_obj = controller.get_physical_drive_by_id(physical_disk)
            if not disk_obj:
                msg = ("Unable to find physical disk '%(physical_disk)s' "
                       "on '%(controller)s'" %
                       {'physical_disk': physical_disk,
                        'controller': controller_id})
                raise exception.InvalidInputError(reason=msg)

        physical_drive_ids = logical_disk['physical_disks']

        controller.create_logical_drive(logical_disk, physical_drive_ids)
        server.refresh()


def delete_configuration():
    """Delete a RAID configuration on this server."""

    server = objects.Server()
    for controller in server.controllers:
        controller.delete_all_logical_drives()


def get_configuration():
    """Get the current RAID configuration."""

    server = objects.Server()
    logical_drives = server.get_logical_drives()
    raid_info = dict()
    raid_info['logical_disks'] = []

    for logical_drive in logical_drives:
        logical_drive_info = {}
        logical_drive_info['size_gb'] = logical_drive.size_gb
        logical_drive_info['raid_level'] = logical_drive.raid_level

        array = logical_drive.parent
        controller = array.parent
        logical_drive_info['controller'] = controller.id

        physical_drive_ids = map(lambda x: x.id, array.physical_drives)
        logical_drive_info['physical_disks'] = physical_drive_ids

        vol_name = logical_drive.get_property('Logical Drive Label')
        logical_drive_info['volume_name'] = vol_name

        wwn = logical_drive.get_property('Unique Identifier')
        logical_drive_info['root_device_hint'] = {'wwn': wwn}

        raid_info['logical_disks'].append(logical_drive_info)

    return raid_info
