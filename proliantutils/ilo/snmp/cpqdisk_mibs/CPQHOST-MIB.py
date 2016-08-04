#
# PySNMP MIB module CPQHOST-MIB (http://pysnmp.sf.net)
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( sysName, ) = mibBuilder.importSymbols("SNMPv2-MIB", "sysName")
( Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, enterprises, iso, Gauge32, NotificationType, ModuleIdentity, ObjectIdentity, Bits, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "enterprises", "iso", "Gauge32", "NotificationType", "ModuleIdentity", "ObjectIdentity", "Bits", "Counter32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
compaq = MibIdentifier((1, 3, 6, 1, 4, 1, 232))
cpqHostOs = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11))
cpqHoMibRev = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 1))
cpqHoComponent = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2))
cpqHoInterface = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 1))
cpqHoInfo = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 2))
cpqHoUtil = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 3))
cpqHoFileSys = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 4))
cpqHoIfPhysMap = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 5))
cpqHoSWRunning = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 6))
cpqHoSwVer = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 7))
cpqHoGeneric = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 8))
cpqHoSwPerf = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 9))
cpqHoSystemStatus = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 10))
cpqHoTrapInfo = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 11))
cpqHoClients = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 12))
cpqHoMemory = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 13))
cpqHoFwVer = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 14))
cpqHoHWInfo = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 15))
cpqPwrThreshold = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 16))
cpqHoOsCommon = MibIdentifier((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4))
cpqHoMibRevMajor = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1,65535))).setMaxAccess("readonly")
cpqHoMibRevMinor = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoMibCondition = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 1, 3), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("unknown", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoOsCommonPollFreq = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readwrite")
cpqHoOsCommonModuleTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2), )
cpqHoOsCommonModuleEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoOsCommonModuleIndex"))
cpqHoOsCommonModuleIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,255))).setMaxAccess("readonly")
cpqHoOsCommonModuleName = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoOsCommonModuleVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,5))).setMaxAccess("readonly")
cpqHoOsCommonModuleDate = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoOsCommonModulePurpose = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 1, 4, 2, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoName = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoVersion = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoDesc = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoOsType = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 4), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,)).clone(namedValues=NamedValues(("other", 1), ("netware", 2), ("windowsnt", 3), ("sco-unix", 4), ("unixware", 5), ("os-2", 6), ("ms-dos", 7), ("dos-windows", 8), ("windows95", 9), ("windows98", 10), ("open-vms", 11), ("nsk", 12), ("windowsCE", 13), ("linux", 14), ("windows2000", 15), ("tru64UNIX", 16), ("windows2003", 17), ("windows2003-x64", 18), ("solaris", 19), ("windows2003-ia64", 20), ("windows2008", 21), ("windows2008-x64", 22), ("windows2008-ia64", 23), ("vmware-esx", 24), ("vmware-esxi", 25), ("windows2012", 26), ("windows7", 27), ("windows7-x64", 28), ("windows8", 29), ("windows8-x64", 30), ("windows81", 31), ("windows81-x64", 32), ("windowsxp", 33), ("windowsxp-x64", 34), ("windowsvista", 35), ("windowsvista-x64", 36), ("windows2008-r2", 37), ("windows2012-r2", 38), ("rhel", 39), ("rhel-64", 40), ("solaris-64", 41), ("sles", 42), ("sles-64", 43), ("ubuntu", 44), ("ubuntu-64", 45), ("debian", 46), ("debian-64", 47), ("linux-64-bit", 48), ("other-64-bit", 49), ("centos-32bit", 50), ("centos-64bit", 51), ("oracle-linux32", 52), ("oracle-linux64", 53), ("apple-osx", 54),))).setMaxAccess("readonly")
cpqHoTelnet = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 5), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3,)).clone(namedValues=NamedValues(("other", 1), ("available", 2), ("notavailable", 3),))).setMaxAccess("readonly")
cpqHoSystemRole = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,64))).setMaxAccess("readwrite")
cpqHoSystemRoleDetail = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 7), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,512))).setMaxAccess("readwrite")
cpqHoCrashDumpState = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 8), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("completememorydump", 1), ("kernelmemorydump", 2), ("smallmemorydump", 3), ("none", 4),))).setMaxAccess("readonly")
cpqHoCrashDumpCondition = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 9), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("other", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoCrashDumpMonitoring = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 10), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2,)).clone(namedValues=NamedValues(("enabled", 1), ("disabled", 2),))).setMaxAccess("readwrite")
cpqHoMaxLogicalCPUSupported = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoSystemName = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 12), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHosysDescr = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 2, 13), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoCpuUtilTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1), )
cpqHoCpuUtilEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoCpuUtilUnitIndex"))
cpqHoCpuUtilUnitIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoCpuUtilMin = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 2), Integer32()).setMaxAccess("readonly")
cpqHoCpuUtilFiveMin = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 3), Integer32()).setMaxAccess("readonly")
cpqHoCpuUtilThirtyMin = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 4), Integer32()).setMaxAccess("readonly")
cpqHoCpuUtilHour = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 5), Integer32()).setMaxAccess("readonly")
cpqHoCpuUtilHwLocation = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 3, 1, 1, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoFileSysTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1), )
cpqHoFileSysEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoFileSysIndex"))
cpqHoFileSysIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoFileSysDesc = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoFileSysSpaceTotal = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 3), Integer32()).setMaxAccess("readonly")
cpqHoFileSysSpaceUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 4), Integer32()).setMaxAccess("readonly")
cpqHoFileSysPercentSpaceUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 5), Integer32()).setMaxAccess("readonly")
cpqHoFileSysAllocUnitsTotal = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 6), Integer32()).setMaxAccess("readonly")
cpqHoFileSysAllocUnitsUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 7), Integer32()).setMaxAccess("readonly")
cpqHoFileSysStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 8), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("unknown", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoFileSysShortDesc = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 1, 1, 9), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoFileSysCondition = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 4, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("unknown", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoIfPhysMapTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1), )
cpqHoIfPhysMapEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoIfPhysMapIndex"))
cpqHoIfPhysMapIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoIfPhysMapSlot = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,255))).setMaxAccess("readonly")
cpqHoIfPhysMapIoBaseAddr = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 3), Integer32()).setMaxAccess("readonly")
cpqHoIfPhysMapIrq = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,255))).setMaxAccess("readonly")
cpqHoIfPhysMapDma = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 5), Integer32()).setMaxAccess("readonly")
cpqHoIfPhysMapMemBaseAddr = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 6), Integer32()).setMaxAccess("readonly")
cpqHoIfPhysMapPort = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 7), Integer32()).setMaxAccess("readonly")
cpqHoIfPhysMapDuplexState = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 8), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3,)).clone(namedValues=NamedValues(("other", 1), ("half", 2), ("full", 3),))).setMaxAccess("readonly")
cpqHoIfPhysMapCondition = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 1, 1, 9), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("other", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoIfPhysMapOverallCondition = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 5, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("other", 1), ("ok", 2), ("degraded", 3), ("failed", 4),))).setMaxAccess("readonly")
cpqHoSWRunningTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1), )
cpqHoSWRunningEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoSWRunningIndex"))
cpqHoSWRunningIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoSWRunningName = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoSWRunningDesc = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoSWRunningVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoSWRunningDate = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoSWRunningMonitor = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 6), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8,)).clone(namedValues=NamedValues(("other", 1), ("start", 2), ("stop", 3), ("startAndStop", 4), ("count", 5), ("startAndCount", 6), ("countAndStop", 7), ("startCountAndStop", 8),))).setMaxAccess("readonly")
cpqHoSWRunningState = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 7), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3,)).clone(namedValues=NamedValues(("other", 1), ("started", 2), ("stopped", 3),))).setMaxAccess("readonly")
cpqHoSWRunningCount = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoSWRunningCountMin = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readwrite")
cpqHoSWRunningCountMax = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readwrite")
cpqHoSWRunningEventTime = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 11), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoSWRunningStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 12), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5, 6, 7,)).clone(namedValues=NamedValues(("unknown", 1), ("normal", 2), ("warning", 3), ("minor", 4), ("major", 5), ("critical", 6), ("disabled", 7),))).setMaxAccess("readonly")
cpqHoSWRunningConfigStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 13), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5,)).clone(namedValues=NamedValues(("unknown", 1), ("starting", 2), ("initialized", 3), ("configured", 4), ("operational", 5),))).setMaxAccess("readonly")
cpqHoSWRunningIdentifier = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 14), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoSWRunningRedundancyMode = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 1, 1, 15), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("unknown", 1), ("master", 2), ("backup", 3), ("slave", 4),))).setMaxAccess("readonly")
cpqHoSwRunningTrapDesc = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 6, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoSwVerNextIndex = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 1), Integer32()).setMaxAccess("readonly")
cpqHoSwVerTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2), )
cpqHoSwVerEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoSwVerIndex"))
cpqHoSwVerIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoSwVerStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3,)).clone(namedValues=NamedValues(("other", 1), ("loaded", 2), ("notloaded", 3),))).setMaxAccess("readonly")
cpqHoSwVerType = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 3), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5, 6,)).clone(namedValues=NamedValues(("other", 1), ("driver", 2), ("agent", 3), ("sysutil", 4), ("application", 5), ("keyfile", 6),))).setMaxAccess("readwrite")
cpqHoSwVerName = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,127))).setMaxAccess("readwrite")
cpqHoSwVerDescription = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,127))).setMaxAccess("readwrite")
cpqHoSwVerDate = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoSwVerLocation = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 7), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readwrite")
cpqHoSwVerVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 8), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,50))).setMaxAccess("readonly")
cpqHoSwVerVersionBinary = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 2, 1, 9), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,50))).setMaxAccess("readonly")
cpqHoSwVerAgentsVer = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 7, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,50))).setMaxAccess("readonly")
cpqHoGenericData = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 8, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,254))).setMaxAccess("readwrite")
cpqHoCriticalSoftwareUpdateData = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 8, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,512))).setMaxAccess("readwrite")
cpqHoSwPerfAppErrorDesc = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 9, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,254))).setMaxAccess("readonly")
cpqHoMibStatusArray = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4,256))).setMaxAccess("readonly")
cpqHoConfigChangedDate = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoGUID = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16,17))).setMaxAccess("readwrite")
cpqHoCodeServer = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 4), Integer32()).setMaxAccess("readonly")
cpqHoWebMgmtPort = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 5), Integer32()).setMaxAccess("readonly")
cpqHoGUIDCanonical = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(32,36))).setMaxAccess("readwrite")
cpqHoMibHealthStatusArray = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 10, 7), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1,256))).setMaxAccess("readonly")
cpqHoTrapFlags = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 11, 1), Integer32()).setMaxAccess("readonly")
cpqHoClientLastModified = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(7,7)).setFixedLength(7)).setMaxAccess("readonly")
cpqHoClientDelete = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,15))).setMaxAccess("readwrite")
cpqHoClientTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3), )
cpqHoClientEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoClientIndex"))
cpqHoClientIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readonly")
cpqHoClientName = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,15))).setMaxAccess("readonly")
cpqHoClientIpxAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(20,20)).setFixedLength(20)).setMaxAccess("readonly")
cpqHoClientIpAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 4), IpAddress()).setMaxAccess("readonly")
cpqHoClientCommunity = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,48))).setMaxAccess("readonly")
cpqHoClientID = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 12, 3, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16,16)).setFixedLength(16)).setMaxAccess("readonly")
cpqHoPhysicalMemorySize = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 1), Integer32()).setMaxAccess("readonly")
cpqHoPhysicalMemoryFree = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 2), Integer32()).setMaxAccess("readonly")
cpqHoPagingMemorySize = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 3), Integer32()).setMaxAccess("readonly")
cpqHoPagingMemoryFree = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 4), Integer32()).setMaxAccess("readonly")
cpqHoBootPagingFileSize = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,10))).setMaxAccess("readonly")
cpqHoBootPagingFileMinimumSize = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,10))).setMaxAccess("readonly")
cpqHoBootPagingFileVolumeFreeSpace = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 13, 7), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,10))).setMaxAccess("readonly")
cpqHoFwVerTable = MibTable((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1), )
cpqHoFwVerEntry = MibTableRow((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1), ).setIndexNames((0, "CPQHOST-MIB", "cpqHoFwVerIndex"))
cpqHoFwVerIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 1), Integer32()).setMaxAccess("readonly")
cpqHoFwVerCategory = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5,)).clone(namedValues=NamedValues(("other", 1), ("storage", 2), ("nic", 3), ("rib", 4), ("system", 5),))).setMaxAccess("readonly")
cpqHoFwVerDeviceType = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 3), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,)).clone(namedValues=NamedValues(("other", 1), ("internalArrayController", 2), ("fibreArrayController", 3), ("scsiController", 4), ("fibreChannelTapeController", 5), ("modularDataRouter", 6), ("ideCdRomDrive", 7), ("ideDiskDrive", 8), ("scsiCdRom-ScsiAttached", 9), ("scsiDiskDrive-ScsiAttached", 10), ("scsiTapeDrive-ScsiAttached", 11), ("scsiTapeLibrary-ScsiAttached", 12), ("scsiDiskDrive-ArrayAttached", 13), ("scsiTapeDrive-ArrayAttached", 14), ("scsiTapeLibrary-ArrayAttached", 15), ("scsiDiskDrive-FibreAttached", 16), ("scsiTapeDrive-FibreAttached", 17), ("scsiTapeLibrary-FibreAttached", 18), ("scsiEnclosureBackplaneRom-ScsiAttached", 19), ("scsiEnclosureBackplaneRom-ArrayAttached", 20), ("scsiEnclosureBackplaneRom-FibreAttached", 21), ("scsiEnclosureBackplaneRom-ra4x00", 22), ("systemRom", 23), ("networkInterfaceController", 24), ("remoteInsightBoard", 25), ("sasDiskDrive-SasAttached", 26), ("sataDiskDrive-SataAttached", 27), ("usbController", 28), ("sasControllerAdapter", 29), ("sataControllerAdapter", 30), ("systemDevice", 31),))).setMaxAccess("readonly")
cpqHoFwVerDisplayName = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,127))).setMaxAccess("readonly")
cpqHoFwVerVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,31))).setMaxAccess("readonly")
cpqHoFwVerLocation = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoFwVerXmlString = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 7), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,255))).setMaxAccess("readonly")
cpqHoFwVerKeyString = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 8), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,127))).setMaxAccess("readonly")
cpqHoFwVerUpdateMethod = MibTableColumn((1, 3, 6, 1, 4, 1, 232, 11, 2, 14, 1, 1, 9), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4,)).clone(namedValues=NamedValues(("other", 1), ("noUpdate", 2), ("softwareflash", 3), ("replacePhysicalRom", 4),))).setMaxAccess("readonly")
cpqHoHWInfoPlatform = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 15, 1), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5,)).clone(namedValues=NamedValues(("unknown", 1), ("cellular", 2), ("foundation", 3), ("virtualMachine", 4), ("serverBlade", 5),))).setMaxAccess("readonly")
cpqPwrWarnType = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 16, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,254))).setMaxAccess("readwrite")
cpqPwrWarnThreshold = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 16, 2), Integer32()).setMaxAccess("readwrite")
cpqPwrWarnDuration = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 16, 3), Integer32()).setMaxAccess("readwrite")
cpqSerialNum = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 16, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,254))).setMaxAccess("readwrite")
cpqServerUUID = MibScalar((1, 3, 6, 1, 4, 1, 232, 11, 2, 16, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0,254))).setMaxAccess("readwrite")
cpqHoGenericTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11001)).setObjects(*(("CPQHOST-MIB", "cpqHoGenericData"),))
cpqHoAppErrorTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11002)).setObjects(*(("CPQHOST-MIB", "cpqHoSwPerfAppErrorDesc"),))
cpqHo2GenericTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11003)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoGenericData"),))
cpqHo2AppErrorTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11004)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoSwPerfAppErrorDesc"),))
cpqHo2NicStatusOk = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11005)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"),))
cpqHo2NicStatusFailed = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11006)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"),))
cpqHo2NicSwitchoverOccurred = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11007)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"),))
cpqHo2NicStatusOk2 = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11008)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"), ("CPQHOST-MIB", "cpqHoIfPhysMapPort"),))
cpqHo2NicStatusFailed2 = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11009)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"), ("CPQHOST-MIB", "cpqHoIfPhysMapPort"),))
cpqHo2NicSwitchoverOccurred2 = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11010)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"), ("CPQHOST-MIB", "cpqHoIfPhysMapPort"), ("CPQHOST-MIB", "cpqHoIfPhysMapSlot"), ("CPQHOST-MIB", "cpqHoIfPhysMapPort"),))
cpqHoProcessEventTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11011)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoSwRunningTrapDesc"),))
cpqHoProcessCountWarning = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11012)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoSWRunningName"), ("CPQHOST-MIB", "cpqHoSWRunningCount"), ("CPQHOST-MIB", "cpqHoSWRunningCountMin"), ("CPQHOST-MIB", "cpqHoSWRunningCountMax"), ("CPQHOST-MIB", "cpqHoSWRunningEventTime"),))
cpqHoProcessCountNormal = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11013)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoSWRunningName"), ("CPQHOST-MIB", "cpqHoSWRunningCount"), ("CPQHOST-MIB", "cpqHoSWRunningCountMin"), ("CPQHOST-MIB", "cpqHoSWRunningCountMax"), ("CPQHOST-MIB", "cpqHoSWRunningEventTime"),))
cpqHoCriticalSoftwareUpdateTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11014)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoCriticalSoftwareUpdateData"),))
cpqHoCrashDumpNotEnabledTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11015)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoCrashDumpState"),))
cpqHoBootPagingFileTooSmallTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11016)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoCrashDumpState"), ("CPQHOST-MIB", "cpqHoBootPagingFileSize"), ("CPQHOST-MIB", "cpqHoBootPagingFileMinimumSize"),))
cpqHoSWRunningStatusChangeTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11017)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoSWRunningName"), ("CPQHOST-MIB", "cpqHoSWRunningDesc"), ("CPQHOST-MIB", "cpqHoSwRunningTrapDesc"), ("CPQHOST-MIB", "cpqHoSWRunningVersion"), ("CPQHOST-MIB", "cpqHoSWRunningStatus"), ("CPQHOST-MIB", "cpqHoSWRunningConfigStatus"), ("CPQHOST-MIB", "cpqHoSWRunningIdentifier"), ("CPQHOST-MIB", "cpqHoSWRunningRedundancyMode"),))
cpqHo2PowerThresholdTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11018)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqPwrWarnType"), ("CPQHOST-MIB", "cpqPwrWarnThreshold"), ("CPQHOST-MIB", "cpqPwrWarnDuration"), ("CPQHOST-MIB", "cpqSerialNum"), ("CPQHOST-MIB", "cpqServerUUID"),))
cpqHoBootPagingFileOrFreeSpaceTooSmallTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11019)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoCrashDumpState"), ("CPQHOST-MIB", "cpqHoBootPagingFileSize"), ("CPQHOST-MIB", "cpqHoBootPagingFileVolumeFreeSpace"), ("CPQHOST-MIB", "cpqHoBootPagingFileMinimumSize"),))
cpqHoMibHealthStatusArrayChangeTrap = NotificationType((1, 3, 6, 1, 4, 1, 232) + (0,11020)).setObjects(*(("CPQHOST-MIB", "sysName"), ("CPQHOST-MIB", "cpqHoTrapFlags"), ("CPQHOST-MIB", "cpqHoMibHealthStatusArray"),))
mibBuilder.exportSymbols("CPQHOST-MIB", cpqHoUtil=cpqHoUtil, cpqHoFileSysTable=cpqHoFileSysTable, cpqHoFileSysDesc=cpqHoFileSysDesc, cpqHoFileSys=cpqHoFileSys, cpqHoClientIndex=cpqHoClientIndex, cpqHoOsCommonModuleDate=cpqHoOsCommonModuleDate, cpqHoProcessCountWarning=cpqHoProcessCountWarning, cpqHoAppErrorTrap=cpqHoAppErrorTrap, cpqHoCodeServer=cpqHoCodeServer, cpqHoMibRevMinor=cpqHoMibRevMinor, cpqHoTelnet=cpqHoTelnet, cpqHo2NicStatusFailed=cpqHo2NicStatusFailed, cpqHoIfPhysMapPort=cpqHoIfPhysMapPort, cpqHoMibHealthStatusArrayChangeTrap=cpqHoMibHealthStatusArrayChangeTrap, cpqHoFwVerXmlString=cpqHoFwVerXmlString, cpqHoSwVer=cpqHoSwVer, cpqHoPhysicalMemoryFree=cpqHoPhysicalMemoryFree, cpqHoInfo=cpqHoInfo, cpqHoCrashDumpCondition=cpqHoCrashDumpCondition, cpqHoOsCommonModulePurpose=cpqHoOsCommonModulePurpose, cpqHoSwPerfAppErrorDesc=cpqHoSwPerfAppErrorDesc, cpqHoComponent=cpqHoComponent, cpqHoSWRunningTable=cpqHoSWRunningTable, cpqHoGeneric=cpqHoGeneric, cpqHoSWRunningEventTime=cpqHoSWRunningEventTime, cpqHoSWRunningCount=cpqHoSWRunningCount, cpqHoSWRunningRedundancyMode=cpqHoSWRunningRedundancyMode, cpqHoSwVerDate=cpqHoSwVerDate, cpqHoTrapFlags=cpqHoTrapFlags, cpqHosysDescr=cpqHosysDescr, cpqHoCrashDumpMonitoring=cpqHoCrashDumpMonitoring, cpqPwrThreshold=cpqPwrThreshold, cpqHoOsCommonModuleIndex=cpqHoOsCommonModuleIndex, cpqHoCpuUtilHwLocation=cpqHoCpuUtilHwLocation, cpqHoIfPhysMapMemBaseAddr=cpqHoIfPhysMapMemBaseAddr, cpqSerialNum=cpqSerialNum, cpqHoSWRunningStatus=cpqHoSWRunningStatus, cpqHoSwVerVersionBinary=cpqHoSwVerVersionBinary, cpqHoOsCommonModuleVersion=cpqHoOsCommonModuleVersion, cpqHoMemory=cpqHoMemory, cpqHoBootPagingFileOrFreeSpaceTooSmallTrap=cpqHoBootPagingFileOrFreeSpaceTooSmallTrap, cpqHoBootPagingFileVolumeFreeSpace=cpqHoBootPagingFileVolumeFreeSpace, cpqHo2PowerThresholdTrap=cpqHo2PowerThresholdTrap, cpqHoFileSysAllocUnitsUsed=cpqHoFileSysAllocUnitsUsed, cpqHoSWRunning=cpqHoSWRunning, cpqHoSWRunningName=cpqHoSWRunningName, cpqHoOsCommonModuleName=cpqHoOsCommonModuleName, cpqHoSWRunningIdentifier=cpqHoSWRunningIdentifier, cpqHoPhysicalMemorySize=cpqHoPhysicalMemorySize, cpqHoCpuUtilUnitIndex=cpqHoCpuUtilUnitIndex, cpqHoMibRev=cpqHoMibRev, cpqHoFileSysPercentSpaceUsed=cpqHoFileSysPercentSpaceUsed, cpqHoCrashDumpNotEnabledTrap=cpqHoCrashDumpNotEnabledTrap, cpqHoCpuUtilFiveMin=cpqHoCpuUtilFiveMin, cpqHoIfPhysMapTable=cpqHoIfPhysMapTable, cpqHoMibHealthStatusArray=cpqHoMibHealthStatusArray, cpqHoSwVerDescription=cpqHoSwVerDescription, cpqHoSystemRoleDetail=cpqHoSystemRoleDetail, cpqHoFileSysSpaceTotal=cpqHoFileSysSpaceTotal, cpqPwrWarnDuration=cpqPwrWarnDuration, cpqHoSwVerType=cpqHoSwVerType, cpqHoIfPhysMapDuplexState=cpqHoIfPhysMapDuplexState, cpqHoFwVerCategory=cpqHoFwVerCategory, cpqHoIfPhysMapDma=cpqHoIfPhysMapDma, cpqHoGenericTrap=cpqHoGenericTrap, cpqHoSWRunningEntry=cpqHoSWRunningEntry, cpqHoHWInfo=cpqHoHWInfo, cpqHoClientCommunity=cpqHoClientCommunity, cpqHoSystemStatus=cpqHoSystemStatus, cpqHoInterface=cpqHoInterface, cpqHo2NicStatusOk2=cpqHo2NicStatusOk2, cpqHoClientDelete=cpqHoClientDelete, cpqHoSWRunningStatusChangeTrap=cpqHoSWRunningStatusChangeTrap, cpqHoVersion=cpqHoVersion, cpqHoIfPhysMapCondition=cpqHoIfPhysMapCondition, cpqHoConfigChangedDate=cpqHoConfigChangedDate, cpqHo2NicSwitchoverOccurred=cpqHo2NicSwitchoverOccurred, cpqHoFwVerDeviceType=cpqHoFwVerDeviceType, cpqHoFwVerKeyString=cpqHoFwVerKeyString, cpqHoProcessCountNormal=cpqHoProcessCountNormal, cpqHoIfPhysMapOverallCondition=cpqHoIfPhysMapOverallCondition, cpqHoClientName=cpqHoClientName, cpqHoClientTable=cpqHoClientTable, cpqHoMaxLogicalCPUSupported=cpqHoMaxLogicalCPUSupported, cpqHoClientLastModified=cpqHoClientLastModified, cpqHoFwVerLocation=cpqHoFwVerLocation, cpqHoMibCondition=cpqHoMibCondition, cpqHoClientEntry=cpqHoClientEntry, cpqHo2GenericTrap=cpqHo2GenericTrap, cpqHoCpuUtilHour=cpqHoCpuUtilHour, cpqHostOs=cpqHostOs, cpqHoCriticalSoftwareUpdateData=cpqHoCriticalSoftwareUpdateData, cpqServerUUID=cpqServerUUID, cpqHoIfPhysMapIrq=cpqHoIfPhysMapIrq, cpqHoSystemName=cpqHoSystemName, cpqHoClientIpAddress=cpqHoClientIpAddress, cpqPwrWarnThreshold=cpqPwrWarnThreshold, cpqHoSystemRole=cpqHoSystemRole, cpqHoHWInfoPlatform=cpqHoHWInfoPlatform, cpqHo2NicStatusOk=cpqHo2NicStatusOk, cpqHoIfPhysMapSlot=cpqHoIfPhysMapSlot, cpqHoTrapInfo=cpqHoTrapInfo, cpqHoFileSysShortDesc=cpqHoFileSysShortDesc, cpqHoCpuUtilTable=cpqHoCpuUtilTable, cpqHoOsCommon=cpqHoOsCommon, cpqHoIfPhysMapIndex=cpqHoIfPhysMapIndex, cpqHoPagingMemorySize=cpqHoPagingMemorySize, cpqHoBootPagingFileSize=cpqHoBootPagingFileSize, cpqHoFileSysEntry=cpqHoFileSysEntry, cpqHoOsType=cpqHoOsType, cpqHoClientIpxAddress=cpqHoClientIpxAddress, cpqHoSwVerEntry=cpqHoSwVerEntry, cpqHoMibRevMajor=cpqHoMibRevMajor, cpqHoOsCommonModuleEntry=cpqHoOsCommonModuleEntry, cpqHoPagingMemoryFree=cpqHoPagingMemoryFree, cpqHoCpuUtilMin=cpqHoCpuUtilMin, cpqHoFwVerTable=cpqHoFwVerTable, cpqHoSWRunningIndex=cpqHoSWRunningIndex, cpqHoMibStatusArray=cpqHoMibStatusArray, cpqHoSwVerNextIndex=cpqHoSwVerNextIndex, cpqHo2AppErrorTrap=cpqHo2AppErrorTrap, cpqHoOsCommonModuleTable=cpqHoOsCommonModuleTable, cpqHoSWRunningState=cpqHoSWRunningState, cpqHoGUIDCanonical=cpqHoGUIDCanonical, cpqHoProcessEventTrap=cpqHoProcessEventTrap, cpqHoSwVerTable=cpqHoSwVerTable, cpqHoSWRunningDesc=cpqHoSWRunningDesc, cpqHoIfPhysMapIoBaseAddr=cpqHoIfPhysMapIoBaseAddr, cpqHoSwVerAgentsVer=cpqHoSwVerAgentsVer, cpqHoSWRunningCountMin=cpqHoSWRunningCountMin, cpqHoOsCommonPollFreq=cpqHoOsCommonPollFreq, cpqHoFileSysCondition=cpqHoFileSysCondition, cpqHoCpuUtilEntry=cpqHoCpuUtilEntry, cpqHoSWRunningMonitor=cpqHoSWRunningMonitor, cpqHoGenericData=cpqHoGenericData, cpqHoSWRunningVersion=cpqHoSWRunningVersion, cpqHoFwVerEntry=cpqHoFwVerEntry, cpqHoSwVerName=cpqHoSwVerName, cpqHoFwVerIndex=cpqHoFwVerIndex, cpqHoClientID=cpqHoClientID, cpqHoSwVerLocation=cpqHoSwVerLocation, cpqHoBootPagingFileMinimumSize=cpqHoBootPagingFileMinimumSize, cpqHoFwVerUpdateMethod=cpqHoFwVerUpdateMethod, cpqHoSWRunningCountMax=cpqHoSWRunningCountMax, cpqHoSwVerIndex=cpqHoSwVerIndex, cpqHoDesc=cpqHoDesc, cpqHoFileSysIndex=cpqHoFileSysIndex, cpqHoGUID=cpqHoGUID, cpqHo2NicSwitchoverOccurred2=cpqHo2NicSwitchoverOccurred2, cpqHoSwVerStatus=cpqHoSwVerStatus, cpqHoFileSysStatus=cpqHoFileSysStatus, cpqHoSwPerf=cpqHoSwPerf, cpqHoFwVerVersion=cpqHoFwVerVersion, cpqHoFwVer=cpqHoFwVer, cpqHoCrashDumpState=cpqHoCrashDumpState, cpqHoCriticalSoftwareUpdateTrap=cpqHoCriticalSoftwareUpdateTrap, cpqHoIfPhysMapEntry=cpqHoIfPhysMapEntry, cpqHo2NicStatusFailed2=cpqHo2NicStatusFailed2, cpqHoCpuUtilThirtyMin=cpqHoCpuUtilThirtyMin, cpqHoFileSysSpaceUsed=cpqHoFileSysSpaceUsed, compaq=compaq, cpqHoWebMgmtPort=cpqHoWebMgmtPort, cpqHoSWRunningConfigStatus=cpqHoSWRunningConfigStatus, cpqHoSwVerVersion=cpqHoSwVerVersion, cpqHoName=cpqHoName, cpqHoFwVerDisplayName=cpqHoFwVerDisplayName, cpqHoSWRunningDate=cpqHoSWRunningDate, cpqPwrWarnType=cpqPwrWarnType, cpqHoIfPhysMap=cpqHoIfPhysMap, cpqHoBootPagingFileTooSmallTrap=cpqHoBootPagingFileTooSmallTrap, cpqHoClients=cpqHoClients, cpqHoFileSysAllocUnitsTotal=cpqHoFileSysAllocUnitsTotal, cpqHoSwRunningTrapDesc=cpqHoSwRunningTrapDesc)
