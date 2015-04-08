# coding=utf-8

# Copyright 2012 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2012 NTT DOCOMO, INC.
# Copyright 2014 International Business Machines Corporation
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

"""
NOTE THAT CERTAIN DISTROS MAY INSTALL openipmi BY DEFAULT, INSTEAD OF ipmitool,
WHICH PROVIDES DIFFERENT COMMAND-LINE OPTIONS AND *IS NOT SUPPORTED* BY THIS
DRIVER.
"""

import subprocess


def _exec_ipmitool(driver_info, command):
    """Execute the ipmitool command.

    This uses the lanplus interface to communicate with the BMC device driver.

    :param driver_info: the ipmitool parameters for accessing a node.
    :param command: the ipmitool command to be executed.

    """
    ipmi_cmd = ("ipmitool -H %(address)s"
                " -I lanplus -U %(user)s -P %(passwd)s %(cmd)s"
                % {'address': driver_info['address'],
                   'user': driver_info['username'],
                   'passwd': driver_info['password'],
                   'cmd': command})

    out = None
    try:
        out = subprocess.check_output(ipmi_cmd, shell=True)
    except Exception:
        pass
    return out


def get_nic_capacity(driver_info):
    """Gets the FRU data to see if it is NIC data

    Gets the FRU data in loop from 0-255 FRU Ids
    and check if the returned data is NIC data. Couldn't
    find any easy way to detect if it is NIC data. We should't be
    hardcoding the FRU Id.

    :param driver_info: Contains the access credentials to access
                        the BMC.
    :returns: the max capacity supported by the NIC adapter.
    """
    i = 0
    value = None
    while i < 255:
        cmd = "fru print %s" % hex(i)
        out = _exec_ipmitool(driver_info, cmd)
        if out and 'port' in out:
            value = _parse_ipmi_nic_capacity(out)
        i = i + 1
    if value:
        return value


def _parse_ipmi_nic_capacity(nic_out):
    """Parse the FRU output for NIC capacity

    Parses the FRU output. Seraches for the key "Product Name"
    in FRU output and greps for maximum speed supported by the
    NIC adapter.

    :param nic_out: the FRU output for NIC adapter.
    :returns: the max capacity supported by the NIC adapter.

    """
    if (("Device not present" in nic_out)
       or ("Unknown FRU header" in nic_out) or not nic_out):
        return None

    capacity = None
    product_name = None
    data = nic_out.split('\n')
    for item in data:
        key = item.split(':')
        if len(key) > 1:
            if "Product Name" in key[0]:
                product_name = key[1]

    if product_name:
        product_name_array = product_name.split(' ')
        for item in product_name_array:
            if 'Gb' in item:
                capacity = item

    return capacity
