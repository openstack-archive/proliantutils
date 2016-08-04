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

import os

from pysnmp import hlapi
from pysnmp.smi import builder
from pysnmp.smi import view

from proliantutils import exception
from proliantutils import log

LOG = log.get_logger(__name__)

cpq_mibs_path = os.path.dirname(os.path.abspath(__file__))
cpq_mibs_path = os.path.join(cpq_mibs_path, "cpqdisk_mibs")
mBuilder = builder.MibBuilder()
mBuilder.addMibSources(builder.DirMibSource(cpq_mibs_path))
mibBuilder = mBuilder.loadModules('CPQIDA-MIB', 'CPQSCSI-MIB')
mibViewController = view.MibViewController(mibBuilder)

# A dictionary of supported mapped snmp attributes
MAPPED_SNMP_ATTRIBUTES = {
    'authProtocol': {
        'SHA': hlapi.usmHMACSHAAuthProtocol,
        'MD5': hlapi.usmHMACMD5AuthProtocol,
    },
    'privProtocol': {
        'AES': hlapi.usmAesCfb128Protocol,
        'DES': hlapi.usmDESPrivProtocol,
    },
}


def _get_mapped_snmp_value(key, value):
    """Parses the auth protocol and privacy protocols.

    :param key: either 'authProtocol' or 'privProtocol'
    :param value: protocol value.
    :returns the corresponding hlapi value.
    """
    return MAPPED_SNMP_ATTRIBUTES.get(key).get(value)


def _parse_mibs(iLOIP, auth_user, auth_protocol, auth_prot_pp,
                priv_protocol, auth_priv_pp):
    """Parses the MIBs.

    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :param auth_user: SNMP user
    :param auth_protocol: Auth Protocol
    :param auth_prot_pp: Pass phrase value for AuthProtocol.
    :param priv_protocol:Privacy Protocol.
    :param auth_priv_pp: Pass phrase value for Privacy Protocol.
    :returns the dictionary of parsed MIBs.
    :raises exception.InvalidInputError if pysnmp is unable to get
            SNMP data due to wrong inputs provided.
    :raises exception.IloError if pysnmp raises any exception.
    """
    result = {}
    try:
        for(errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in hlapi.nextCmd(
                hlapi.SnmpEngine(),
                hlapi.UsmUserData(auth_user, auth_prot_pp,
                                  auth_priv_pp, authProtocol=auth_protocol,
                                  privProtocol=priv_protocol),
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
                msg = "SNMP failed to traverse MIBs %s", errorIndication
                raise exception.IloSNMPInvalidInputFailure(msg)
            else:
                if errorStatus:
                    msg = ('Parsing MIBs failed. %s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[-1][int(errorIndex)-1]
                        or '?'
                        )
                    )
                    LOG.debug(msg)
                    raise exception.IloSNMPInvalidInputFailure(msg)
                else:
                    for varBindTableRow in varBinds:
                        name, val = tuple(varBindTableRow)
                        oid, label, suffix = (
                            mibViewController.getNodeName(name))
                        key = name.prettyPrint()
                        # Don't traverse outside the tables we requested
                        if not (key.find("SNMPv2-SMI::enterprises.232.3") >= 0
                                or (key.find(
                                    "SNMPv2-SMI::enterprises.232.5") >= 0)):
                            break
                        if key not in result:
                            result[key] = {}
                            result[key][label[-1]] = {}
                        result[key][label[-1]][suffix] = val
    except Exception as e:
        msg = "SNMP library failed with error %s", e
        LOG.debug(msg)
        raise exception.IloSNMPExceptionFailure(msg)
    return result


def _get_disksize_MiB(iLOIP, snmp_credentials):
    """Reads the dictionary of parsed MIBs and gets the disk size.

    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :param snmp_credentials in a dictionary having following mandatory
           keys.
           auth_user: SNMP user
           auth_protocol: Auth Protocol
           auth_prot_pp: Pass phrase value for AuthProtocol.
           priv_protocol:Privacy Protocol.
           auth_priv_pp: Pass phrase value for Privacy Protocol.

    :returns the dictionary of disk sizes of all physical drives.
    """
    # '1.3.6.1.4.1.232.5.5.1.1',  # cpqscsi SAS HBA Table
    # '1.3.6.1.4.1.232.3.2.3.1',  # cpqida Drive Array Logical Drive Table
    auth_user = snmp_credentials.get('auth_user')
    auth_prot_pp = snmp_credentials.get('auth_prot_pp')
    auth_priv_pp = snmp_credentials.get('auth_priv_pp')
    auth_Prot = _get_mapped_snmp_value('authProtocol',
                                       snmp_credentials['auth_protocol'])
    priv_Prot = _get_mapped_snmp_value('privProtocol',
                                       snmp_credentials['priv_protocol'])
    result = _parse_mibs(iLOIP, auth_user, auth_protocol=auth_Prot,
                         auth_prot_pp=auth_prot_pp,
                         priv_protocol=priv_Prot,
                         auth_priv_pp=auth_priv_pp)
    disksize = {}
    for uuid in sorted(result):
        for key in result[uuid]:
            # We only track the Physical Disk Size
            if key.find('PhyDrvSize') >= 0:
                disksize[uuid] = dict()
                for suffix in sorted(result[uuid][key]):
                    size = result[uuid][key][suffix]
                    disksize[uuid][key] = str(size)
    return disksize


def get_local_gb(iLOIP, snmp_credentials):
    """Gets the maximum disk size among all disks.

    :param iLOIP: IP address of the server on which SNMP discovery
                  has to be executed.
    :param snmp_credentials in a dictionary having following mandatory
           keys.
           auth_user: SNMP user
           auth_protocol: Auth Protocol
           auth_prot_pp: Pass phrase value for AuthProtocol.
           priv_protocol:Privacy Protocol.
           auth_priv_pp: Pass phrase value for Privacy Protocol.
    """
    disk_sizes = _get_disksize_MiB(iLOIP, snmp_credentials)
    max_size = 0
    for uuid in disk_sizes:
        for key in disk_sizes[uuid]:
            if int(disk_sizes[uuid][key]) > max_size:
                max_size = int(disk_sizes[uuid][key])
    max_size_gb = max_size/1024
    return max_size_gb
