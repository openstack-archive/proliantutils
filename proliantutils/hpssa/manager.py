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

import json
import os

import jsonschema
from jsonschema import exceptions as json_schema_exc

from proliantutils import exception
from proliantutils.hpssa import constants
from proliantutils.hpssa import disk_allocator
from proliantutils.hpssa import objects

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RAID_CONFIG_SCHEMA = os.path.join(CURRENT_DIR, "raid_config_schema.json")


def _update_physical_disk_details(raid_config, server):
    """Adds the physical disk details to the RAID configuration passed."""
    raid_config['physical_disks'] = []
    physical_drives = server.get_physical_drives()
    for physical_drive in physical_drives:
        physical_drive_dict = physical_drive.get_physical_drive_dict()
        raid_config['physical_disks'].append(physical_drive_dict)


def validate(raid_config):
    """Validates the RAID configuration provided.

    This method validates the RAID configuration provided against
    a JSON schema.

    :param raid_config: The RAID configuration to be validated.
    :raises: InvalidInputError, if validation of the input fails.
    """
    raid_schema_fobj = open(RAID_CONFIG_SCHEMA, 'r')
    raid_config_schema = json.load(raid_schema_fobj)
    try:
        jsonschema.validate(raid_config, raid_config_schema)
    except json_schema_exc.ValidationError as e:
        raise exception.InvalidInputError(e.message)

    for logical_disk in raid_config['logical_disks']:

        # If user has provided 'number_of_physical_disks' or
        # 'physical_disks', validate that they have mentioned at least
        # minimum number of physical disks required for that RAID level.
        raid_level = logical_disk['raid_level']
        min_disks_reqd = constants.RAID_LEVEL_MIN_DISKS[raid_level]

        no_of_disks_specified = None
        if 'number_of_physical_disks' in logical_disk:
            no_of_disks_specified = logical_disk['number_of_physical_disks']
        elif 'physical_disks' in logical_disk:
            no_of_disks_specified = len(logical_disk['physical_disks'])

        if (no_of_disks_specified and
                no_of_disks_specified < min_disks_reqd):
            msg = ("RAID level %(raid_level)s requires at least %(number) "
                   "disks." % {'raid_level': raid_level,
                               'number': min_disks_reqd})
            raise exception.InvalidInputError(msg)


def create_configuration(raid_config):
    """Create a RAID configuration on this server.

    This method creates the given RAID configuration on the
    server based on the input passed.
    :param raid_config: The dictionary containing the requested
        RAID configuration. This data structure should be as follows:
        raid_config = {'logical_disks': [{'raid_level': 1, 'size_gb': 100},
                                         <info-for-logical-disk-2>
                                        ]}
    :returns: the current raid configuration. This is same as raid_config
        with some extra properties like root_device_hint, volume_name,
        controller, physical_disks, etc filled for each logical disk
        after its creation.
    :raises exception.InvalidInputError, if input is invalid.
    """
    validate(raid_config)

    server = objects.Server()

    # Make sure we create the large disks first.  This is avoid the
    # situation that we avoid giving large disks to smaller requests.
    # For example, consider this:
    #   - two logical disks - LD1(50), LD(100)
    #   - have 4 physical disks - PD1(50), PD2(50), PD3(100), PD4(100)
    #
    # In this case, for RAID1 configuration, if we were to consider
    # LD1 first and allocate PD3 and PD4 for it, then allocation would
    # fail. So follow a particular order for allocation.
    logical_disks_sorted = sorted(raid_config['logical_disks'],
                                  key=lambda x: int(x['size_gb']),
                                  reverse=True)

    # We figure out the new disk created by recording the wwns
    # before and after the create, and then figuring out the
    # newly found wwn from it.
    wwns_before_create = set([x.wwn for x in
                              server.get_logical_drives()])

    for logical_disk in logical_disks_sorted:

        if 'physical_disks' not in logical_disk:
            disk_allocator.allocate_disks(logical_disk, server,
                                          raid_config)

        controller_id = logical_disk['controller']

        controller = server.get_controller_by_id(controller_id)
        if not controller:
            msg = ("Unable to find controller named '%s'" % controller_id)
            raise exception.InvalidInputError(reason=msg)

        if 'physical_disks' in logical_disk:
            for physical_disk in logical_disk['physical_disks']:
                disk_obj = controller.get_physical_drive_by_id(physical_disk)
                if not disk_obj:
                    msg = ("Unable to find physical disk '%(physical_disk)s' "
                           "on '%(controller)s'" %
                           {'physical_disk': physical_disk,
                            'controller': controller_id})
                    raise exception.InvalidInputError(msg)

        controller.create_logical_drive(logical_disk)

        # Now find the new logical drive created.
        server.refresh()
        wwns_after_create = set([x.wwn for x in
                                 server.get_logical_drives()])

        new_wwn = wwns_after_create - wwns_before_create

        if not new_wwn:
            reason = ("Newly created logical disk with raid_level "
                      "'%(raid_level)s' and size %(size_gb)s GB not "
                      "found." % {'raid_level': logical_disk['raid_level'],
                                  'size_gb': logical_disk['size_gb']})
            raise exception.HPSSAOperationError(reason=reason)

        new_logical_disk = server.get_logical_drive_by_wwn(new_wwn.pop())
        new_log_drive_properties = new_logical_disk.get_logical_drive_dict()
        logical_disk.update(new_log_drive_properties)

        wwns_before_create = wwns_after_create.copy()

    _update_physical_disk_details(raid_config, server)
    return raid_config


def delete_configuration():
    """Delete a RAID configuration on this server."""
    server = objects.Server()
    for controller in server.controllers:
        # Trigger delete only if there is some RAID array, otherwise
        # hpssacli will fail saying "no logical drives found."
        if controller.raid_arrays:
            controller.delete_all_logical_drives()


def get_configuration():
    """Get the current RAID configuration.

    Get the RAID configuration from the server and return it
    as a dictionary.

    :returns: A dictionary of the below format.
        raid_config = {
            'logical_disks': [{
                'size_gb': 100,
                'raid_level': 1,
                'physical_disks': [
                    '5I:0:1',
                    '5I:0:2'],
                'controller': 'Smart array controller'
                },
            ]
        }
    """
    server = objects.Server()
    logical_drives = server.get_logical_drives()
    raid_config = dict()
    raid_config['logical_disks'] = []

    for logical_drive in logical_drives:
        logical_drive_dict = logical_drive.get_logical_drive_dict()
        raid_config['logical_disks'].append(logical_drive_dict)

    _update_physical_disk_details(raid_config, server)
    return raid_config
