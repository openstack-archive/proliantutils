# Copyright 2014 Hewlett-Packard Development Company, L.P.
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


"""Test Utils for iLO test modules."""

NIC_FRU_OUT = (
    "Board Mfg Date        : Mon Apr 28 23:16:00 2014\n"
    "Board Mfg             : HP\n"
    "Board Product         : HP Ethernet 1Gb 4-port 331FLR Adapter\n"
    "Board Serial          : CN84170RX5\n"
    "Board Part Number     : 634025-001\n"
    "Board Extra           : d23041\n"
    "Board Extra           : d5629133b001\n"
    "Product Manufacturer  : HP\n"
    "Product Name          : HP Ethernet 1Gb 4-port 331FLR Adapter\n"
    "Product Part Number   : 629135-B21\n"
    "Product Version       : 00\n"
    "Product Serial        : CN84170RX5")

NIC_FRU_OUT_NO_PORT_DETAILS = (
    "Board Mfg Date        : Mon Apr 28 23:16:00 2014\n"
    "Board Mfg             : HP\n"
    "Board Serial          : CN84170RX5\n"
    "Board Part Number     : 634025-001\n"
    "Board Extra           : d23041\n"
    "Board Extra           : d5629133b001\n"
    "Product Manufacturer  : HP\n"
    "Product Part Number   : 629135-B21\n"
    "Product Version       : 00\n"
    "Product Serial        : CN84170RX5")

NIC_FRU_OUT_NO_PRODUCT_NAME = (
    "Board Mfg Date        : Mon Apr 28 23:16:00 2014\n"
    "Board Mfg             : HP\n"
    "Board Product         : HP Ethernet 1Gb 4-port 331FLR Adapter\n"
    "Board Serial          : CN84170RX5\n"
    "Board Part Number     : 634025-001\n"
    "Board Extra           : d23041\n"
    "Board Extra           : d5629133b001\n"
    "Product Manufacturer  : HP\n"
    "Product Part Number   : 629135-B21\n"
    "Product Version       : 00\n"
    "Product Serial        : CN84170RX5")

NIC_FRU_OUT_ALL = (
    "FRU Device Description : Builtin FRU Device (ID 0)"
    "Chassis Type          : Rack Mount Chassis"
    "Chassis Serial        : 2M24500B4F"
    "Board Mfg Date        : Sat Mar 26 00:00:00 2005"
    "Board Mfg             : HP"
    "Board Product         : ProLiant DL180 Gen9"
    "Board Serial          : 2M24500B4F"
    "Board Part Number     : 754524-B21"
    "Product Manufacturer  : HP"
    "Product Name          : ProLiant DL180 Gen9"
    "Product Part Number   : 754524-B21"
    "Product Serial        : 2M24500B4F"

    "FRU Device Description : BMC CONTROLLER (ID 238)"
    "Product Manufacturer  : HP"
    "Product Name          : BMC CONTROLLER"
    "Product Part Number   : iLO 4"

    "FRU Device Description : MB BIOS (ID 239)"
    "Product Manufacturer  : HP"
    "Product Name          : SYSTEM BIOS"
    "Product Part Number   : U20"
    "Product Version       : 11/03/2014"
    "Board Mfg Date        : Mon Apr 28 23:16:00 2014\n"
    "Board Mfg             : HP\n"
    "Board Product         : HP Ethernet 1Gb 4-port 331FLR Adapter\n"
    "Board Serial          : CN84170RX5\n"
    "Board Part Number     : 634025-001\n"
    "Board Extra           : d23041\n"
    "Board Extra           : d5629133b001\n"
    "Product Manufacturer  : HP\n"
    "Product Part Number   : 629135-B21\n"
    "Product Version       : 00\n"
    "Product Serial        : CN84170RX5"

    "FRU Device Description : CPU 1 (ID 16)"
    "Product Manufacturer  : Intel(R) Corporation"
    "Product Name          : Intel(R) Xeon(R) CPU E5-2603 v3 @ 1.60GHz"

    "FRU Device Description : CPU 1 DIMM 6 (ID 110)"
    "Device not present (Command response could not be provided)"

    "FRU Device Description : CPU 1 DIMM 8 (ID 111)"
    "Device not present (Command response could not be provided)")


LESSER_THAN_MIN_SUGGESTED_FW_STR = 2.25
MIN_SUGGESTED_FW_STR = 2.30
GREATER_THAN_MIN_SUGGESTED_FW_STR = 2.35
