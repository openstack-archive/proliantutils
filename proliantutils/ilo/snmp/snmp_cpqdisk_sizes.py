#!/usr/bin/env python
# Copyright 2017 Hewlett-Packard Enterprise Development Company, L.P.
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
import os

from pysnmp import hlapi
from pysnmp.smi import builder
from pysnmp.smi import view

import proliantutils.ilo.snmp as proliant_snmp
from proliantutils import exception
from proliantutils import log

LOG = log.get_logger(__name__)

cpq_mibs_path = os.path.dirname(inspect.getfile(proliant_snmp))
cpq_mibs_path = cpq_mibs_path + "/cpqdisk_mibs"
mBuilder = builder.MibBuilder()
mBuilder.addMibSources(builder.DirMibSource(cpq_mibs_path))
mibBuilder = mBuilder.loadModules('CPQIDA-MIB', 'CPQSCSI-MIB')
mibViewController = view.MibViewController(mibBuilder)


def _parse_auth_protocol(auth_protocol):
    """Parses the auth protocol and assigns the value accordingly.

    :param auth_protocol: The protocol value either `SHA` or `MD5` or None.
    :returns corresponding protocol value for SNMP.
    """
    auth_Prot = hlapi.usmNoAuthProtocol
    if auth_protocol == 'SHA':
        auth_Prot = hlapi.usmHMACSHAAuthProtocol
    elif auth_protocol == 'MD5':
        auth_Prot = hlapi.usmHMACMD5AuthProtocol
    return auth_Prot


def _parse_privacy_protocol(priv_protocol):
    """Parses the privacy protocol and assigns the value accordingly.

    :param priv_protocol: The protocol value either `AES` or `DES` or None.
    :returns corresponding protocol value for SNMP.
    """
    priv_Prot = hlapi.usmNoPrivProtocol
    if priv_protocol == "AES":
        priv_Prot = hlapi.usmAesCfb128Protocol
    elif priv_protocol == "DES":
        priv_Prot = hlapi.usmDESPrivProtocol
    return priv_Prot


def _parse_mibs(auth_user, auth_prot_pp, auth_priv_pp,
                auth_protocol, priv_protocol, iLOIP):
    """Parses the MIBs.

    :param auth_user: SNMP user
    :param auth_prot_pp: Pass phrase value for AuthProtocol.
    :param auth_priv_pp: Pass phrase value for Privacy Protocol.
    :param auth_protocol: Auth Protocol
    :param priv_protocol:Privacy Protocol.
    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :returns the dictionary of parsed MIBs.
    """
    result = dict()
    try:
        for(errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in hlapi.nextCmd(
                hlapi.SnmpEngine(),
                hlapi.UsmUserData(auth_user, auth_prot_pp,
                                  auth_priv_pp, auth_protocol=auth_protocol,
                                  priv_protocol=priv_protocol),
                hlapi.UdpTransportTarget((iLOIP, 161), timeout=3, retries=3),
                hlapi.ContextData(),
                # cpqida cpqDaPhyDrvTable Drive Array Physical Drive Table
                hlapi.ObjectType(
                    hlapi.ObjectIdentity('1.3.6.1.4.1.232.3.2.5.1')),
                # cpqscsi SCSI Physical Drive Table
                hlapi.ObjectType(
                    hlapi.ObjectIdentity('1.3.6.1.4.1.232.5.2.4.1')),
                # cpqscsi SAS Physical Drive Table
                hlapi.ObjectType(
                    hlapi.ObjectIdentity('1.3.6.1.4.1.232.5.5.2.1')),
                lexicographicMode=False,
                ignoreNonIncreasingOid=True):

            if errorIndication:
                LOG.error(errorIndication)
            else:
                if errorStatus:
                    msg = ('Parsing MIBs failed. %s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[-1][int(errorIndex)-1]
                        or '?'
                        )
                    )
                    LOG.error(msg)
                    raise exception.InvalidInputError(msg)
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
    except Exception:
        raise 
    return result


def _get_disksize_MiB(iLOIP, auth_user, auth_prot_pp,
                      auth_priv_pp, auth_protocol, priv_protocol):
    """Reads the dictionary of parsed MIBs and gets the disk size.

    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :param auth_user: SNMP user
    :param auth_prot_pp: Pass phrase value for AuthProtocol.
    :param auth_priv_pp: Pass phrase value for Privacy Protocol.
    :param auth_protocol: Auth Protocol
    :param priv_protocol:Privacy Protocol.
    :returns the dictionary of disk sizes of all physical drives.
    """
    # '1.3.6.1.4.1.232.5.5.1.1',  # cpqscsi SAS HBA Table
    # '1.3.6.1.4.1.232.3.2.3.1',  # cpqida Drive Array Logical Drive Table
    auth_Prot = _parse_auth_protocol(auth_protocol)
    priv_Prot = _parse_privacy_protocol(priv_protocol)
    result = _parse_mibs(auth_user, auth_prot_pp, auth_priv_pp,
                        auth_Prot, priv_Prot, iLOIP)
    disksize = dict()
    for uuid in sorted(result):
        for key in result[uuid]:
            # We only track the Physical Disk Size
            if key.find('PhyDrvSize') >= 0:
                disksize[uuid] = dict()
                for suffix in sorted(result[uuid][key]):
                    size = int(result[uuid][key][suffix])/1024
                    disksize[uuid][key] = str(size)
    return disksize


def get_local_gb(iLOIp, auth_user, auth_prot_pp, auth_priv_pp, auth_protocol,
                 priv_protocol):
    """Gets the maximum size.

    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :param auth_user: SNMP user
    :param auth_prot_pp: Pass phrase value for AuthProtocol.
    :param auth_priv_pp: Pass phrase value for Privacy Protocol.
    :param auth_protocol: Auth Protocol
    :param priv_protocol:Privacy Protocol.
    """
    disk_sizes = _get_disksize_MiB(iLOIp, auth_user, auth_prot_pp,
                                  auth_priv_pp, auth_protocol, priv_protocol)
    max_size = 0
    for uuid in disk_sizes:
        for key in disk_sizes[uuid]:
            if int(disk_sizes[uuid][key]) > max_size:
                max_size = int(disk_sizes[uuid][key])
    return max_size
