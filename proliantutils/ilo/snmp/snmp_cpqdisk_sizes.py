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

from pysnmp import hlapi
from pysnmp.smi import builder
from pysnmp.smi import view

import proliantutils.ilo.snmp as proliant_snmp

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
    """Parses the auth protocol and assigns the value accordingly.

    :param authProtocol: The protocol value either `SHA` or `MD5` or None.
    :returns corresponding protocol value for SNMP.
    """
    auth_Prot = hlapi.usmNoAuthProtocol
    if authProtocol == 'SHA':
        auth_Prot = hlapi.usmHMACSHAAuthProtocol
    elif authProtocol == 'MD5':
        auth_Prot = hlapi.usmHMACMD5AuthProtocol
    return auth_Prot


def parse_privacy_protocol(privProtocol):
    """Parses the privacy protocol and assigns the value accordingly.

    :param privProtocol: The protocol value either `AES` or `DES` or None.
    :returns corresponding protocol value for SNMP.
    """
    priv_Prot = hlapi.usmNoPrivProtocol
    if privProtocol == "AES":
        priv_Prot = hlapi.usmAesCfb128Protocol
    elif privProtocol == "DES":
        priv_Prot = hlapi.usmDESPrivProtocol
    return priv_Prot


def parse_mibs(authUser, authProtocolPassPhrase, authPrivPassPhrase,
               auth_Prot, priv_Prot, iLOIP):
    """Parses the MIBs.

    :param authUser: SNMP user
    :param authProtocolPassPhrase: Pass phrase value for AuthProtocol.
    :param authPrivPassPhrase: Pass phrase value for Privacy Protocol.
    :param auth_Prot: Auth Protocol
    :param priv_Prot:Privacy Protocol.
    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :returns the dictionary of parsed MIBs.
    """
    result = dict()
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in hlapi.nextCmd(
            hlapi.SnmpEngine(),
            hlapi.UsmUserData(authUser, authProtocolPassPhrase,
                              authPrivPassPhrase, authProtocol=auth_Prot,
                              privProtocol=priv_Prot),
            hlapi.UdpTransportTarget((iLOIP, 161), timeout=3, retries=3),
            hlapi.ContextData(),
            # cpqida cpqDaPhyDrvTable Drive Array Physical Drive Table
            hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.4.1.232.3.2.5.1')),
            # cpqscsi SCSI Physical Drive Table
            hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.4.1.232.5.2.4.1')),
            # cpqscsi SAS Physical Drive Table
            hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.4.1.232.5.5.2.1')),
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
    """Reads the dictionary of parsed MIBs and gets the disk size.

    :param authUser: SNMP user
    :param authProtocolPassPhrase: Pass phrase value for AuthProtocol.
    :param authPrivPassPhrase: Pass phrase value for Privacy Protocol.
    :param authProtocol: Auth Protocol
    :param privProtocol:Privacy Protocol.
    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :returns the dictionary of disk sizes of all physical drives.
    """
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
    """Gets the maximum size.

    :param authUser: SNMP user
    :param authProtocolPassPhrase: Pass phrase value for AuthProtocol.
    :param authPrivPassPhrase: Pass phrase value for Privacy Protocol.
    :param authProtocol: Auth Protocol
    :param privProtocol:Privacy Protocol.
    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    """
    disk_sizes = get_disksize_MiB(iLOIp, authUser, authProtValue,
                                  privProtValue, authProtocol, privProtocol)
    max_size = 0
    for uuid in disk_sizes:
        for key in disk_sizes[uuid]:
            if int(disk_sizes[uuid][key]) > max_size:
                max_size = int(disk_sizes[uuid][key])
    return max_size
