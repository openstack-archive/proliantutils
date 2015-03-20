# Copyright 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Flake doesn't allow files without anything. Remove on first commit.
MODULE = "RIS"

HTTP_BOOT_URL = {
    "UefiShellStartupUrl": "http://10.10.1.30:8081/startup.nsh"
    }

RESPONSE_BODY_FOR_REST_OP = """
{
    "AssetTag": "",
    "AvailableActions": [
        {
            "Action": "Reset",
            "Capabilities": [
                {
                    "AllowableValues": [
                        "On",
                        "ForceOff",
                        "ForceRestart",
                        "Nmi",
                        "PushPowerButton"
                    ],
                    "PropertyName": "ResetType"
                }
            ]
        }
    ],
    "Bios": {
        "Current": {
            "VersionString": "I36 v1.40 (01/28/2015)"
        }
    },
    "Boot": {
        "BootSourceOverrideEnabled": "Disabled",
        "BootSourceOverrideSupported": [
            "None",
            "Cd",
            "Hdd",
            "Usb",
            "Utilities",
            "Diags",
            "BiosSetup",
            "Pxe",
            "UefiShell",
            "UefiTarget"
        ],
        "BootSourceOverrideTarget": "None",
        "UefiTargetBootSourceOverride": "None",
        "UefiTargetBootSourceOverrideSupported": [
            "HD.Emb.1.2",
            "Generic.USB.1.1",
            "NIC.FlexLOM.1.1.IPv4",
            "NIC.FlexLOM.1.1.IPv6",
            "CD.Virtual.2.1"
        ]
    },
    "Description": "Computer System View",
    "HostCorrelation": {
        "HostMACAddress": [
            "6c:c2:17:39:fe:80",
            "6c:c2:17:39:fe:88"
        ],
        "HostName": "",
        "IPAddress": [
            "",
            ""
        ]
    },
    "IndicatorLED": "Off",
    "Manufacturer": "HP",
    "Memory": {
        "TotalSystemMemoryGB": 16
    },
    "Model": "ProLiant BL460c Gen9",
    "Name": "Computer System",
    "Oem": {
        "Hp": {
            "AvailableActions": [
                {
                    "Action": "PowerButton",
                    "Capabilities": [
                        {
                            "AllowableValues": [
                                "Press",
                                "PressAndHold"
                            ],
                            "PropertyName": "PushType"
                        },
                        {
                            "AllowableValues": [
                                "/Oem/Hp"
                            ],
                            "PropertyName": "Target"
                        }
                    ]
                },
                {
                    "Action": "SystemReset",
                    "Capabilities": [
                        {
                            "AllowableValues": [
                                "ColdBoot"
                            ],
                            "PropertyName": "ResetType"
                        },
                        {
                            "AllowableValues": [
                                "/Oem/Hp"
                            ],
                            "PropertyName": "Target"
                        }
                    ]
                }
            ],
            "Battery": [],
            "Bios": {
                "Backup": {
                    "Date": "v1.40 (01/28/2015)",
                    "Family": "I36",
                    "VersionString": "I36 v1.40 (01/28/2015)"
                },
                "Current": {
                    "Date": "01/28/2015",
                    "Family": "I36",
                    "VersionString": "I36 v1.40 (01/28/2015)"
                },
                "UefiClass": 2
            },
            "DeviceDiscoveryComplete": {
                "AMSDeviceDiscovery": "NoAMS",
                "SmartArrayDiscovery": "Initial",
                "vAuxDeviceDiscovery": "DataIncomplete",
                "vMainDeviceDiscovery": "ServerOff"
            },
            "PostState": "PowerOff",
            "PowerAllocationLimit": 500,
            "PowerAutoOn": "PowerOn",
            "PowerOnDelay": "Minimum",
            "PowerRegulatorMode": "Dynamic",
            "PowerRegulatorModesSupported": [
                "OSControl",
                "Dynamic",
                "Max",
                "Min"
            ],
            "ServerSignature": 0,
            "Type": "HpComputerSystemExt.0.10.1",
            "VirtualProfile": "Inactive",
            "VirtualUUID": null,
            "links": {
                "BIOS": {
                    "href": "/rest/v1/systems/1/bios"
                },
                "MEMORY": {
                    "href": "/rest/v1/Systems/1/Memory"
                },
                "PCIDevices": {
                    "href": "/rest/v1/Systems/1/PCIDevices"
                },
                "PCISlots": {
                    "href": "/rest/v1/Systems/1/PCISlots"
                },
                "SecureBoot": {
                    "href": "/rest/v1/Systems/1/SecureBoot"
                }
            }
        }
    },
    "Power": "Off",
    "Processors": {
        "Count": 1,
        "ProcessorFamily": "Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz",
        "Status": {
            "HealthRollUp": "OK"
        }
    },
    "SKU": "727021-B21",
    "SerialNumber": "SGH449WNL3",
    "Status": {
        "Health": "OK",
        "State": "Disabled"
    },
    "SystemType": "Physical",
    "Type": "ComputerSystem.0.9.6",
    "UUID": "30373237-3132-4753-4834-3439574E4C33",
    "links": {
        "Chassis": [
            {
                "href": "/rest/v1/Chassis/1"
            }
        ],
        "Logs": {
            "href": "/rest/v1/Systems/1/Logs"
        },
        "ManagedBy": [
            {
                "href": "/rest/v1/Managers/1"
            }
        ],
        "self": {
            "href": "/rest/v1/Systems/1"
        }
    }
}
"""

BASE64_GZIPPED_RESPONSE = """
H4sIAHN9ClUC/+1YW2/iOBR+51dEeZqR2pAQCoWnhUALGm5qSndXoz6YYMAaEyPHoWVH/e9r50JJ7ARajVbzsH0p8rnZ5xx/53MqPysa/9M7QQDZI1jrbU3Xr5K1PUAYLDDseAwRP+Cy75FE/P08/op1IxVh/QC5p8TFUeyAHVggjBiCWTdqd+9uMSYvYgtPAIcFpkflqZ8Lm5HeEerB6Wp1VocfgAHKyvQmW1QmnoXBZkZeIO2GjPGsKDWf1Q70GSU7SNlhArbwmM/Hww7Kbt4yK8+V7HoSQO8iIhL3nmHdCSmFPsssRoInSANeRpdR5EetMLQb2t4y6qb2xbSqtdtqzbRuvuq5SG9pJEKyTqMVl4Qi83tIKVrCvi/KuRTOeyiIf1+VGbjhbkcoi0yyxdcnxIdSpy3zK4OltDQPFtISS9szJ+ghsJYWRU5dyMJdXjB7lXY0hyvkbiDGKsEjoGt+XSqKrlDkItFuS0c/8SVbfVS/JOODntHfLgzLqOUPcw99SJFnzN0uF1t58WToGHcYvo6mYyE2hrN9/QKdhlTenvGEKAsBNmo8SiXb/Gkj9mDgUbRLIckh213IINXcQ8DgVntC8CUFuQEJmEP4fcAgUT9pXyEcd5zOcklhIKOP3vDaXq1tNdt2q72C7Vszv928wq260iJOet9PqzScFYbORypKxdBfIg8wQkf9nnD/joD6GPjhCngspJAK0WB2lMAtoYdsLh4JAzhOYCy+73IFq5GJNiZLiIUvjmIjBHymdUf1hulpvD1aqff0pLmypOIp/5mtwk5GqtLZdG6oHGfVKUgXwPHZyVUe7FOT7GQWiNpfXajY8ZcDgpd6qfpzuTdp/IhZpp4+xxlw9Z/mpMr7o8pb4peeMg/D5ZNWnrgluTjbhHH3q2jT79GEDu+paLL/0oyX0Jr/G+v5HNXL0xHAOI4KwP7+rGAqEnwmRt6PcKeUxUMUsOgICv5X0KZ3YIvwIeGNRUof5pgl7VDIZKVDvHv+fTYvOJiDQTTda5USbc5n9siDnC97hHO0gxicGEYHU9S1M3Zz+jEB5OuKY+nulj92OpSCQ0Z/6HO0AVhlse+Er4oIPNVg6Hvp3lSGY4B8haULKf8pmElpFmacJbksKWg0uuXnXLwu7r8X8bkR2iLRHjemqVQMGZm+UwHpBZku9zg9jLY6Rj7ahlul2gNch1hQLcGCoowcfN5U3nnloJhyx5TIdYjPKFGWQx0lYXivymWUe5PmQSMuiIvWPhDskG8qn70IuQVn3KUsLh5j/VdmmIZlyi+AhLZzgFwhDOMW4+QT7WGB5nw+FIzVDzHOKWDk/ygCteHULUaDDYUrEbnK6RKr7q1qEG06qFrVhcDJi67tuD+ePvz9gSDuMUjCqy8KM3OG8VUJPhXqxPzScC4m7NPBYuOLQrnQ400lfSy4NNiJ+Zkx+VbwnSK6gLnHEO9LnquA0Py3EhJG88U6eZYddU9mhs8g/vLwVfsLEl/8d2ZzrX9zXWuYLW1va39oltEy7wf/nD7vBJiFcsb1AQSYbR4IxvNdtM1vRV9c3G9zodCsNc2add2tpbdO3GCO3pNwu4hP6t4P6vXWn5ORfdSQgyeBk5C5jcLMJ5vsLqLapJAw2xwC/uRMseoIFVmg4CjRMtI5qyd3XbdNu2nX7Oa1bdm163rzxr6u39r1a7tut26a9X7dsY8HkFFAdzZ8miKZ7ymAQmqwxLZq6QU9dPpgH5G1om4lTRsZVBS3QrzCwRouu4dP7Tq2phduO4B49ZFtS21Xeav8C14gvWoyFgAA
"""

HEADERS_FOR_REST_OP = [('content-length', '2729'),
                       ('server', 'HP-iLO-Server/1.30'),
                       ('etag', 'W/"B61EB245"'),
                       ('allow', 'GET, HEAD, POST, PATCH'),
                       ('cache-control', 'no-cache'),
                       ('date', 'Thu, 19 Mar 2015 06:55:59 GMT'),
                       ('x_hp-chrp-service-version', '1.0.3'),
                       ('content-type', 'application/json')]

COLLECTIONS_SAMPLE = """
{
    "Description": "iLO User Accounts",
    "links": {
        "Member": [
            {
                "href": "/rest/v1/AccountService/Accounts/1"
            }
        ],
        "self": {
            "href": "/rest/v1/AccountService/Accounts"
        }
    },
    "Items": [
        {
            "UserName": "Administrator",
            "Description": "iLO User Account",
            "links": {
                "self": {
                    "href": "/rest/v1/AccountService/Accounts/1"
                }
            },
            "Oem": {
                "Hp": {
                    "Privileges": {
                        "RemoteConsolePriv": "true",
                        "iLOConfigPriv": "true",
                        "VirtualMediaPriv": "true",
                        "UserConfigPriv": "true",
                        "VirtualPowerAndResetPriv": "true",
                        "LoginPriv": "true"
                    },
                    "LoginName": "Administrator",
                    "Type": "HpiLOAccount.0.9.7"
                }
            },
            "Password": null,
            "Type": "ManagerAccount.0.9.7",
            "Name": "User Account"
        }
    ],
    "MemberType": "ManagerAccount.0",
    "Total": 1,
    "Type": "Collection.0.9.5",
    "Name": "Accounts"
}
"""

GET_HEADERS = {
    'content-length': '114',
    'etag': 'W/"715B59E6"',
    'allow': 'GET, HEAD, PATCH, POST',
    'cache-control': 'no-cache',
    'date': 'Mon, 23 Mar 2015 08:49:12 GMT',
    'server': 'HP-iLO-Server/1.30',
    'content-type': 'application/json',
    'x_hp-chrp-service-version': '1.0.3'
}

REST_GET_SECURE_BOOT = {
    "Name": "SecureBoot",
    "ResetAllKeys": True,
    "ResetToDefaultKeys": True,
    "SecureBootCurrentState": False,
    "SecureBootEnable": True,
    "Type": "HpSecureBoot.0.9.5",
    "links":
        {
            "self":
                {
                    "href": "/rest/v1/Systems/1/SecureBoot"
                }
        }
    }

REST_FAILURE_OUTPUT = {
    'Type': 'ExtendedError.1.0.0',
    'Messages': [{'MessageID': 'Base.0.0.FakeFailureMessage'}],
    'Name': 'Extended Error Information'
}

REST_POST_RESPONSE = {
    'Type': 'ExtendedError.0.9.6',
    'Messages': [{'MessageID': 'Base.0.0.Success'}],
    'Name': 'Extended Error Information'
}

GET_MANAGER_DETAILS = """
    {
       "AvailableActions":
       [
           {
               "Action": "Reset"
           }
       ],
       "CommandShell":
       {
           "ConnectTypesSupported":
           [
               "SSH",
               "Oem"
           ],
           "Enabled": true,
           "MaxConcurrentSessions": 9
       },
       "Description": "Manager View",
       "Firmware":
       {
           "Current":
           {
               "VersionString": "iLO 4 v2.20"
           }
       },
       "GraphicalConsole":
       {
           "ConnectTypesSupported":
           [
               "KVMIP"
           ],
           "Enabled": true,
           "MaxConcurrentSessions": 10
       },
       "ManagerType": "BMC",
       "Model": "iLO 4",
       "Name": "Manager",
       "Oem":
       {
           "Hp":
           {
               "AvailableActions":
               [
                   {
                       "Action": "ResetRestApiState",
                       "Capabilities":
                       [
                           {
                               "AllowableValues":
                               [
                                   "/Oem/Hp"
                               ],
                               "PropertyName": "Target"
                           }
                       ]
                   }
               ],
               "FederationConfig":
               {
                   "IPv6MulticastScope": "Site",
                   "MulticastAnnouncementInterval": 600,
                   "MulticastDiscovery": "Enabled",
                   "MulticastTimeToLive": 5,
                   "iLOFederationManagement": "Enabled"
               },
               "Firmware":
               {
                   "Current":
                   {
                       "Date": "Feb 09 2015",
                       "DebugBuild": false,
                       "MajorVersion": 2,
                       "MinorVersion": 20,
                       "Time": "",
                       "VersionString": "iLO 4 v2.20"
                   }
               },
               "License":
               {
                   "LicenseKey": "32Q6W-PQWTB-H7XYL-39968-RR53R",
                   "LicenseString": "iLO 4 Advanced",
                   "LicenseType": "Perpetual"
               },
               "RequiredLoginForiLORBSU": false,
               "SerialCLISpeed": 9600,
               "SerialCLIStatus": "EnabledAuthReq",
               "Type": "HpiLO.0.13.0",
               "VSPLogDownloadEnabled": false,
               "iLOSelfTestResults":
               [
                   {
                       "Notes": "",
                       "SelfTestName": "NVRAMData",
                       "Status": "OK"
                   },
                   {
                       "Notes": "Controller firmware revision 2.09.00 ",
                       "SelfTestName": "EmbeddedFlash/SDCard",
                       "Status": "OK"
                   },
                   {
                       "Notes": "",
                       "SelfTestName": "EEPROM",
                       "Status": "OK"
                   },
                   {
                       "Notes": "",
                       "SelfTestName": "HostRom",
                       "Status": "OK"
                   },
                   {
                       "Notes": "",
                       "SelfTestName": "SupportedHost",
                       "Status": "OK"
                   },
                   {
                       "Notes": "ProLiant BL460c Gen9 System Programmable \
                                 Logic Device version 0x13",
                       "SelfTestName": "CPLDPAL0",
                       "Status": "Informational"
                   },
                   {
                       "Notes": "ProLiant BL460c Gen9 SAS Programmable \
                                 Logic Device version 0x01",
                       "SelfTestName": "CPLDPAL1",
                       "Status": "Informational"
                   }
               ],
               "links":
               {
                   "ActiveHealthSystem":
                   {
                       "href": "/rest/v1/Managers/1/ActiveHealthSystem"
                   },
                   "DateTimeService":
                   {
                       "href": "/rest/v1/Managers/1/DateTime"
                   },
                   "EmbeddedMediaService":
                   {
                       "href": "/rest/v1/Managers/1/EmbeddedMedia"
                   },
                   "FederationDispatch":
                   {
                       "extref": "/dispatch"
                   },
                   "FederationGroups":
                   {
                       "href": "/rest/v1/Managers/1/FederationGroups"
                   },
                   "FederationPeers":
                   {
                       "href": "/rest/v1/Managers/1/FederationPeers"
                   },
                   "LicenseService":
                   {
                       "href": "/rest/v1/Managers/1/LicenseService"
                   },
                   "UpdateService":
                   {
                       "href": "/rest/v1/Managers/1/UpdateService"
                   },
                   "VSPLogLocation":
                   {
                       "extref": "/sol.log.gz"
                   }
               }
           }
       },
       "SerialConsole":
       {
           "ConnectTypesSupported":
           [
               "SSH",
               "IPMI",
               "Oem"
           ],
           "Enabled": true,
           "MaxConcurrentSessions": 13
       },
       "Status":
       {
           "State": "Enabled"
       },
       "Type": "Manager.0.10.0",
       "UUID": "83590768-e977-575a-927a-b3de8f692d4f",
       "links":
       {
           "EthernetNICs":
           {
               "href": "/rest/v1/Managers/1/NICs"
           },
           "Logs":
           {
               "href": "/rest/v1/Managers/1/Logs"
           },
           "ManagerForServers":
           [
               {
                   "href": "/rest/v1/Systems/1"
               }
           ],
           "NetworkService":
           {
               "href": "/rest/v1/Managers/1/NetworkService"
           },
           "VirtualMedia":
           {
               "href": "/rest/v1/Managers/1/VirtualMedia"
           },
           "self":
           {
               "href": "/rest/v1/Managers/1"
           }
       }
    }
"""

GET_BIOS_SETTINGS = """
    {
       "AcpiRootBridgePxm": "Enabled",
       "AcpiSlit": "Enabled",
       "AdjSecPrefetch": "Enabled",
       "AdminEmail": "",
       "AdminName": "",
       "AdminOtherInfo": "",
       "AdminPassword": null,
       "AdminPhone": "",
       "AdvancedMemProtection": "AdvancedEcc",
       "AsrStatus": "Enabled",
       "AsrTimeoutMinutes": "10",
       "AssetTagProtection": "Unlocked",
       "AttributeRegistry": "HpBiosAttributeRegistryI36.1.0.40",
       "BootMode": "Uefi",
       "BootOrderPolicy": "RetryIndefinitely",
       "ChannelInterleaving": "Enabled",
       "CollabPowerControl": "Enabled",
       "ConsistentDevNaming": "LomsOnly",
       "CustomPostMessage": "",
       "DcuIpPrefetcher": "Enabled",
       "DcuStreamPrefetcher": "Enabled",
       "Description": "This is the Platform/BIOS Configuration (RBSU)\
                       Current Settings",
       "Dhcpv4": "Enabled",
       "DynamicPowerCapping": "Auto",
       "DynamicPowerResponse": "Fast",
       "EmbSasEnable": "Enabled",
       "EmbSata1Enable": "Enabled",
       "EmbSata2Enable": "Enabled",
       "EmbVideoConnection": "Auto",
       "EmbeddedDiagnostics": "Enabled",
       "EmbeddedDiagsMode": "Auto",
       "EmbeddedSata": "Ahci",
       "EmbeddedSerialPort": "Com2Irq3",
       "EmbeddedUefiShell": "Enabled",
       "EmbeddedUserPartition": "Disabled",
       "EmsConsole": "Com1Irq4",
       "EnergyPerfBias": "BalancedPerf",
       "EraseUserDefaults": "No",
       "ExtendedAmbientTemp": "Disabled",
       "ExtendedMemTest": "Disabled",
       "F11BootMenu": "Enabled",
       "FCScanPolicy": "AllTargets",
       "FanFailPolicy": "Shutdown",
       "FanInstallReq": "EnableMessaging",
       "FlexLom1Enable": "Enabled",
       "HwPrefetcher": "Enabled",
       "IntelDmiLinkFreq": "Auto",
       "IntelNicDmaChannels": "Enabled",
       "IntelPerfMonitoring": "Disabled",
       "IntelProcVtd": "Enabled",
       "IntelQpiFreq": "Auto",
       "IntelQpiLinkEn": "Auto",
       "IntelQpiPowerManagement": "Enabled",
       "IntelTxt": "Disabled",
       "IntelligentProvisioning": "Enabled",
       "InternalSDCardSlot": "Enabled",
       "IoNonPostedPrefetching": "Enabled",
       "Ipv4Address": "0.0.0.0",
       "Ipv4Gateway": "0.0.0.0",
       "Ipv4PrimaryDNS": "0.0.0.0",
       "Ipv4SecondaryDNS": "0.0.0.0",
       "Ipv4SubnetMask": "0.0.0.0",
       "MaxMemBusFreqMHz": "Auto",
       "MaxPcieSpeed": "MaxSupported",
       "MemFastTraining": "Enabled",
       "MinProcIdlePkgState": "C6Retention",
       "MinProcIdlePower": "C6",
       "MixedPowerSupplyReporting": "Enabled",
       "Modified": "2015-03-13T21:50:42+00:00",
       "Name": "BIOS Current Settings",
       "NetworkBootRetry": "Enabled",
       "NicBoot1": "NetworkBoot",
       "NicBoot2": "Disabled",
       "NicBoot3": "Disabled",
       "NicBoot4": "Disabled",
       "NicBoot5": "Disabled",
       "NicBoot6": "Disabled",
       "NicBoot7": "Disabled",
       "NicBoot8": "Disabled",
       "NmiDebugButton": "Enabled",
       "NodeInterleaving": "Disabled",
       "NumaGroupSizeOpt": "Clustered",
       "OldAdminPassword": null,
       "OldPowerOnPassword": null,
       "PciBusPadding": "Enabled",
       "PostF1Prompt": "Delayed20Sec",
       "PowerButton": "Enabled",
       "PowerOnDelay": "None",
       "PowerOnLogo": "Enabled",
       "PowerOnPassword": null,
       "PowerProfile": "BalancedPowerPerf",
       "PowerRegulator": "DynamicPowerSavings",
       "PreBootNetwork": "Auto",
       "ProcAes": "Enabled",
       "ProcCoreDisable": 0,
       "ProcNoExecute": "Enabled",
       "ProcVirtualization": "Enabled",
       "ProcX2Apic": "Enabled",
       "ProductId": "727021-B21",
       "QpiBandwidthOpt": "Balanced",
       "QpiSnoopConfig": "Standard",
       "RemovableFlashBootSeq": "ExternalKeysFirst",
       "RestoreDefaults": "No",
       "RestoreManufacturingDefaults": "No",
       "RomSelection": "CurrentRom",
       "SataSecureErase": "Disabled",
       "SaveUserDefaults": "No",
       "SecureBootStatus": "Disabled",
       "SerialConsoleBaudRate": "115200",
       "SerialConsoleEmulation": "Vt100Plus",
       "SerialConsolePort": "Auto",
       "SerialNumber": "SGH449WNL3",
       "ServerAssetTag": "",
       "ServerName": "",
       "ServerOtherInfo": "",
       "ServerPrimaryOs": "",
       "ServiceEmail": "",
       "ServiceName": "",
       "ServiceOtherInfo": "",
       "ServicePhone": "",
       "SettingsResult":
       {
           "ETag": "5E0136E3",
           "Messages":
           [
               {
                   "MessageArgs":
                   [
                       "Disable",
                       "TpmOperation"
                   ],
                   "MessageID": "Base.1.0:PropertyValueTypeError"
               },
               {
                   "MessageArgs":
                   [
                   ],
                   "MessageID": "Base.1.0:Success"
               }
           ],
           "Time": "2015-03-09T17:50:09+00:00"
       },
       "Sriov": "Enabled",
       "ThermalConfig": "OptimalCooling",
       "ThermalShutdown": "Enabled",
       "TimeZone": "Unspecified",
       "Tpm2Operation": "NoAction",
       "Tpm2Visibility": "Visible",
       "TpmBinding": "Disabled",
       "TpmState": "NotPresent",
       "TpmType": "NoTpm",
       "TpmUefiOpromMeasuring": "Enabled",
       "TpmVisibility": "Visible",
       "Type": "HpBios.1.1.0",
       "UefiPxeBoot": "Auto",
       "UefiShellBootOrder": "Disabled",
       "UefiShellStartup": "Disabled",
       "UefiShellStartupLocation": "Auto",
       "UefiShellStartupUrl": "",
       "UrlBootFile": "",
       "Usb3Mode": "Auto",
       "UsbBoot": "Enabled",
       "UsbControl": "UsbEnabled",
       "UtilityLang": "English",
       "VideoOptions": "BothVideoEnabled",
       "VirtualInstallDisk": "Disabled",
       "VirtualSerialPort": "Com1Irq4",
       "WakeOnLan": "Disabled",
       "links":
       {
           "BaseConfigs":
           {
               "href": "/rest/v1/systems/1/bios/BaseConfigs"
           },
           "Boot":
           {
               "href": "/rest/v1/systems/1/bios/Boot"
           },
           "Mappings":
           {
               "href": "/rest/v1/systems/1/bios/Mappings"
           },
           "Settings":
           {
               "href": "/rest/v1/systems/1/bios/Settings"
           },
           "iScsi":
           {
               "href": "/rest/v1/systems/1/bios/iScsi"
           },
           "self":
           {
               "href": "/rest/v1/systems/1/bios"
           }
       }
    }
"""
