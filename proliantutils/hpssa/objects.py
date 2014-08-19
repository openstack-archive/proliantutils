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

import time

from oslo.concurrency import processutils

from proliantutils.hpssa import exception
from proliantutils.hpssa import types


def _get_indentation(string):
    """Return the number of spaces before the current line."""
    return len(string) - len(string.lstrip(' '))


def _get_key_value(string):
    """Return the (key, value) as a tuple from a string."""

    key = ''
    value = ''
    try:
        key, value = string.split(':')
    except ValueError:
        string = string.lstrip(' ')
        if string.startswith('physicaldrive'):
            fields = string.split(' ')
            key = fields[0]
            value = fields[1]

    return key.lstrip(' ').rstrip(' '), value.lstrip(' ').rstrip(' ')


def _get_dict(lines, start_index, indentation):
    """Recursive function for parsing hpssacli output."""

    info = dict()
    current_item = None

    i = start_index
    while i < len(lines):

        current_line = lines[i]
        current_line_indentation = _get_indentation(current_line)

        if current_line_indentation == indentation:
            current_item = current_line.lstrip(' ')
            info[current_item] = dict()
            i = i + 1
            continue

        if i >= len(lines) - 1:
            key, value = _get_key_value(current_line)
            info[current_item][key] = value
            return info, i

        next_line = lines[i+1]
        next_line_indentation = _get_indentation(next_line)

        if current_line_indentation == next_line_indentation:
            key, value = _get_key_value(current_line)
            info[current_item][key] = value
            i = i + 1
        elif next_line_indentation > current_line_indentation:
            ret_dict, j = _get_dict(lines, i, current_line_indentation)
            info[current_item].update(ret_dict)
            i = j + 1
        elif next_line_indentation < current_line_indentation:
            key, value = _get_key_value(current_line)
            info[current_item][key] = value
            return info, i

    return info, i


def _convert_to_dict(stdout):
    """Wrapper function for parsing hpssacli command.

    This function gets the output from hpssacli command
    and calls the recursive function _get_dict to return
    the complete dictionary containing the RAID information.
    """

    lines = stdout.split("\n")
    lines = filter(None, lines)
    info_dict, j = _get_dict(lines, 0, 0)
    return info_dict


class Server(object):
    """Class for Server object

    This can consists of many RAID controllers - both internal
    and external.
    """

    def __init__(self):
        """Constructor for Server object."""
        self.last_updated = None
        self.controllers = []
        self.refresh()

    def _get_all_details(self):
        """Gets the current RAID configuration on the server.

        This methods gets the current RAID configuration on the server using
        hpssacli command and returns the output.

        :returns: stdout after running the hpssacli command
        """
        try:
            stdout, stderr = processutils.execute("hpssacli",
                                                  "controller",
                                                  "all",
                                                  "show",
                                                  "config",
                                                  "detail")
        except (OSError, processutils.ProcessExecutionError) as e:
            raise exception.HPSSAOperationError(reason=e)

        return stdout

    def refresh(self):
        """Refresh the server and it's child objects.

        This method removes all the cache information in the server
        and it's child objects, and fetches the information again from
        the server using hpssacli command.
        """
        config = self._get_all_details()

        raid_info = _convert_to_dict(config)
        self.controllers = []

        for key, value in raid_info.iteritems():
            self.controllers.append(Controller(key, value, self))

        self.last_updated = time.time()

    def get_controller_by_id(self, id):
        """Get the controller object given the id.

        This method returns the controller object when given the
        id.
        :param id: id of the controller, for example
            'Smart Array P822 in Slot 2'
        :returns: Controller object which has the id or None if the
            controller is not found.
        """
        for controller in self.controllers:
            if controller.id == id:
                return controller
        return None

    def get_logical_drives(self):
        """Get all the RAID logical drives in the Server.

        This method returns all the RAID logical drives on the server
        by examining all the controllers.

        :returns: a list of LogicalDrive objects.
        """
        logical_drives = []
        for controller in self.controllers:
            for array in controller.arrays:
                for logical_drive in array.logical_drives:
                    logical_drives.append(logical_drive)
        return logical_drives


class Controller(object):
    """This is the class for RAID controller."""

    def __init__(self, id, properties, parent):
        """Constructor for Controller object."""
        self.parent = parent
        self.properties = properties
        self.id = id
        self.unassigned_physical_drives = []
        self.arrays = []

        unassigned_drives = properties.get('unassigned', dict())
        for key, value in unassigned_drives.iteritems():
            self.unassigned_physical_drives.append(PhysicalDrive(key,
                                                                 value,
                                                                 self))

        arrays = filter(lambda x: x.startswith('Array'), properties.keys())
        for array in arrays:
            self.arrays.append(Array(array, properties[array], self))

    def get_physical_drive_by_id(self, id):
        """Get a PhysicalDrive object when provided with id.

        This method examines both assigned and unassigned physical
        drives of the controller and returns the physical drive.

        :param id: id of physical drive, for example '5I:1:1'.
        :returns: PhysicalDrive object having the id, or None if
            physical drive is not found.
        """
        for phy_drive in self.unassigned_physical_drives:
            if phy_drive.id == id:
                return phy_drive
        for array in self.arrays:
            for phy_drive in array.physical_drives:
                if phy_drive.id == id:
                    return phy_drive
        return None

    def execute_cmd(self, *args):
        """Execute a given hpssacli command on the controller.

        This method executes a given command on the controller.

        :params args: a tuple consisting of sub-commands to be appended
            after specifying the controller in hpssacli command.
        :raises: HPSSAOperationError, if hpssacli operation failed.
        """

        slot = self.properties['Slot']
        base_cmd = ("hpssacli", "controller", "slot=%s" % slot)
        cmd = base_cmd + args

        try:
            return processutils.execute(*cmd)
        except (OSError, processutils.ProcessExecutionError) as e:
            raise exception.HPSSAOperationError(reason=e)

    def create_logical_drive(self, logical_drive_info, physical_drive_ids):
        """Create a logical drive on the controller.

        This method creates a logical drive on the controller when the
        logical drive details and physical drive ids are passed to it.

        :param logical_drive_info: a dictionary containing the details
            of the logical drive as specified in raid config.
        :param physical_drive_ids: a list of physical drive ids to be used.
        :raises: HPSSAOperationError, if hpssacli operation failed.
        """
        phy_drive_ids = ','.join(physical_drive_ids)
        size_mb = logical_drive_info['size_gb'] * 1024
        raid_level = logical_drive_info['raid_level']
        self.execute_cmd("create", "type=logicaldrive",
                         "drives=%s" % phy_drive_ids,
                         "raid=%s" % raid_level,
                         "size=%s" % size_mb)

    def delete_all_logical_drives(self):
        """Deletes all logical drives on trh controller.

        This method deletes all logical drives on trh controller.
        :raises: HPSSAOperationError, if hpssacli operation failed.
        """
        self.execute_cmd("logicaldrive", "all", "delete", "forced")


class Array(object):
    """Class for a RAID Array.

    RAID array consists of many logical drives and many physical
    drives.
    """
    def __init__(self, id, properties, parent):
        """Constructor for a RAID Array object."""
        self.parent = parent
        self.properties = properties
        self.id = id[7:]

        self.logical_drives = []
        self.physical_drives = []

        logical_drives = filter(lambda x: x.startswith('Logical Drive'),
                                properties.keys())
        for logical_drive in logical_drives:
            self.logical_drives.append(LogicalDrive(logical_drive,
                                       properties[logical_drive],
                                       self))

        physical_drives = filter(lambda x: x.startswith('physicaldrive'),
                                 properties.keys())
        for physical_drive in physical_drives:
            self.physical_drives.append(PhysicalDrive(physical_drive,
                                        properties[physical_drive],
                                        self))


class LogicalDrive(object):
    """Class for LogicalDrive object."""

    def __init__(self, id, properties, parent):
        """Constructor for a LogicalDrive object."""
        # Strip off 'Logical Drive' before storing it in id
        self.id = id[15:]
        self.parent = parent
        self.properties = properties

        # TODO(rameshg87): Check if size is always reported in GB
        self.size_gb = int(float(self.properties['Size'].rstrip(' GB')))
        self.raid_level = self.properties['Fault Tolerance']

    def get_property(self, prop):
        if not self.properties:
            return None
        return self.properties.get(prop)


class PhysicalDrive:
    """Class for PhysicalDrive object."""

    def __init__(self, id, properties, parent):
        """Constructor for a PhysicalDrive object."""
        self.parent = parent
        self.properties = properties

        # Strip off physicaldrive before storing it in id
        self.id = id[14:]

        # TODO(rameshg87): Check if size is always reported in GB
        self.size_gb = int(float(self.properties['Size'].rstrip(' GB')))

        ssa_interface = self.properties['Interface Type']
        self.interface_type = types.get_interface_type(ssa_interface)
        self.disk_type = types.get_disk_type(ssa_interface)
