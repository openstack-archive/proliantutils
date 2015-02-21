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
from proliantutils.hpssa import types

# TODO(rameshg87): Add the minimum disks required for other RAID
# levels.
RAID_LEVEL_MIN_DISKS = {types.RAID_0: 2,
                        types.RAID_1: 2,
                        types.RAID_1_ADM: 3,
                        types.RAID_10: 4,
                        types.RAID_5: 3,
                        types.RAID_6: 3}

FILTER_CRITERIAS = ['disk_type', 'interface_type', 'model', 'firmware']


def _get_criteria_matching_disks(logical_disk, physical_drives):
    """Finds the physical drives matching the criterias of logical disk.

    This method finds the physical drives matching the criterias
    of the logical disk passed.

    :param logical_disk: The logical disk dictionary from raid config
    :param physical_drives: The physical drives to consider.
    :returns: A list of physical drives which match the criterias
    """
    matching_physical_drives = []
    criterias_to_consider = [x for x in FILTER_CRITERIAS
                             if x in logical_disk]

    for physical_drive in physical_drives:
        for criteria in criterias_to_consider:
            logical_drive_value = logical_disk.get(criteria)
            physical_drive_value = getattr(physical_drive, criteria)
            if logical_drive_value != physical_drive_value:
                break
        else:
            matching_physical_drives.append(physical_drive)

    return matching_physical_drives


def allocate_disks(logical_disk, server):
    """Allocate physical disks to a logical disk.

    This method allocated physical disks to a logical
    disk based on the current state of the server and
    criterias mentioned in the logical disk.

    :param logical_disk: a dictionary of a logical disk
        from the RAID configuration input to the module.
    :param server: An objects.Server object
    :raises: PhysicalDisksNotFoundError, if cannot find
        physical disks for the request.
    """
    size_gb = logical_disk['size_gb']
    raid_level = logical_disk['raid_level']
    number_of_physical_disks = logical_disk.get(
        'number_of_physical_disks', RAID_LEVEL_MIN_DISKS[raid_level])
    share_physical_disks = logical_disk.get('share_physical_disks', False)

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
            break

        if not share_physical_disks:
            # TODO(rameshg87): When this logical drives can share disks
            # with other arrays, figure out free space in other arrays
            # and then consider which array to use.
            pass
    else:
        raise exception.PhysicalDisksNotFoundError(size_gb=size_gb,
                                                   raid_level=raid_level)
