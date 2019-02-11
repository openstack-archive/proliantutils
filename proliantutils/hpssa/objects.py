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

import os
import re
import time

from oslo_concurrency import processutils
from oslo_utils import strutils

from proliantutils import exception
from proliantutils.hpssa import constants
from proliantutils import log


LOG = log.get_logger(__name__)


def _get_indentation(string):
    """Return the number of spaces before the current line."""
    return len(string) - len(string.lstrip(' '))


def _get_key_value(string):
    """Return the (key, value) as a tuple from a string."""
    # Normally all properties look like this:
    #   Unique Identifier: 600508B1001CE4ACF473EE9C826230FF
    #   Disk Name: /dev/sda
    #   Mount Points: None
    key = ''
    value = ''
    try:
        key, value = string.split(': ')
    except ValueError:
        # This handles the case when the property of a logical drive
        # returned is as follows. Here we cannot split by ':' because
        # the disk id has colon in it. So if this is about disk,
        # then strip it accordingly.
        #   Mirror Group 0: physicaldrive 6I:1:5
        string = string.lstrip(' ')
        if string.startswith('physicaldrive'):
            fields = string.split(' ')
            # Include fields[1] to key to avoid duplicate pairs
            # with the same 'physicaldrive' key
            key = fields[0] + " " + fields[1]
            value = fields[1]
        else:
            # TODO(rameshg87): Check if this ever occurs.
            return string.strip(' '), None

    return key.strip(' '), value.strip(' ')


def _get_dict(lines, start_index, indentation, deep):
    """Recursive function for parsing hpssacli/ssacli output."""

    info = {}
    current_item = None

    i = start_index
    while i < len(lines):

        current_line = lines[i]
        current_line_indentation = _get_indentation(current_line)

        # Check for multi-level returns
        if current_line_indentation < indentation:
            return info, i-1

        if current_line_indentation == indentation:
            current_item = current_line.lstrip(' ')
            info[current_item] = {}
            i = i + 1
            continue

        if i < len(lines) - 1:
            next_line_indentation = _get_indentation(lines[i+1])
        else:
            next_line_indentation = current_line_indentation

        if next_line_indentation > current_line_indentation:
            ret_dict, i = _get_dict(lines, i, current_line_indentation, deep+1)
            for key in ret_dict.keys():
                if key in info[current_item]:
                    info[current_item][key].update(ret_dict[key])
                else:
                    info[current_item][key] = ret_dict[key]
        else:
            key, value = _get_key_value(current_line)
            if key:
                info[current_item][key] = value

        # Do not return if it's the top level of recursion
        if next_line_indentation < current_line_indentation and deep > 0:
            return info, i

        i = i + 1

    return info, i


def _convert_to_dict(stdout):
    """Wrapper function for parsing hpssacli/ssacli command.

    This function gets the output from hpssacli/ssacli command
    and calls the recursive function _get_dict to return
    the complete dictionary containing the RAID information.
    """

    lines = stdout.split("\n")
    lines = list(filter(None, lines))
    info_dict, j = _get_dict(lines, 0, 0, 0)
    return info_dict


def _ssacli(*args, **kwargs):
    """Wrapper function for executing hpssacli/ssacli command.

    This function executes ssacli command if it exists, else it
    falls back to hpssacli.
    :param args: args to be provided to hpssacli/ssacli command
    :param kwargs: kwargs to be sent to processutils except the
        following:
        - dont_transform_to_hpssa_exception - Set to True if this
          method shouldn't transform other exceptions to hpssa
          exceptions only when hpssa controller is available. This is
          useful when the return code from hpssacli/ssacli is useful for
          analysis.
    :returns: a tuple containing the stdout and stderr after running
        the process.
    :raises: HPSSAOperationError, if some error was encountered and
        dont_dont_transform_to_hpssa_exception was set to False.
    :raises: OSError or processutils.ProcessExecutionError if execution
        failed and dont_transform_to_hpssa_exception was set to True.
    """

    dont_transform_to_hpssa_exception = kwargs.get(
        'dont_transform_to_hpssa_exception', False)
    kwargs.pop('dont_transform_to_hpssa_exception', None)

    try:
        if os.path.exists("/usr/sbin/ssacli"):
            stdout, stderr = processutils.execute("ssacli",
                                                  *args, **kwargs)
        else:
            stdout, stderr = processutils.execute("hpssacli",
                                                  *args, **kwargs)
    except (OSError, processutils.ProcessExecutionError) as e:
        if 'No controllers detected' in str(e):
            msg = ("SSA controller not found. Enable ssa controller"
                   " to continue with the desired operation")
            raise exception.HPSSAOperationError(reason=msg)
        elif not dont_transform_to_hpssa_exception:
            raise exception.HPSSAOperationError(reason=e)
        else:
            raise

    return stdout, stderr


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
        hpssacli/ssacli command and returns the output.

        :returns: stdout after running the hpssacli/ssacli command. The output
            looks as follows:

            Smart Array P822 in Slot 2
               Bus Interface: PCI
               Slot: 2
               Serial Number: PDVTF0BRH5T0MO
               .
               .
               .
               Array: A
                  Interface Type: SAS
                  Unused Space: 0  MB
                  Status: OK

                  Logical Drive: 1
                     Size: 2.7 TB
                     Fault Tolerance: 6
                     Heads: 255
                     Unique Identifier: 600508B1001C45441D106BDFAAEBA41E
                     Disk Name: /dev/sda
                     .
                     .

               physicaldrive 5I:1:1
                  Port: 5I
                  Box: 1
                  Bay: 1
                  Status: OK
                  Interface Type: SAS
                  Drive Type: Data Drive
                  .
                  .
                  .
                physicaldrive 5I:1:2
                  Port: 5I
                  Box: 1
                  Bay: 2
                  Status: OK
                  Interface Type: SAS
                  Drive Type: Data Drive

        :raises: HPSSAOperationError, if hpssacli/ssacli operation failed.
        """
        stdout, stderr = _ssacli("controller", "all", "show",
                                 "config", "detail")
        return stdout

    def refresh(self):
        """Refresh the server and it's child objects.

        This method removes all the cache information in the server
        and it's child objects, and fetches the information again from
        the server using hpssacli/ssacli command.

        :raises: HPSSAOperationError, if hpssacli/ssacli operation failed.
        """
        config = self._get_all_details()

        raid_info = _convert_to_dict(config)
        self.controllers = []

        for key, value in raid_info.items():
            self.controllers.append(Controller(key, value, self))

        self.last_updated = time.time()

    def get_controller_by_id(self, id):
        """Get the controller object given the id.

        This method returns the controller object for given id.

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
            for array in controller.raid_arrays:
                for logical_drive in array.logical_drives:
                    logical_drives.append(logical_drive)
        return logical_drives

    def get_physical_drives(self):
        """Get all the RAID physical drives on the Server.

        This method returns all the physical drives on the server
        by examining all the controllers.

        :returns: a list of PhysicalDrive objects.
        """
        physical_drives = []
        for controller in self.controllers:
            # First add unassigned physical drives.
            for physical_drive in controller.unassigned_physical_drives:
                physical_drives.append(physical_drive)
            # Now add physical drives part of RAID arrays.
            for array in controller.raid_arrays:
                for physical_drive in array.physical_drives:
                    physical_drives.append(physical_drive)

        return physical_drives

    def get_logical_drive_by_wwn(self, wwn):
        """Get the logical drive object given the wwn.

        This method returns the logical drive object with the given wwn.

        :param wwn: wwn of the logical drive
        :returns: LogicalDrive object which has the wwn or None if
            logical drive is not found.
        """
        disk = [x for x in self.get_logical_drives() if x.wwn == wwn]
        if disk:
            return disk[0]
        return None


class Controller(object):
    """This is the class for RAID controller."""

    def __init__(self, id, properties, parent):
        """Constructor for Controller object."""
        self.parent = parent
        self.properties = properties
        self.id = id
        self.unassigned_physical_drives = []
        self.raid_arrays = []

        # This step is needed because of the mismatch in the data returned by
        # hpssacli and ssacli.
        attr = ''.join(x for x in properties
                       if x == 'Unassigned' or x == 'unassigned')

        unassigned_drives = properties.get(attr, {})
        for key, value in unassigned_drives.items():
            self.unassigned_physical_drives.append(PhysicalDrive(key,
                                                                 value,
                                                                 self))

        raid_arrays = filter(lambda x: x.startswith('Array'),
                             properties.keys())
        for array in raid_arrays:
            self.raid_arrays.append(RaidArray(array, properties[array], self))

    def get_physical_drive_by_id(self, id):
        """Get a PhysicalDrive object for given id.

        This method examines both assigned and unassigned physical
        drives of the controller and returns the physical drive.

        :param id: id of physical drive, for example '5I:1:1'.
        :returns: PhysicalDrive object having the id, or None if
            physical drive is not found.
        """
        for phy_drive in self.unassigned_physical_drives:
            if phy_drive.id == id:
                return phy_drive
        for array in self.raid_arrays:
            for phy_drive in array.physical_drives:
                if phy_drive.id == id:
                    return phy_drive
        return None

    def execute_cmd(self, *args, **kwargs):
        """Execute a given hpssacli/ssacli command on the controller.

        This method executes a given command on the controller.

        :params args: a tuple consisting of sub-commands to be appended
            after specifying the controller in hpssacli/ssacli command.
        :param kwargs: kwargs to be passed to execute() in processutils
        :raises: HPSSAOperationError, if hpssacli/ssacli operation failed.
        """
        slot = self.properties['Slot']
        base_cmd = ("controller", "slot=%s" % slot)
        cmd = base_cmd + args
        return _ssacli(*cmd, **kwargs)

    def create_logical_drive(self, logical_drive_info):
        """Create a logical drive on the controller.

        This method creates a logical drive on the controller when the
        logical drive details and physical drive ids are passed to it.

        :param logical_drive_info: a dictionary containing the details
            of the logical drive as specified in raid config.
        :raises: HPSSAOperationError, if hpssacli/ssacli operation failed.
        """
        cmd_args = []
        if 'array' in logical_drive_info:
            cmd_args.extend(['array', logical_drive_info['array']])

        cmd_args.extend(['create', "type=logicaldrive"])

        if 'physical_disks' in logical_drive_info:
            phy_drive_ids = ','.join(logical_drive_info['physical_disks'])
            cmd_args.append("drives=%s" % phy_drive_ids)

        raid_level = logical_drive_info['raid_level']
        # For RAID levels (like 5+0 and 6+0), HPSSA names them differently.
        # Check if we have mapping stored, otherwise use the same.
        raid_level = constants.RAID_LEVEL_INPUT_TO_HPSSA_MAPPING.get(
            raid_level, raid_level)
        cmd_args.append("raid=%s" % raid_level)

        # If size_gb is MAX, then don't pass size argument.  HPSSA will
        # automatically allocate the maximum # disks size possible to the
        # logical disk.
        if logical_drive_info['size_gb'] != "MAX":
            size_mb = logical_drive_info['size_gb'] * 1024
            cmd_args.append("size=%s" % size_mb)

        self.execute_cmd(*cmd_args, process_input='y')

    def delete_all_logical_drives(self):
        """Deletes all logical drives on trh controller.

        This method deletes all logical drives on trh controller.
        :raises: HPSSAOperationError, if hpssacli/ssacli operation failed.
        """
        self.execute_cmd("logicaldrive", "all", "delete", "forced")

    def _get_erase_command(self, drive, pattern):
        """Return the command arguments based on the pattern.

        Erase command examples:
        1) Sanitize: "ssacli ctrl slot=0 pd 1I:1:1 modify erase
                      erasepattern=overwrite unrestricted=off forced"
        2) Zeros: "ssacli ctrl slot=0 pd 1I:1:1 modify erase
                   erasepattern=zero forced"

        :param drive: A string with comma separated list of drives.
        :param pattern: A string which defines the type of erase.
        :returns: A list of ssacli command arguments.
        """
        cmd_args = []
        cmd_args.append("pd %s" % drive)
        cmd_args.extend(['modify', 'erase', pattern])

        if pattern != 'erasepattern=zero':
            cmd_args.append('unrestricted=off')

        cmd_args.append('forced')
        return cmd_args

    def erase_devices(self, drives):
        """Perform Erase on all the drives in the controller.

        This method erases all the hdd and ssd drives in the controller
        by overwriting the drives with patterns for hdd and erasing storage
        blocks for ssd drives. The drives would be unavailable until after
        successful completion or failure.

        If the sanitize erase is not supported on any disk it will try to
        populate zeros on disk drives.

        :param drives: A list of drive objects in the controller.
        :raises: HPSSAOperationError, if sanitize erase is not supported.
        """
        for drive in drives:
            if drive.disk_type == constants.DISK_TYPE_HDD:
                LOG.debug("Disk erase running with erasepattern=overwrite on "
                          "disk: %s" % drive.id)
                cmd_args = self._get_erase_command(drive.id,
                                                   'erasepattern=overwrite')
            else:
                LOG.debug("Disk erase running with erasepattern=block on "
                          "disk: %s" % drive.id)
                cmd_args = self._get_erase_command(drive.id,
                                                   'erasepattern=block')
            stdout = self.execute_cmd(*cmd_args)

            if "not supported" in str(stdout):
                LOG.debug("Disk erase running with erasepattern=zero on "
                          "disk: %s" % drive.id)
                cmd_args = self._get_erase_command(drive.id,
                                                   'erasepattern=zero')
                self.execute_cmd(*cmd_args)


class RaidArray(object):
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

    def can_accomodate(self, logical_disk):
        """Check if this RAID array can accomodate the logical disk.

        This method uses hpssacli/ssacli command's option to check if the
        logical disk with desired size and RAID level can be created
        on this RAID array.

        :param logical_disk: Dictionary of logical disk to be created.
        :returns: True, if logical disk can be created on the RAID array
                  False, otherwise.
        """
        raid_level = constants.RAID_LEVEL_INPUT_TO_HPSSA_MAPPING.get(
            logical_disk['raid_level'], logical_disk['raid_level'])
        args = ("array", self.id, "create", "type=logicaldrive",
                "raid=%s" % raid_level, "size=?")

        if logical_disk['size_gb'] != "MAX":
            desired_disk_size = logical_disk['size_gb']
        else:
            desired_disk_size = constants.MINIMUM_DISK_SIZE

        try:
            stdout, stderr = self.parent.execute_cmd(
                *args, dont_transform_to_hpssa_exception=True)
        except processutils.ProcessExecutionError as ex:
            # hpssacli/ssacli returns error code 1 when RAID level of the
            # logical disk is not supported on the array.
            # If that's the case, just return saying the logical disk
            # cannot be accomodated in the array.
            # If exist_code is not 1, then it's some other error that we
            # don't expect to appear and hence raise it back.
            if ex.exit_code == 1:
                return False
            else:
                raise exception.HPSSAOperationError(reason=ex)
        except Exception as ex:
            raise exception.HPSSAOperationError(reason=ex)

        # TODO(rameshg87): This always returns in MB, but confirm with
        # HPSSA folks.
        match = re.search('Max: (\d+)', stdout)
        if not match:
            return False

        max_size_gb = int(match.group(1)) / 1024
        return desired_disk_size <= max_size_gb


class LogicalDrive(object):
    """Class for LogicalDrive object."""

    def __init__(self, id, properties, parent):
        """Constructor for a LogicalDrive object."""
        # Strip off 'Logical Drive' before storing it in id
        self.id = id[15:]
        self.parent = parent
        self.properties = properties

        # 'string_to_bytes' takes care of converting any returned
        # (like 500MB, 25GB) unit of storage space to bytes (Integer value).
        # It requires space to be stripped.
        try:
            size = self.properties['Size'].replace(' ', '')
            # TODO(rameshg87): Reduce the disk size by 1 to make sure Ironic
            # has enough space to write a config drive. Remove this when
            # Ironic doesn't need it.
            self.size_gb = int(strutils.string_to_bytes(size,
                                                        return_int=True) /
                               (1024*1024*1024)) - 1
        except KeyError:
            msg = ("Can't get 'Size' parameter from ssacli output for logical "
                   "disk '%(logical_disk)s' of RAID array '%(array)s' in "
                   "controller '%(controller)s'." %
                   {'logical_disk': self.id,
                    'array': self.parent.id,
                    'controller': self.parent.parent.id})
            raise exception.HPSSAOperationError(reason=msg)
        except ValueError:
            msg = ("ssacli returned unknown size '%(size)s' for logical "
                   "disk '%(logical_disk)s' of RAID array '%(array)s' in "
                   "controller '%(controller)s'." %
                   {'size': size, 'logical_disk': self.id,
                    'array': self.parent.id,
                    'controller': self.parent.parent.id})
            raise exception.HPSSAOperationError(reason=msg)

        self.raid_level = self.properties.get('Fault Tolerance')
        # For RAID levels (like 5+0 and 6+0), HPSSA names them differently.
        # Check if we have mapping stored, otherwise use the same.
        raid_level_mapping = constants.RAID_LEVEL_HPSSA_TO_INPUT_MAPPING
        self.raid_level = raid_level_mapping.get(self.raid_level,
                                                 self.raid_level)

        self.volume_name = self.properties.get('Logical Drive Label')

        # Trim down the WWN to 16 digits (8 bytes) so that it matches
        # lsblk output in Linux.
        wwn = self.properties.get('Unique Identifier')
        if wwn:
            wwn = '0x' + wwn[:16].lower()
            self.wwn = wwn

    def get_property(self, prop):
        if not self.properties:
            return None
        return self.properties.get(prop)

    def get_logical_drive_dict(self):

        physical_disk_ids = [x.id for x in self.parent.physical_drives]

        return {'size_gb': self.size_gb,
                'raid_level': self.raid_level,
                'root_device_hint': {'wwn': self.wwn},
                'controller': self.parent.parent.id,
                'physical_disks': physical_disk_ids,
                'volume_name': self.volume_name}


class PhysicalDrive(object):
    """Class for PhysicalDrive object."""

    def __init__(self, id, properties, parent):
        """Constructor for a PhysicalDrive object."""
        self.parent = parent
        self.properties = properties

        # Strip off physicaldrive before storing it in id
        self.id = id[14:]

        # 'string_to_bytes' takes care of converting any returned
        # (like 500MB, 25GB) unit of storage space to bytes (Integer value).
        # It requires space to be stripped.
        try:
            size = self.properties['Size'].replace(' ', '')
            self.size_gb = int(strutils.string_to_bytes(size,
                                                        return_int=True) /
                               (1024*1024*1024))
        except KeyError:
            msg = ("Can't get 'Size' parameter from ssacli output for "
                   "physical disk '%(physical_disk)s' of controller "
                   "'%(controller)s'." %
                   {'physical_disk': self.id,
                    'controller': self.parent.parent.id})
            raise exception.HPSSAOperationError(reason=msg)
        except ValueError:
            msg = ("ssacli returned unknown size '%(size)s' for physical "
                   "disk '%(physical_disk)s' of controller "
                   "'%(controller)s'." %
                   {'size': size, 'physical_disk': self.id,
                    'controller': self.parent.id})
            raise exception.HPSSAOperationError(reason=msg)

        try:
            ssa_interface = self.properties['Interface Type']
        except KeyError:
            msg = ("Can't get 'Interface Type' parameter from ssacli output "
                   "for physical disk '%(physical_disk)s' of controller "
                   "'%(controller)s'." %
                   {'physical_disk': self.id,
                    'controller': self.parent.parent.id})
            raise exception.HPSSAOperationError(reason=msg)

        self.interface_type = constants.get_interface_type(ssa_interface)
        self.disk_type = constants.get_disk_type(ssa_interface)
        self.model = self.properties.get('Model')
        self.firmware = self.properties.get('Firmware Revision')
        self.erase_status = self.properties.get('Status')

    def get_physical_drive_dict(self):
        """Returns a dictionary of with the details of the physical drive."""

        if isinstance(self.parent, RaidArray):
            controller = self.parent.parent.id
            status = 'active'
        else:
            controller = self.parent.id
            status = 'ready'

        return {'size_gb': self.size_gb,
                'controller': controller,
                'id': self.id,
                'disk_type': self.disk_type,
                'interface_type': self.interface_type,
                'model': self.model,
                'firmware': self.firmware,
                'status': status,
                'erase_status': self.erase_status}
