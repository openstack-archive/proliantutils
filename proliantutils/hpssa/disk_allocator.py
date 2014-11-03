# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

from proliantutils import exception
from proliantutils.hpssa import constants

FILTER_CRITERIA = ['disk_type', 'interface_type', 'model', 'firmware']


def _get_criteria_matching_disks(logical_disk, physical_drives):
    """Finds the physical drives matching the criteria of logical disk.

    This method finds the physical drives matching the criteria
    of the logical disk passed.

    :param logical_disk: The logical disk dictionary from raid config
    :param physical_drives: The physical drives to consider.
    :returns: A list of physical drives which match the criteria
    """
    matching_physical_drives = []
    criteria_to_consider = [x for x in FILTER_CRITERIA
                            if x in logical_disk]

    for physical_drive_object in physical_drives:
        for criteria in criteria_to_consider:
            logical_drive_value = logical_disk.get(criteria)
            physical_drive_value = getattr(physical_drive_object, criteria)
            if logical_drive_value != physical_drive_value:
                break
        else:
            matching_physical_drives.append(physical_drive_object)

    return matching_physical_drives


def allocate_disks(logical_disk, server, raid_config):
    """Allocate physical disks to a logical disk.

    This method allocated physical disks to a logical
    disk based on the current state of the server and
    criteria mentioned in the logical disk.

    :param logical_disk: a dictionary of a logical disk
        from the RAID configuration input to the module.
    :param server: An objects.Server object
    :param raid_config: The target RAID configuration requested.
    :raises: PhysicalDisksNotFoundError, if cannot find
        physical disks for the request.
    """
    size_gb = logical_disk['size_gb']
    raid_level = logical_disk['raid_level']
    number_of_physical_disks = logical_disk.get(
        'number_of_physical_disks', constants.RAID_LEVEL_MIN_DISKS[raid_level])
    share_physical_disks = logical_disk.get('share_physical_disks', False)

    # Try to create a new independent array for this request.
    for controller in server.controllers:
        physical_drives = controller.unassigned_physical_drives
        physical_drives = _get_criteria_matching_disks(logical_disk,
                                                       physical_drives)
        physical_drives = [x for x in physical_drives
                           if x.size_gb >= size_gb]

        if len(physical_drives) >= number_of_physical_disks:
            selected_drives = sorted(physical_drives, key=lambda x: x.size_gb)
            selected_drive_ids = [x.id for x in selected_drives]
            logical_disk['controller'] = controller.id
            physical_disks = selected_drive_ids[:number_of_physical_disks]
            logical_disk['physical_disks'] = physical_disks
            return

    # We didn't find physical disks to create an independent array.
    # Check if we can get some shared arrays.
    if share_physical_disks:
        sharable_disk_wwns = []
        for sharable_logical_disk in raid_config['logical_disks']:
            if (sharable_logical_disk.get('share_physical_disks', False) and
                    'root_device_hint' in sharable_logical_disk):
                wwn = sharable_logical_disk['root_device_hint']['wwn']
                sharable_disk_wwns.append(wwn)

        for controller in server.controllers:
            sharable_arrays = [x for x in controller.raid_arrays if
                               x.logical_drives[0].wwn in sharable_disk_wwns]

            for array in sharable_arrays:

                # Check if criterias for the logical disk match the ones with
                # physical disks in the raid array.
                criteria_matched_disks = _get_criteria_matching_disks(
                    logical_disk, array.physical_drives)

                # Check if all disks in the array don't match the criteria
                if len(criteria_matched_disks) != len(array.physical_drives):
                    continue

                # Check if raid array can accomodate the logical disk.
                if array.can_accomodate(logical_disk):
                    logical_disk['controller'] = controller.id
                    logical_disk['array'] = array.id
                    return

    # We check both options and couldn't get any physical disks.
    raise exception.PhysicalDisksNotFoundError(size_gb=size_gb,
                                               raid_level=raid_level)
