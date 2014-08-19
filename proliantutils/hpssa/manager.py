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

import json
import os

import jsonschema
from jsonschema import exceptions as json_schema_exc

from proliantutils.hpssa import exception
from proliantutils.hpssa import objects

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RAID_CONFIG_SCHEMA = os.path.join(CURRENT_DIR, "raid_config_schema.json")


def _compare_logical_disks(ld1, ld2):
    """Compares the two logical disks provided based on size."""
    return ld1['size_gb'] - ld2['size_gb']


def _find_physical_disks(logical_disk, server):
    # To be implemented
    pass


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


def create_configuration(raid_config):
    """Create a RAID configuration on this server.

    This method creates the given RAID configuration on the
    server based on the input passed.
    :param raid_config: The dictionary containing the requested
        RAID configuration. This data structure should be as follows:

        raid_config = {
                     'logical_disks': [
                                       {
                                        'size_gb': 100,
                                        'raid_level': 1,
                                       },
                                       .
                                       .
                                       .
                                      ]
                   }
    :raises exception.InvalidInputError, if input is invalid.
    """
    validate(raid_config)

    server = objects.Server()
    logical_disks_sorted = sorted(raid_config['logical_disks'],
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
    """Get the current RAID configuration.

    Get the RAID configuration from the server and return it
    as a dictionary.

    :returns: A dictionary of the below format.
        raid_config = {
                     'logical_disks': [
                                       {
                                        'size_gb': 100,
                                        'raid_level': 1,
                                        'physical_disks': [
                                                           '5I:0:1',
                                                           '5I:0:2',
                                                          ],
                                        'controller': 'Smart array controller'
                                        .
                                        .
                                       },
                                       .
                                       .
                                       .
                                      ]
                   }
    """
    server = objects.Server()
    logical_drives = server.get_logical_drives()
    raid_config = dict()
    raid_config['logical_disks'] = []

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

        raid_config['logical_disks'].append(logical_drive_info)

    return raid_config
