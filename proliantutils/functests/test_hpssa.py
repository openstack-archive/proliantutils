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
import glob
import os
import stat

from oslo_concurrency import processutils
import testtools

from proliantutils.hpssa import constants
from proliantutils.hpssa import manager
from proliantutils.hpssa import objects


class HPSSATestCase(testtools.TestCase):

    def tearDown(self):
        super(HPSSATestCase, self).tearDown()
        manager.delete_configuration()

    def _get_server(self):

        server = objects.Server()
        return server

    def _get_physical_drives(self, server, no_of_physical_drives_required,
                             size_gb_required):

        for controller in server.controllers:
            physical_drives = [x for x in controller.unassigned_physical_drives
                               if x.size_gb >= size_gb_required]
            if len(physical_drives) >= no_of_physical_drives_required:
                break
        else:
            self.fail("This test requires a controller with atleast %d "
                      "physical drives on the server" %
                      no_of_physical_drives_required)

        return physical_drives[:no_of_physical_drives_required]

    def _test_create_configuration_single_logical_drive(self, raid_level):

        server = self._get_server()
        size_gb = 100

        manager.delete_configuration()
        devices_before_create = set(glob.glob('/dev/sd[a-z]'))

        minimum_disks_required = constants.RAID_LEVEL_MIN_DISKS[raid_level]
        self._get_physical_drives(server, minimum_disks_required, size_gb)

        raid_config = {
            'logical_disks': [{'size_gb': size_gb, 'raid_level': raid_level}]}

        current_config = manager.create_configuration(raid_config)

        logical_disk = current_config['logical_disks'][0]
        self.assertIsNotNone(logical_disk['root_device_hint'])
        self.assertIsNotNone(logical_disk['volume_name'])

        devices_after_create = set(glob.glob('/dev/sd[a-z]'))
        new_device = devices_after_create - devices_before_create

        # Make sure only one new device appeared now.
        if len(new_device) != 1:
            self.fail("More than 1 block devices were found after "
                      "creating RAID volume")

        new_device_file = new_device.pop()
        s = os.stat(new_device_file)
        if not stat.S_ISBLK(s.st_mode):
            self.fail("Newly created disk %s is not a block device"
                      % new_device_file)

        # SCSI disk devices have major number 8
        # https://www.kernel.org/doc/Documentation/devices.txt
        # TODO(rameshg87: Need to check if any more assetions need to be
        # done on the newly created disk device.
        self.assertEqual(8, os.major(s.st_rdev))

        stdout, stderr = processutils.execute("lsblk", "-Pio", "SIZE",
                                              new_device_file)
        # Output is like (two times printed):
        # SIZE="8G"
        # SIZE="8G"
        created_disk_size = stdout.split("\n")[0].split('"')[1][:-1]
        self.assertEqual(size_gb, int(created_disk_size))

        stdout, stderr = processutils.execute("lsblk", "-Pio", "WWN",
                                              new_device_file)
        # Output is like:
        # WWN="0x600508b1001cca7f"
        # TODO(rameshg87: Check with ssa team whether this can be
        # assumed.
        wwn = stdout.split("\n")[0].split('"')[1]
        self.assertEqual(logical_disk['root_device_hint']['wwn'], wwn)

        manager.delete_configuration()

    def test_raid_0_single_drive(self):
        self._test_create_configuration_single_logical_drive('0')

    def test_raid_1_single_drive(self):
        self._test_create_configuration_single_logical_drive('1')

    def test_raid_5_single_drive(self):
        self._test_create_configuration_single_logical_drive('5')

    def test_raid_6_single_drive(self):
        self._test_create_configuration_single_logical_drive('6')

    def test_raid_10_single_drive(self):
        self._test_create_configuration_single_logical_drive('1+0')

    def test_raid_50_single_drive(self):
        self._test_create_configuration_single_logical_drive('5+0')

    def test_raid_60_single_drive(self):
        self._test_create_configuration_single_logical_drive('6+0')
