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

from oslo.concurrency import processutils
import testtools

from proliantutils.hpssa import manager
from proliantutils.hpssa import objects


class HPSSATestCase(testtools.TestCase):

    def tearDown(self):
        super(HPSSATestCase, self).tearDown()
        manager.delete_configuration()

    def _get_server(self):

        server = objects.Server()
        if not server.controllers:
            self.fail("No controllers detected on the server.")
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

    def test_create_configuration_single_logical_drive(self):

        server = self._get_server()
        size_gb = 100

        manager.delete_configuration()
        devices_before_create = set(glob.glob('/dev/sd[a-z]'))

        for raid_level in ['0', '1', '5', '6']:
            self._get_physical_drives(server, 2, size_gb)

            raid_config = {
                'logical_disks':
                    [{'size_gb': size_gb,
                      'raid_level': raid_level}]
            }

            current_config = manager.create_configuration(raid_config)

            logical_disk = current_config['logical_disks'][0]
            self.assertIsNotNone(logical_disk['root_device_hint'])
            self.assertIsNotNone(logical_disk['volume_name'])

            devices_after_create = set(glob.glob('/dev/sd[a-z]'))
            new_device = devices_after_create - devices_before_create
            new_device_file = new_device.pop()

            s = os.stat(new_device_file)
            if not stat.S_ISBLK(s.st_mode):
                self.fail("Newly created disk %s is not a block device"
                          % new_device_file)

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
            wwn = stdout.split("\n")[0].split('"')[1]
            self.assertEqual(logical_disk['root_device_hint']['wwn'], wwn)

            manager.delete_configuration()
