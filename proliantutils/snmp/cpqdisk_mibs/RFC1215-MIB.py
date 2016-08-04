#
# PySNMP MIB module RFC1215-MIB (http://pysnmp.sf.net)
# ASN.1 source file:///home/jman/src/github-hpe.com/jman/snmp/upd10.40mib/rfc-1215.mib
# Produced by pysmi-0.0.7 at Tue Jun 21 15:58:20 2016
# On host Gen9Test26 platform Linux version 3.13.0-24-generic by user jman
# Using Python version 2.7.9 (default, May 18 2016, 21:34:57) 
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( ifIndex, ) = mibBuilder.importSymbols("IF-MIB", "ifIndex")
( egpNeighAddr, ) = mibBuilder.importSymbols("RFC1213-MIB", "egpNeighAddr")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, mib_2, IpAddress, TimeTicks, Counter64, Unsigned32, iso, Gauge32, ModuleIdentity, ObjectIdentity, Bits, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "mib-2", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "iso", "Gauge32", "ModuleIdentity", "ObjectIdentity", "Bits", "Counter32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
snmp = MibIdentifier((1, 3, 6, 1, 2, 1, 11))
coldStart = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,0)).setObjects(*())
warmStart = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,1)).setObjects(*())
linkDown = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,2)).setObjects(*(("RFC1215-MIB", "ifIndex"),))
linkUp = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,3)).setObjects(*(("RFC1215-MIB", "ifIndex"),))
authenticationFailure = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,4)).setObjects(*())
egpNeighborLoss = NotificationType((1, 3, 6, 1, 2, 1, 11) + (0,5)).setObjects(*(("RFC1215-MIB", "egpNeighAddr"),))
mibBuilder.exportSymbols("RFC1215-MIB", linkDown=linkDown, authenticationFailure=authenticationFailure, warmStart=warmStart, egpNeighborLoss=egpNeighborLoss, snmp=snmp, linkUp=linkUp, coldStart=coldStart)
