#!/usr/bin/env python
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

__author__ = 'HPE'

import inspect
import logging
import os

from pysnmp.hlapi import ContextData
from pysnmp.hlapi import nextCmd
from pysnmp.hlapi import ObjectIdentity
from pysnmp.hlapi import ObjectType
from pysnmp.hlapi import SnmpEngine
from pysnmp.hlapi import UdpTransportTarget
from pysnmp.hlapi import usmAesCfb128Protocol
from pysnmp.hlapi import usmDESPrivProtocol
from pysnmp.hlapi import usmHMACMD5AuthProtocol
from pysnmp.hlapi import usmHMACSHAAuthProtocol
from pysnmp.hlapi import usmNoAuthProtocol
from pysnmp.hlapi import usmNoPrivProtocol
from pysnmp.hlapi import UsmUserData
from pysnmp.smi import builder
from pysnmp.smi import view

import proliantutils.snmp as proliant_snmp

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(lineno)d %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

cpq_mibs_path = os.path.dirname(inspect.getfile(proliant_snmp))
cpq_mibs_path = cpq_mibs_path + "/cpqdisk_mibs"
mBuilder = builder.MibBuilder()
mBuilder.addMibSources(builder.DirMibSource(cpq_mibs_path))
mibBuilder = mBuilder.loadModules('CPQIDA-MIB', 'CPQSCSI-MIB')
mibViewController = view.MibViewController(mibBuilder)


def parse_auth_protocol(authProtocol):
    auth_Prot = usmNoAuthProtocol
    if authProtocol == 'SHA':
        auth_Prot = usmHMACSHAAuthProtocol
    elif authProtocol == 'MD5':
        auth_Prot = usmHMACMD5AuthProtocol
    return auth_Prot


def parse_privacy_protocol(privProtocol):
    priv_Prot = usmNoPrivProtocol
    if privProtocol == "AES":
        priv_Prot = usmAesCfb128Protocol
    elif privProtocol == "DES":
        priv_Prot = usmDESPrivProtocol
    return priv_Prot


def parse_mibs(authUser, authProtocolPassPhrase, authPrivPassPhrase,
               auth_Prot, priv_Prot, iLOIP):
    result = dict()
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(
            SnmpEngine(),
            UsmUserData(authUser, authProtocolPassPhrase, authPrivPassPhrase,
                        authProtocol=auth_Prot, privProtocol=priv_Prot),
            UdpTransportTarget((iLOIP, 161), timeout=3, retries=3),
            ContextData(),
            # cpqida cpqDaPhyDrvTable Drive Array Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.3.2.5.1')),
            # cpqscsi SCSI Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.5.2.4.1')),
            # cpqscsi SAS Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.5.5.2.1')),
            lexicographicMode=False,
            ignoreNonIncreasingOid=True):

        if errorIndication:
            log.error(errorIndication)
        else:
            if errorStatus:
                log.error('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                for varBindTableRow in varBinds:
                    name, val = tuple(varBindTableRow)
                    oid, label, suffix = mibViewController.getNodeName(name)
                    key = name.prettyPrint()
                    # Don't traverse outside the tables we requested
                    if not (key.find("SNMPv2-SMI::enterprises.232.3") >= 0 or
                            key.find("SNMPv2-SMI::enterprises.232.5") >= 0):
                        break
                    if key not in result:
                        result[key] = dict()
                        result[key][label[-1]] = dict()
                    result[key][label[-1]][suffix] = val
    return result


def get_disksize_MiB(iLOIP, authUser, authProtocolPassPhrase,
                     authPrivPassPhrase, authProtocol, privProtocol):
    # '1.3.6.1.4.1.232.5.5.1.1',  # cpqscsi SAS HBA Table
    # '1.3.6.1.4.1.232.3.2.3.1',  # cpqida Drive Array Logical Drive Table
    auth_Prot = parse_auth_protocol(authProtocol)
    priv_Prot = parse_privacy_protocol(privProtocol)
    result = parse_mibs(authUser, authProtocolPassPhrase, authPrivPassPhrase,
                        auth_Prot, priv_Prot, iLOIP)
    disksize = dict()
    maxsize = 0
    aggregatesize = 0
    lineno = 1
    for uuid in sorted(result):
        for key in result[uuid]:
            for suffix in sorted(result[uuid][key]):
                log.debug('%-3d %s/%s = %s' % (lineno, uuid, key, result
                          [uuid][key][suffix]))
                lineno += 1
            # We only track the Physical Disk Size
            if key.find('PhyDrvSize') >= 0:
                disksize[uuid] = dict()
                for suffix in sorted(result[uuid][key]):
                    size = result[uuid][key][suffix]/1024
                    if size > maxsize:
                        maxsize = size
                    disksize[uuid][key] = str(size)
                    aggregatesize += size
                    log.debug("%-50s %s %-6s %s MiB %s GiB" % (
                              uuid, key, suffix, result[uuid][key][suffix],
                              result[uuid][key][suffix]/1024))
    return disksize


def get_local_gb(iLOIp, authUser, authProtValue, privProtValue, authProtocol,
                 privProtocol):
    disk_sizes = get_disksize_MiB(iLOIp, authUser, authProtValue,
                                  privProtValue, authProtocol, privProtocol)
    max_size = 0
    for uuid in disk_sizes:
        for key in disk_sizes[uuid]:
            if disk_sizes[uuid][key] > max_size:
                max_size = disk_sizes[uuid][key]
    return max_size
