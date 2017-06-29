# Copyright 2017 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import mock
import testtools

from proliantutils.redfish.resources.system import memory


class MemoryTestCase(testtools.TestCase):

    def setUp(self):
        super(MemoryTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/rdimm.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        self.mem_inst = memory.Memory(
            self.conn, '/redfish/v1/Systems/1/Memory/proc1dimm12/',
            redfish_version='1.0.2')

    def test_attributes(self):
        self.assertEqual('proc1dimm12',
                         self.mem_inst.identity)
        self.assertEqual('proc1dimm12',
                         self.mem_inst.name)
        self.assertEqual(72,
                         self.mem_inst.bus_width_bits)
        self.assertEqual(32768,
                         self.mem_inst.capacity_mib)
        self.assertEqual('PROC 1 DIMM 12',
                         self.mem_inst.device_locator)
        self.assertEqual('DDR4',
                         self.mem_inst.memory_device_type)
        self.assertEqual(["DRAM"],
                         self.mem_inst.memory_media)
        self.assertEqual('DRAM',
                         self.mem_inst.memory_type)
        self.assertEqual(2400,
                         self.mem_inst.operating_speed_mhz)
        self.assertEqual('52736',
                         self.mem_inst.vendor_id)


class MemoryCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(MemoryCollectionTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = (
                json.loads(f.read()))

        self.mem_col_inst = memory.MemoryCollection(
            self.conn, '/redfish/v1/Systems/1/Memory/',
            redfish_version='1.0.2')

    def test_memory_data_nvdimm_n(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_nvdimm.json', 'r') as f:
            mem1 = (
                json.loads(f.read())['default'])
        self.conn.get.return_value.json.return_value = mem1
        exp_value = {'persistent_memory': True,
                     'nvdimm_n': True,
                     'logical_nvdimm_n': False}
        ret = self.mem_col_inst.memory_data()
        self.assertEqual(ret, exp_value)

    def test_memory_data_logical(self):
        with open('proliantutils/tests/redfish/'
                  'json_samples/logical_nvdimm.json', 'r') as f:
            mem1 = (
                json.loads(f.read())['logical_nvdimm'])
        self.conn.get.return_value.json.return_value = mem1
        exp_value = {'persistent_memory': True,
                     'nvdimm_n': True,
                     'logical_nvdimm_n': True}
        ret = self.mem_col_inst.memory_data()
        self.assertEqual(ret, exp_value)
