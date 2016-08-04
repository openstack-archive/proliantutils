#!/usr/bin/env python
# from pysnmp.entity.rfc3413.oneliner import cmdgen
import optparse
from pysnmp.smi import builder, view
from pysnmp.hlapi import *
import logging
import os
import inspect
import proliantutils.snmp as proliant_snmp

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(lineno)d %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

cpq_mibs_path = os.path.dirname(inspect.getfile(proliant_snmp))
cpq_mibs_path = cpq_mibs_path + "/cpqdisk_mibs"
mBuilder = builder.MibBuilder()
mBuilder.addMibSources(builder.DirMibSource(cpq_mibs_path))
#mBuilder.addMibSources(builder.DirMibSource("proliantutils/snmp/cpqdisk_mibs"))
# print(mBuilder.getMibSources())
mibBuilder = mBuilder.loadModules('CPQIDA-MIB', 'CPQSCSI-MIB')
mibViewController = view.MibViewController(mibBuilder)


def get_disksize_MiB(iLOIP, iLOReadCommunities):
    # '1.3.6.1.4.1.232.5.5.1.1',  # cpqscsi SAS HBA Table
    # '1.3.6.1.4.1.232.3.2.3.1',  # cpqida Drive Array Logical Drive Table
    log.info("iLO %s ReadCommunity %s", iLOIP, iLOReadCommunities)
    result = dict()
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(iLOReadCommunities),
            UdpTransportTarget((iLOIP, 161), timeout=3, retries=3),
            ContextData(),
            # cpqida cpqDaPhyDrvTable Drive Array Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.3.2.5.1')),
            # cpqscsi SCSI Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.5.2.4.1')),
            # cpqscsi SAS Physical Drive Table
            ObjectType(ObjectIdentity('1.3.6.1.4.1.232.5.5.2.1')),
            # lookupNames=True,
            # lookupValues=True,
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
            if key.find('PhyDrvSize') >= 0:  # or key.find('LogDrvSize') >= 0:
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
    #log.info("AggregateDiskSize %.2f TiB", aggregatesize/(1024*1024))
    log.info("AggregateDiskSize %.2f TiB", aggregatesize/(1024))
    return disksize
    #return (disksize, str(aggregatesize/1024))


def main(iloip, snmprc):
    #parse = optparse.OptionParser()
    #parse.add_option('--iloip', type='string',
    #                 dest='iloip',
    #                 help='IP address of iLO',
    #                 default='172.30.102.222')

    #parse.add_option('--snmprc', type='string',
    #                 dest='snmprc',
    #                 help='SNMP Read Community String',
    #                 default='zTKeKi')

    #(opts, _) = parse.parse_args(sys.argv)

    #(disk_sizes, totalGiB) = get_disksize_MiB(opts.iloip, opts.snmprc)
    (disk_sizes, totalGiB) = get_disksize_MiB(iloip, snmprc)
    print("AggregateDiskSize %s GiB" % totalGiB)
    for uuid in disk_sizes:
        for key in disk_sizes[uuid]:
            print("%s %s MiB" % (key, disk_sizes[uuid][key]))
    return disk_sizes
if __name__ == '__main__':
    import sys
    sys.exit(main("10.10.1.52", "zTKeKi"))
