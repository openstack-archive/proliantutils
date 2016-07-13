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

REST_GET_SMART_STORAGE = """
{
    "Model": "ProLiant BL460c Gen9",
    "Name": "Computer System",
    "Oem": {
        "Hp": {
            "links":
                {
                    "SmartStorage":
                        {
                            "href": "/rest/v1/Systems/1/SmartStorage"
                        }
                }
           }
    }
}
"""

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
                       "MinorVersion": 4,
                       "Time": "",
                       "VersionString": "iLO 4 v2.04"
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

GET_MANAGER_DETAILS_EQ_SUGGESTED = """
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
                       "MinorVersion": 4,
                       "Time": "",
                       "VersionString": "iLO 4 v2.30"
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

GET_MANAGER_DETAILS_GT_SUGGESTED = """
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
               "VersionString": "iLO 4 v2.54"
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
                       "MinorVersion": 54,
                       "Time": "",
                       "VersionString": "iLO 4 v2.54"
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

GET_MANAGER_DETAILS_NO_FIRMWARE = """
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
                       "MinorVersion": 20,
                       "Time": "",
                       "VersionString": "iLO 4 v"
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
       "NvDimmNMemFunctionality": "Enabled",
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

GET_BIOS_BOOT = """

{
    "AttributeRegistry": "HpBiosAttributeRegistryP89.1.1.00",
    "BootSources": [
        {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:0)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x0)"
        },
        {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:1)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.2",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x1)"
        },
        {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                         331i Adapter - NIC (PXE IPv4) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv4",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
                                        (C4346BB7EF30,0x0)/IPv4(0.0.0.0)"
        },
        {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 2-port\
                                         361i Adapter - NIC (iSCSI IPv4) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x3)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.iSCSI",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x3)/Pci(0x0,0x0)/MAC\
            (C4346BB7EF30,0x1)/IPv4(0.0.0.0)/iSCSI(iqn.2016-07.org.de\
            :storage,0x1,0x0,None,None,None,TCP)"
        },
        {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                          331i Adapter - NIC (PXE IPv6) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv6",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
            (C4346BB7EF30,0x0)/IPv6(0000:0000:0000:0000:0000:0000:0000:0000)"
        },
        {
            "BootString": "Generic USB Boot",
            "CorrelatableID": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)",
            "StructuredBootString": "Generic.USB.1.1",
            "UEFIDevicePath": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)"
        },
        {
            "BootString": "iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)",
            "StructuredBootString": "CD.Virtual.2.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)"
        }
    ],
    "DefaultBootOrder": [
        "Floppy",
        "Cd",
        "Usb",
        "EmbeddedStorage",
        "PcieSlotStorage",
        "EmbeddedFlexLOM",
        "PcieSlotNic",
        "UefiShell"
    ],
    "Description": "This is the Server Boot Order Current Settings",
    "DesiredBootDevices": [
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        },
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        }
    ],
    "Modified": "2015-05-26T23:38:24+00:00",
    "Name": "Boot Order Current Settings",
    "PersistentBootConfigOrder": [
        "HD.Slot.1.1",
        "HD.Slot.1.2",
        "NIC.LOM.1.1.iSCSI",
        "NIC.LOM.1.1.IPv4",
        "NIC.LOM.1.1.IPv6",
        "Generic.USB.1.1",
        "CD.Virtual.2.1"
    ],
    "SettingsResult": {
        "ETag": "0DEA61A1609C51EED0628E3B0BC633DD",
        "Messages": [
            {
                "MessageArgs": [
                    "PersistentBootConfigOrder[0"
                ],
                "MessageID": "Base.1.0:PropertyValueNotInList"
            },
            {
                "MessageArgs": [],
                "MessageID": "Base.1.0:Success"
            }
        ],
        "Time": "2015-05-14T02:38:40+00:00"
    },
    "Type": "HpServerBootSettings.1.2.0",
    "links": {
        "BaseConfigs": {
            "href": "/rest/v1/systems/1/bios/Boot/BaseConfigs"
        },
        "Settings": {
            "href": "/rest/v1/systems/1/bios/Boot/Settings"
        },
        "self": {
            "href": "/rest/v1/systems/1/bios/Boot"
        }
    }
}

"""

GET_BIOS_MAPPINGS = """
{
    "Registry": "HpBiosAttributeRegistryP89.1.1.00",
    "BiosPciSettingsMappings": [
        {
            "Associations": [
                "EmbSata1Enable"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1F,0x2)",
            "Instance": 1,
            "Subinstances": []
        },
        {
            "Associations": [
                "EmbSata2Enable"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x11,0x4)",
            "Instance": 2,
            "Subinstances": []
        },
        {
            "Associations": [
                "EmbNicEnable",
                {
                    "PreBootNetwork": "EmbNic"
                }
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "Instance": 3,
            "Subinstances": [
                {
                 "Associations": [
                 "NicBoot1"
                 ],
                 "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
                 "Subinstance": 1
                },
                {
                 "Associations": [
                 "NicBoot2"
                 ],
                 "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x1)",
                 "Subinstance": 2
                },
                {
                 "Associations": [
                 "NicBoot3"
                 ],
                 "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x2)",
                 "Subinstance": 3
                },
                {
                 "Associations": [
                 "NicBoot4"
                 ],
                 "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x3)",
                 "Subinstance": 4
                }
            ]
        },
        {
           "Associations": [
                "EmbSasEnable"
           ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)",
            "Instance": 4,
           "Subinstances": []
        },
        {
            "Associations": [
                "FlexLom1Enable",
                {
                    "PreBootNetwork": "FlexLom1"
                }
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x2)/Pci(0x0,0x0)",
            "Instance": 5,
            "Subinstances": []
        },
        {
            "Associations": [
                "PciSlot1Enable"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "Instance": 6,
            "Subinstances": []
        },
        {
            "Associations": [
                "PciSlot3Enable"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x3,0x0)/Pci(0x0,0x0)",
            "Instance": 7,
            "Subinstances": []
        },
        {
            "Associations": [
                "PciSlot2Enable"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x3,0x2)/Pci(0x0,0x0)",
            "Instance": 8,
            "Subinstances": []
        },
        {
            "Associations": [
                "Slot1StorageBoot"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
                                                       Scsi(0x0,0x0)",
            "Instance": 9,
            "Subinstances": []
        },
        {
            "Associations": [
                "Slot1StorageBoot"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
                                                       Scsi(0x0,0x1)",
            "Instance": 10,
            "Subinstances": []
        },
        {
            "Associations": [
                "Slot1StorageBoot"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
                     Scsi(0x0,0x0)/HD(1,MBR,0x000677A4,0x800,0x2800)",
            "Instance": 11,
            "Subinstances": []
        },
        {
            "Associations": [
                "Slot1StorageBoot"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
                     Scsi(0x0,0x0)/HD(2,MBR,0x000677A4,0x3000,0x800)",
            "Instance": 12,
            "Subinstances": []
        },
        {
            "Associations": [
                "Slot1StorageBoot"
            ],
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
                 Scsi(0x0,0x0)/HD(3,MBR,0x000677A4,0x3800,0x6400000)",
            "Instance": 13,
            "Subinstances": []
        }
    ],
    "Modified": "2015-05-22T06:48:46+00:00",
    "Name": "Bios Setting Mapping to Devices",
    "Type": "HpBiosMapping.1.2.0",
    "links": {
        "self": {
            "href": "/rest/v1/systems/1/bios/Mappings"
        }
    }
}
"""
GET_BASE_CONFIG = """


    {
       "BaseConfigs":
       [
           {
               "default":
               {
                   "AcpiRootBridgePxm": "Enabled",
                   "AcpiSlit": "Enabled",
                   "AdjSecPrefetch": "Enabled",
                   "AdminEmail": "",
                   "AdminName": "",
                   "AdminOtherInfo": "",
                   "AdminPassword": "",
                   "AdminPhone": "",
                   "AdvancedMemProtection": "AdvancedEcc",
                   "AsrStatus": "Enabled",
                   "AsrTimeoutMinutes": "10",
                   "AssetTagProtection": "Unlocked",
                   "AutoPowerOn": "RestoreLastState",
                   "BootMode": "Uefi",
                   "BootOrderPolicy": "RetryIndefinitely",
                   "ChannelInterleaving": "Enabled",
                   "CollabPowerControl": "Enabled",
                   "ConsistentDevNaming": "LomsOnly",
                   "CustomPostMessage": "",
                   "DcuIpPrefetcher": "Enabled",
                   "DcuStreamPrefetcher": "Enabled",
                   "Description": "BIOS System Defaults",
                   "Dhcpv4": "Enabled",
                   "DynamicPowerCapping": "Auto",
                   "DynamicPowerResponse": "Fast",
                   "EmbNicEnable": "Enabled",
                   "EmbSas1Boot": "AllTargets",
                   "EmbSata1Enable": "Enabled",
                   "EmbSata2Enable": "Enabled",
                   "EmbVideoConnection": "Auto",
                   "EmbeddedDiagnostics": "Enabled",
                   "EmbeddedDiagsMode": "Auto",
                   "EmbeddedSata": "Ahci",
                   "EmbeddedSerialPort": "Com1Irq4",
                   "EmbeddedUefiShell": "Enabled",
                   "EmbeddedUserPartition": "Disabled",
                   "EmsConsole": "Disabled",
                   "EnergyPerfBias": "BalancedPerf",
                   "EraseUserDefaults": "No",
                   "ExtendedAmbientTemp": "Disabled",
                   "ExtendedMemTest": "Disabled",
                   "F11BootMenu": "Enabled",
                   "FCScanPolicy": "AllTargets",
                   "FanFailPolicy": "Shutdown",
                   "FanInstallReq": "EnableMessaging",
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
                   "NetworkBootRetry": "Enabled",
                   "NicBoot1": "NetworkBoot",
                   "NicBoot2": "Disabled",
                   "NicBoot3": "Disabled",
                   "NicBoot4": "Disabled",
                   "NmiDebugButton": "Enabled",
                   "NodeInterleaving": "Disabled",
                   "NumaGroupSizeOpt": "Clustered",
                   "OldAdminPassword": "",
                   "OldPowerOnPassword": "",
                   "PciBusPadding": "Enabled",
                   "PciSlot1Enable": "Enabled",
                   "PostF1Prompt": "Delayed20Sec",
                   "PowerButton": "Enabled",
                   "PowerOnDelay": "None",
                   "PowerOnLogo": "Enabled",
                   "PowerOnPassword": "",
                   "PowerProfile": "BalancedPowerPerf",
                   "PowerRegulator": "DynamicPowerSavings",
                   "PreBootNetwork": "Auto",
                   "ProcAes": "Enabled",
                   "ProcCoreDisable": 0,
                   "ProcNoExecute": "Enabled",
                   "ProcVirtualization": "Enabled",
                   "ProcX2Apic": "Enabled",
                   "QpiBandwidthOpt": "Balanced",
                   "QpiSnoopConfig": "Standard",
                   "RedundantPowerSupply": "BalancedMode",
                   "RemovableFlashBootSeq": "ExternalKeysFirst",
                   "RestoreDefaults": "No",
                   "RestoreManufacturingDefaults": "No",
                   "SataSecureErase": "Disabled",
                   "SaveUserDefaults": "No",
                   "SecureBoot": "Disabled",
                   "SecureBootStatus": "Disabled",
                   "SerialConsoleBaudRate": "115200",
                   "SerialConsoleEmulation": "Vt100Plus",
                   "SerialConsolePort": "Auto",
                   "ServerAssetTag": "",
                   "ServerName": "",
                   "ServerOtherInfo": "",
                   "ServerPrimaryOs": "",
                   "ServiceEmail": "",
                   "ServiceName": "",
                   "ServiceOtherInfo": "",
                   "ServicePhone": "",
                   "Slot1StorageBoot": "AllTargets",
                   "Slot2StorageBoot": "AllTargets",
                   "Slot3StorageBoot": "AllTargets",
                   "Slot4StorageBoot": "AllTargets",
                   "Slot5StorageBoot": "AllTargets",
                   "Slot6StorageBoot": "AllTargets",
                   "Sriov": "Enabled",
                   "TcmOperation": "Disable",
                   "TcmVisibility": "Visible",
                   "ThermalConfig": "OptimalCooling",
                   "ThermalShutdown": "Enabled",
                   "TimeZone": "UtcM7",
                   "Tpm2Operation": "NoAction",
                   "Tpm2Ppi": "Disabled",
                   "Tpm2Visibility": "Visible",
                   "TpmBinding": "Disabled",
                   "TpmOperation": "Disable",
                   "TpmState": "NotPresent",
                   "TpmType": "NoTpm",
                   "TpmUefiOpromMeasuring": "Enabled",
                   "TpmVisibility": "Visible",
                   "UefiOptimizedBoot": "Enabled",
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
                   "VirtualSerialPort": "Com2Irq3",
                   "VlanControl": "Disabled",
                   "VlanId": 0,
                   "VlanPriority": 0,
                   "WakeOnLan": "Enabled"
               }
           }
       ],
       "Capabilities":
       {
           "BaseConfig": true,
           "BaseConfigs": false
       },
       "Modified": "2015-03-26T00:05:15+00:00",
       "Name": "BIOS Default Settings",
       "Type": "HpBaseConfigs.0.10.0",
       "links":
       {
           "self":
           {
               "href": "/rest/v1/systems/1/bios/BaseConfigs"
           }
       }
    }
"""
GET_ISCSI_PATCH = """
{
    "iSCSIBootSources": [
        {
            "iSCSIBootAttemptInstance": 1,
            "iSCSIBootAttemptName": "NicBoot1",
            "iSCSIBootLUN": "1",
            "iSCSINicSource": "NicBoot1",
            "iSCSITargetIpAddress": "10.10.1.30",
            "iSCSITargetName": "iqn.2011-07.com.example.server:test1",
            "iSCSITargetTcpPort": 3260
         }
     ]
}
"""

GET_ISCSI_SETTINGS = """
{
    "AttributRegistry": "HpBiosAttributeRegistryP89.1.1.00",
    "Description": "This is the Server iSCSI Software Initiator Current \
                             Settings",
    "Modified": "2015-05-28T04:11:55+00:00",
    "Name": "iSCSI Software Initiator Current Settings",
    "SettingsResult": {
        "ETag": "D43535CE",
        "Messages": [
            {
                "MessageArgs": [
                    "iSCSITargetTcpport"
                ],
                "MessageID": "Base.1.0:PropertyUnknown"
            },
            {
                "MessageArgs": [],
                "MessageID": "Base.1.0:Success"
            }
        ],
        "Time": "2015-05-28T04:11:55+00:00"
    },
    "Type": "HpiSCSISoftwareInitiator.1.0.0",
    "iSCSIBootSources": [
        {
            "StructuredBootString": "NIC.LOM.1.1.iSCSI",
            "UEFIDevicePath": null,
            "iSCSIAuthenticationMethod": "None",
            "iSCSIBootAttemptInstance": 1,
            "iSCSIBootAttemptName": "NicBoot1",
            "iSCSIBootEnable": "Enabled",
            "iSCSIBootLUN": "1",
            "iSCSIChapSecret": null,
            "iSCSIChapType": "OneWay",
            "iSCSIChapUsername": null,
            "iSCSIConnectRetry": 0,
            "iSCSIConnectTimeoutMS": 1000,
            "iSCSIInitiatorGateway": "0.0.0.0",
            "iSCSIInitiatorInfoViaDHCP": true,
            "iSCSIInitiatorIpAddress": "0.0.0.0",
            "iSCSIInitiatorNetmask": "0.0.0.0",
            "iSCSIIpAddressType": "IPv4",
            "iSCSINicSource": "NicBoot1",
            "iSCSIReverseChapSecret": null,
            "iSCSIReverseChapUsername": null,
            "iSCSITargetInfoViaDHCP": false,
            "iSCSITargetIpAddress": "10.10.1.38",
            "iSCSITargetName": "iqn.2014-07.com.tecmint:tgt1",
            "iSCSITargetTcpPort": 3260
        },
        {
            "StructuredBootString": "NIC.LOM.1.1.iSCSI",
            "UEFIDevicePath": null,
            "iSCSIAuthenticationMethod": "None",
            "iSCSIBootAttemptInstance": 0,
            "iSCSIBootAttemptName": "test2",
            "iSCSIBootEnable": "Enabled",
            "iSCSIBootLUN": "1",
            "iSCSIChapSecret": null,
            "iSCSIChapType": "OneWay",
            "iSCSIChapUsername": null,
            "iSCSIConnectRetry": 0,
            "iSCSIConnectTimeoutMS": 1000,
            "iSCSIInitiatorGateway": "0.0.0.0",
            "iSCSIInitiatorInfoViaDHCP": true,
            "iSCSIInitiatorIpAddress": "0.0.0.0",
            "iSCSIInitiatorNetmask": "0.0.0.0",
            "iSCSIIpAddressType": "IPv4",
            "iSCSINicSource": "NicBoot1",
            "iSCSIReverseChapSecret": null,
            "iSCSIReverseChapUsername": null,
            "iSCSITargetInfoViaDHCP": false,
            "iSCSITargetIpAddress": "10.10.1.38",
            "iSCSITargetName": "iqn.2014-07.com.tecmint:tgt1",
            "iSCSITargetTcpPort": 3260
        },
        {
            "StructuredBootString": null,
            "UEFIDevicePath": null,
            "iSCSIAuthenticationMethod": "None",
            "iSCSIBootAttemptInstance": 0,
            "iSCSIBootAttemptName": "",
            "iSCSIBootEnable": "Disabled",
            "iSCSIBootLUN": "0",
            "iSCSIChapSecret": null,
            "iSCSIChapType": "OneWay",
            "iSCSIChapUsername": null,
            "iSCSIConnectRetry": 0,
            "iSCSIConnectTimeoutMS": 100,
            "iSCSIInitiatorGateway": "0.0.0.0",
            "iSCSIInitiatorInfoViaDHCP": true,
            "iSCSIInitiatorIpAddress": "0.0.0.0",
            "iSCSIInitiatorNetmask": "0.0.0.0",
            "iSCSIIpAddressType": "IPv4",
            "iSCSINicSource": null,
            "iSCSIReverseChapSecret": null,
            "iSCSIReverseChapUsername": null,
            "iSCSITargetInfoViaDHCP": true,
            "iSCSITargetIpAddress": "0.0.0.0",
            "iSCSITargetName": null,
            "iSCSITargetTcpPort": 0
        },
        {
            "StructuredBootString": null,
            "UEFIDevicePath": null,
            "iSCSIAuthenticationMethod": "None",
            "iSCSIBootAttemptInstance": 0,
            "iSCSIBootAttemptName": "",
            "iSCSIBootEnable": "Disabled",
            "iSCSIBootLUN": "0",
            "iSCSIChapSecret": null,
            "iSCSIChapType": "OneWay",
            "iSCSIChapUsername": null,
            "iSCSIConnectRetry": 0,
            "iSCSIConnectTimeoutMS": 100,
            "iSCSIInitiatorGateway": "0.0.0.0",
            "iSCSIInitiatorInfoViaDHCP": true,
            "iSCSIInitiatorIpAddress": "0.0.0.0",
            "iSCSIInitiatorNetmask": "0.0.0.0",
            "iSCSIIpAddressType": "IPv4",
            "iSCSINicSource": null,
            "iSCSIReverseChapSecret": null,
            "iSCSIReverseChapUsername": null,
            "iSCSITargetInfoViaDHCP": true,
            "iSCSITargetIpAddress": "0.0.0.0",
            "iSCSITargetName": null,
            "iSCSITargetTcpPort": 0
        }
    ],
    "iSCSIInitiatorName": "iqn.1986-03.com.hp:uefi-p89-mxq45006w5",
    "iSCSINicSources": [
        "NicBoot1",
        "NicBoot2",
        "NicBoot3",
        "NicBoot4"
    ],
    "links": {
        "BaseConfigs": {
            "href": "/rest/v1/systems/1/bios/iScsi/BaseConfigs"
        },
        "Mappings": {
            "href": "/rest/v1/systems/1/bios/Mappings"
        },
        "Settings": {
            "href": "/rest/v1/systems/1/bios/iScsi/Settings"
        },
        "self": {
            "href": "/rest/v1/systems/1/bios/iScsi"
        }
    }
}

"""

RESP_VM_STATUS_FLOPPY_EMPTY = """
{
    "Description": "Virtual Removable Media",
    "links": {
        "self": {
            "href": "/rest/v1/Managers/1/VirtualMedia/1"
        }
    },
    "Type": "VirtualMedia.0.9.5",
    "Image": "",
    "ConnectedVia": "NotConnected",
    "MediaTypes": [
        "Floppy",
        "USBStick"
    ],
    "WriteProtected": false,
    "Inserted": false,
    "Name": "VirtualMedia"
}
"""

GET_VM_STATUS_FLOPPY_EMPTY = """
{
    "WRITE_PROTECT": "NO",
    "VM_APPLET": "DISCONNECTED",
    "IMAGE_URL": "",
    "BOOT_OPTION": "NO_BOOT",
    "DEVICE": "FLOPPY",
    "IMAGE_INSERTED": "NO"
}
"""

RESP_VM_STATUS_FLOPPY_INSERTED = """
{
    "ImageName": "floppy.iso",
    "Description": "Virtual Removable Media",
    "links": {
        "self": {
            "href": "/rest/v1/Managers/1/VirtualMedia/1"
        }
    },
    "Type": "VirtualMedia.0.9.5",
    "Image": "http://1.1.1.1/floppy.iso",
    "ConnectedVia": "URI",
    "MediaTypes": [
        "Floppy",
        "USBStick"
    ],
    "WriteProtected": true,
    "Inserted": true,
    "Name": "VirtualMedia"
}
"""

GET_VM_STATUS_FLOPPY_INSERTED = """
{
    "WRITE_PROTECT": "YES",
    "VM_APPLET": "CONNECTED",
    "IMAGE_URL": "http://1.1.1.1/floppy.iso",
    "BOOT_OPTION": "BOOT_ALWAYS",
    "DEVICE": "FLOPPY",
    "IMAGE_INSERTED": "YES"
}
"""

RESP_VM_STATUS_CDROM_INSERTED = """
{
    "Description": "Virtual Removable Media",
    "links": {
        "self": {"href": "/rest/v1/Managers/1/VirtualMedia/2"
        }
    },
    "Type": "VirtualMedia.0.9.5",
    "Image": "http://foo/foo", "ConnectedVia": "NotConnected",
    "MediaTypes": [
        "CD",
        "DVD"
    ],
    "Oem": {
        "Hp": {
        "Type": "HpiLOVirtualMedia.0.9.5",
        "BootOnNextServerReset": false
        }
    },
    "WriteProtected": true,
    "Inserted": true,
    "Name": "VirtualMedia"
}
"""

RESP_VM_STATUS_CDROM_EMPTY = """
{
    "Description": "Virtual Removable Media",
    "links": {
        "self": {"href": "/rest/v1/Managers/1/VirtualMedia/2"
        }
    },
    "Type": "VirtualMedia.0.9.5",
    "Image": "", "ConnectedVia": "NotConnected",
    "MediaTypes": [
        "CD",
        "DVD"
    ],
    "Oem": {
        "Hp": {
        "Type": "HpiLOVirtualMedia.0.9.5",
        "BootOnNextServerReset": false
        }
    },
    "WriteProtected": true,
    "Inserted": false,
    "Name": "VirtualMedia"
}
"""

GET_VM_STATUS_CDROM_EMPTY = """
{
    "WRITE_PROTECT": "YES",
    "VM_APPLET": "DISCONNECTED",
    "IMAGE_URL": "",
    "BOOT_OPTION": "NO_BOOT",
    "DEVICE": "CDROM",
    "IMAGE_INSERTED": "NO"}
"""

RESP_VM_STATUS_CDROM_INSERTED = """
{
    "ImageName": "cdrom.iso",
    "Description": "Virtual Removable Media",
    "links": {"self": {"href": "/rest/v1/Managers/1/VirtualMedia/2"}},
    "Type": "VirtualMedia.0.9.5",
    "Image": "http://1.1.1.1/cdrom.iso",
    "ConnectedVia": "URI",
    "MediaTypes": [
        "CD",
        "DVD"
    ],
    "Oem": {
        "Hp": {
            "Type": "HpiLOVirtualMedia.0.9.5",
            "BootOnNextServerReset": false
        }
    },
    "WriteProtected": true,
    "Inserted": true,
    "Name": "VirtualMedia"
}
"""

GET_VM_STATUS_CDROM_INSERTED = """
{
    "WRITE_PROTECT": "YES",
    "VM_APPLET": "CONNECTED",
    "IMAGE_URL": "http://1.1.1.1/cdrom.iso",
    "BOOT_OPTION": "BOOT_ALWAYS",
    "DEVICE": "CDROM",
    "IMAGE_INSERTED": "YES"
}
"""

PATCH_VM_CDROM = """
{
    "Oem": {
        "Hp": {
            "BootOnNextServerReset": true
        }
    }
}
"""

GET_MANAGER_DETAILS_NO_VMEDIA = """
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
           "self":
           {
               "href": "/rest/v1/Managers/1"
           }
       }
    }
"""

RESP_VM_STATUS_CDROM_MISSING = """
{
    "Description": "Virtual Removable Media",
    "links": {
        "self": {"href": "/rest/v1/Managers/1/VirtualMedia/2"
        }
    },
    "Type": "VirtualMedia.0.9.5",
    "Image": "", "ConnectedVia": "NotConnected",
    "MediaTypes": [
        "DVD"
    ],
    "Oem": {
        "Hp": {
        "Type": "HpiLOVirtualMedia.0.9.5",
        "BootOnNextServerReset": false
        }
    },
    "WriteProtected": true,
    "Inserted": false,
    "Name": "VirtualMedia"
}
"""

RESP_BODY_FOR_SYSTEM_WITH_CDROM = """
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
        "BootSourceOverrideEnabled": "Once",
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
        "BootSourceOverrideTarget": "Cd",
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

RESP_BODY_WITH_UEFI_SHELL = """
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
        "BootSourceOverrideEnabled": "Once",
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
        "BootSourceOverrideTarget": "UefiShell",
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


RESP_BODY_FOR_SYSTEM_WITHOUT_BOOT = """
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

SYSTEM_WITH_CDROM_CONT = """
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
        "BootSourceOverrideEnabled": "Continuous",
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
        "BootSourceOverrideTarget": "Cd",
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

SYSTEM_WITH_UEFISHELL_CONT = """
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
        "BootSourceOverrideEnabled": "Continuous",
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
        "BootSourceOverrideTarget": "UefiShell",
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

UEFI_BOOT_DEVICE_ORDER_PXE = ['NIC.LOM.1.1.IPv4',
                              'NIC.LOM.1.1.IPv6',
                              'HD.Slot.1.2',
                              'Generic.USB.1.1',
                              'CD.Virtual.2.1',
                              'FD.Virtual.1.1']

UEFI_BOOT_DEVICE_ORDER_HDD = ['HD.Slot.1.2',
                              'NIC.LOM.1.1.IPv4',
                              'NIC.LOM.1.1.IPv6',
                              'Generic.USB.1.1',
                              'CD.Virtual.2.1',
                              'FD.Virtual.1.1']

UEFI_BOOT_DEVICE_ORDER_CD = ['CD.Virtual.2.1',
                             'NIC.LOM.1.1.IPv4',
                             'NIC.LOM.1.1.IPv6',
                             'Generic.USB.1.1',
                             'HD.Slot.1.2',
                             'FD.Virtual.1.1']

UEFI_BOOT_DEVICE_ORDER_ERR = ['FAKE.Virtual.2.1',
                              'CD.Virtual.2.1',
                              'NIC.LOM.1.1.IPv4',
                              'NIC.LOM.1.1.IPv6',
                              'Generic.USB.1.1',
                              'HD.Slot.1.2',
                              'FD.Virtual.1.1']

UEFI_BOOT_SOURCES_ERR = '''
[
    {
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC \
                           (3863BB43683C,0x0)/IPv4(0.0.0.0)",
        "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port \
                       331i Adapter - NIC (PXE IPv4) ",
        "StructuredBootString": "NIC.LOM.1.1.IPv4",
        "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)"
        },
    {
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
                           (3863BB43683C,0x0)/IPv6(0000:0000:0000:0000:\
                           0000:0000:0000:0000)",
        "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port \
                       331i Adapter - NIC (PXE IPv6) ",
        "StructuredBootString": "NIC.LOM.1.1.IPv6",
        "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)"
        },
    {
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                           (0x0,0x0)",
        "StructuredBootString": "HD.Slot.1.2",
        "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)"
        },
    {
        "UEFIDevicePath": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)",
        "BootString": "Generic USB Boot",
        "StructuredBootString": "Generic.USB.1.1",
        "CorrelatableID": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)"
        },
    {
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)\
                           /USB(0x0,0x0)",
        "BootString": "iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM",
        "StructuredBootString": "CD.Virtual.2.1",
        "CorrelatableID": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                           (0x0,0x0)"
        },
    {
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x2)/Pci(0x0,0x4)/USB\
                           (0x1,0x0)",
        "BootString": "iLO Virtual USB 1 : HP iLO Virtual USB Key",
        "StructuredBootString": "FD.Virtual.1.1",
        "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x2)/Pci(0x0,0x4)/USB(0x1,\
                           0x0)"
        }
    ]
'''

UEFI_PERS_BOOT_DEVICES = ["HD.Slot.1.1",
                          "HD.Slot.1.2",
                          "NIC.LOM.1.1.iSCSI",
                          "NIC.LOM.1.1.IPv4",
                          "NIC.LOM.1.1.IPv6",
                          "Generic.USB.1.1",
                          "CD.Virtual.2.1"
                          ]

BOOT_PERS_DEV_ORDER_MISSING = """

{
    "AttributeRegistry": "HpBiosAttributeRegistryP89.1.1.00",
    "BootSources": [
        {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:0)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x0)"
        },
        {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:1)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.2",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x1)"
        },
        {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                         331i Adapter - NIC (PXE IPv4) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv4",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
                                        (C4346BB7EF30,0x0)/IPv4(0.0.0.0)"
        },
        {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                          331i Adapter - NIC (PXE IPv6) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv6",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
            (C4346BB7EF30,0x0)/IPv6(0000:0000:0000:0000:0000:0000:0000:0000)"
        },
        {
            "BootString": "Generic USB Boot",
            "CorrelatableID": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)",
            "StructuredBootString": "Generic.USB.1.1",
            "UEFIDevicePath": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)"
        },
        {
            "BootString": "iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)",
            "StructuredBootString": "CD.Virtual.2.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)"
        }
    ],
    "DefaultBootOrder": [
        "Floppy",
        "Cd",
        "Usb",
        "EmbeddedStorage",
        "PcieSlotStorage",
        "EmbeddedFlexLOM",
        "PcieSlotNic",
        "UefiShell"
    ],
    "Description": "This is the Server Boot Order Current Settings",
    "DesiredBootDevices": [
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        },
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        }
    ],
    "Modified": "2015-05-26T23:38:24+00:00",
    "Name": "Boot Order Current Settings",
    "SettingsResult": {
        "ETag": "0DEA61A1609C51EED0628E3B0BC633DD",
        "Messages": [
            {
                "MessageArgs": [
                    "PersistentBootConfigOrder[0"
                ],
                "MessageID": "Base.1.0:PropertyValueNotInList"
            },
            {
                "MessageArgs": [],
                "MessageID": "Base.1.0:Success"
            }
        ],
        "Time": "2015-05-14T02:38:40+00:00"
    },
    "Type": "HpServerBootSettings.1.2.0",
    "links": {
        "BaseConfigs": {
            "href": "/rest/v1/systems/1/bios/Boot/BaseConfigs"
        },
        "Settings": {
            "href": "/rest/v1/systems/1/bios/Boot/Settings"
        },
        "self": {
            "href": "/rest/v1/systems/1/bios/Boot"
        }
    }
}

"""

UEFI_BootSources = '''
[
    {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:0)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x0)"
    },
    {
            "BootString": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                                      RAID 0 Logical Drive(Target:0, Lun:1)",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)",
            "StructuredBootString": "HD.Slot.1.2",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/Scsi\
                                                                (0x0,0x1)"
    },
    {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                         331i Adapter - NIC (PXE IPv4) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv4",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
                                        (C4346BB7EF30,0x0)/IPv4(0.0.0.0)"
    },
    {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 2-port\
                                         361i Adapter - NIC (iSCSI IPv4) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x2,0x3)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.iSCSI",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x3)/Pci(0x0,0x0)/MAC\
            (C4346BB7EF30,0x1)/IPv4(0.0.0.0)/iSCSI(iqn.2016-07.org.de\
            :storage,0x1,0x0,None,None,None,TCP)"
    },

    {
            "BootString": "Embedded LOM 1 Port 1 : HP Ethernet 1Gb 4-port\
                                          331i Adapter - NIC (PXE IPv6) ",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)",
            "StructuredBootString": "NIC.LOM.1.1.IPv6",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1C,0x4)/Pci(0x0,0x0)/MAC\
            (C4346BB7EF30,0x0)/IPv6(0000:0000:0000:0000:0000:0000:0000:0000)"
    },
    {
            "BootString": "Generic USB Boot",
            "CorrelatableID": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)",
            "StructuredBootString": "Generic.USB.1.1",
            "UEFIDevicePath": "UsbClass(0xFFFF,0xFFFF,0xFF,0xFF,0xFF)"
    },
    {
            "BootString": "iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM",
            "CorrelatableID": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)",
            "StructuredBootString": "CD.Virtual.2.1",
            "UEFIDevicePath": "PciRoot(0x0)/Pci(0x1D,0x0)/USB(0x0,0x0)/USB\
                                                                (0x0,0x0)"
    }
]
'''

UEFI_BOOTSOURCES_MISSING = """
{
    "AttributeRegistry": "HpBiosAttributeRegistryP89.1.1.00",
    "DefaultBootOrder": [
        "Floppy",
        "Cd",
        "Usb",
        "EmbeddedStorage",
        "PcieSlotStorage",
        "EmbeddedFlexLOM",
        "PcieSlotNic",
        "UefiShell"
    ],
    "Description": "This is the Server Boot Order Current Settings",
    "DesiredBootDevices": [
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        },
        {
            "CorrelatableID": "",
            "Lun": "",
            "Wwn": "",
            "iScsiTargetName": ""
        }
    ],
    "Modified": "2015-05-26T23:38:24+00:00",
    "Name": "Boot Order Current Settings",
    "PersistentBootConfigOrder": [
        "HD.Slot.1.1",
        "HD.Slot.1.2",
        "NIC.LOM.1.1.IPv4",
        "NIC.LOM.1.1.IPv6",
        "Generic.USB.1.1",
        "CD.Virtual.2.1"
    ],
    "SettingsResult": {
        "ETag": "0DEA61A1609C51EED0628E3B0BC633DD",
        "Messages": [
            {
                "MessageArgs": [
                    "PersistentBootConfigOrder[0"
                ],
                "MessageID": "Base.1.0:PropertyValueNotInList"
            },
            {
                "MessageArgs": [],
                "MessageID": "Base.1.0:Success"
            }
        ],
        "Time": "2015-05-14T02:38:40+00:00"
    },
    "Type": "HpServerBootSettings.1.2.0",
    "links": {
        "BaseConfigs": {
            "href": "/rest/v1/systems/1/bios/Boot/BaseConfigs"
        },
        "Settings": {
            "href": "/rest/v1/systems/1/bios/Boot/Settings"
        },
        "self": {
            "href": "/rest/v1/systems/1/bios/Boot"
        }
    }
}
"""
PCI_DEVICE_DETAILS_NO_GPU = """
{
    "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/PCIDevices",
    "@odata.id": "/redfish/v1/Systems/1/PCIDevices/",
    "@odata.type": "#HpServerPciDeviceCollection.HpServerPciDeviceCollection",
    "Description": " PciDevices view",
    "Items": [
    {
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/\
1/PCIDevices/Members/$entity",
        "@odata.id": "/redfish/v1/Systems/1/PCIDevices/6/",
        "@odata.type": "#HpServerPciDevice.1.0.0.HpServerPciDevice",
        "BusNumber": 132,
        "ClassCode": 6,
        "DeviceID": 34631,
        "DeviceInstance": 2,
        "DeviceLocation": "PCI Slot",
        "DeviceNumber": 0,
        "DeviceSubInstance": 1,
        "DeviceType": "Other PCI Device",
        "FunctionNumber": 0,
        "Id": "6",
        "Name": "PCIe Controller",
        "SegmentNumber": 0,
        "StructuredName": "PCI.Slot.2.1",
        "SubclassCode": 4,
        "SubsystemDeviceID": 34631,
        "SubsystemVendorID": 4277,
        "Type": "HpServerPciDevice.1.0.0",
        "UEFIDevicePath": "PciRoot(0x1)/Pci(0x3,0x0)/Pci(0x0,0x0)",
        "VendorID": 4277,
        "links": {
            "self": {
                "href": "/rest/v1/Systems/1/PCIDevices/6"
            }
        }
    }
    ]
}
"""

PCI_GPU_LIST = """
[
    {
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/PCIDevices/Members/$entity",
        "@odata.id": "/redfish/v1/Systems/1/PCIDevices/6/",
        "@odata.type": "#HpServerPciDevice.1.0.0.HpServerPciDevice",
        "BusNumber": 5,
        "ClassCode": 3,
        "DeviceID": 26528,
        "DeviceInstance": 3,
        "DeviceLocation": "PCI Slot",
        "DeviceNumber": 0,
        "DeviceSubInstance": 1,
        "DeviceType": "Other PCI Device",
        "FunctionNumber": 0,
        "Id": "6",
        "Name": "HAWAII XTGL",
        "SegmentNumber": 0,
        "StructuredName": "PCI.Slot.3.1",
        "SubclassCode": 128,
        "SubsystemDeviceID": 821,
        "SubsystemVendorID": 4098,
        "Type": "HpServerPciDevice.1.0.0",
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
Pci(0x8,0x0)/Pci(0x0,0x0)",
        "VendorID": 4098,
        "links": {
            "self": {
                "href": "/rest/v1/Systems/1/PCIDevices/6"
            }
        }
    }
]
"""

PCI_DEVICE_DETAILS = """
{
    "@odata.context": "/redfish/v1/$metadata#Systems/Members/1/PCIDevices",
    "@odata.id": "/redfish/v1/Systems/1/PCIDevices/",
    "@odata.type": "#HpServerPciDeviceCollection.HpServerPciDeviceCollection",
    "Description": " PciDevices view",
    "Items": [
    {
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/\
1/PCIDevices/Members/$entity",
        "@odata.id": "/redfish/v1/Systems/1/PCIDevices/6/",
        "@odata.type": "#HpServerPciDevice.1.0.0.HpServerPciDevice",
        "BusNumber": 132,
        "ClassCode": 6,
        "DeviceID": 34631,
        "DeviceInstance": 2,
        "DeviceLocation": "PCI Slot",
        "DeviceNumber": 0,
        "DeviceSubInstance": 1,
        "DeviceType": "Other PCI Device",
        "FunctionNumber": 0,
        "Id": "6",
        "Name": "PCIe Controller",
        "SegmentNumber": 0,
        "StructuredName": "PCI.Slot.2.1",
        "SubclassCode": 4,
        "SubsystemDeviceID": 34631,
        "SubsystemVendorID": 4277,
        "Type": "HpServerPciDevice.1.0.0",
        "UEFIDevicePath": "PciRoot(0x1)/Pci(0x3,0x0)/Pci(0x0,0x0)",
        "VendorID": 4277,
        "links": {
            "self": {
                "href": "/rest/v1/Systems/1/PCIDevices/6"
            }
        }
    },
    {
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/PCIDevices/Members/$entity",
        "@odata.id": "/redfish/v1/Systems/1/PCIDevices/6/",
        "@odata.type": "#HpServerPciDevice.1.0.0.HpServerPciDevice",
        "BusNumber": 5,
        "ClassCode": 3,
        "DeviceID": 26528,
        "DeviceInstance": 3,
        "DeviceLocation": "PCI Slot",
        "DeviceNumber": 0,
        "DeviceSubInstance": 1,
        "DeviceType": "Other PCI Device",
        "FunctionNumber": 0,
        "Id": "6",
        "Name": "HAWAII XTGL",
        "SegmentNumber": 0,
        "StructuredName": "PCI.Slot.3.1",
        "SubclassCode": 128,
        "SubsystemDeviceID": 821,
        "SubsystemVendorID": 4098,
        "Type": "HpServerPciDevice.1.0.0",
        "UEFIDevicePath": "PciRoot(0x0)/Pci(0x2,0x0)/Pci(0x0,0x0)/\
Pci(0x8,0x0)/Pci(0x0,0x0)",
        "VendorID": 4098,
        "links": {
            "self": {
                "href": "/rest/v1/Systems/1/PCIDevices/6"
            }
        }
    }
  ]
}
"""

STORAGE_SETTINGS = """
{
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/SmartStorage$entity",
        "@odata.id": "/redfish/v1/Systems/1/SmartStorage/",
        "@odata.type": "#HpSmartStorage.HpSmartStorage",
        "Description": "HP Smart Storage",
        "Id": "1",
        "Links": {
        "ArrayControllers": {
                "@odata.id": "/redfish/v1/Systems/1\
/SmartStorage/ArrayControllers/"
                },
                "HostBusAdapters": {
                "@odata.id": "/redfish/v1/Systems/1/SmartStorage\
/HostBusAdapters/"
                }
        },
        "Name": "HpSmartStorage",
        "Status": {
                "Health": "OK"
                },
        "Type": "HpSmartStorage.1.0.0",
        "links": {
                "ArrayControllers": {
                        "href": "/rest/v1/Systems/1/SmartStorage\
/ArrayControllers"
                        },
                "HostBusAdapters": {
                        "href": "/rest/v1/Systems/1/SmartStorage\
/HostBusAdapters"
                },
        "self": {
                "href": "/rest/v1/Systems/1/SmartStorage"
                }
        }
}
"""

ARRAY_SETTINGS = """
{
        "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/SmartStorage/ArrayControllers",
        "@odata.id": "/redfish/v1/Systems/1/SmartStorage/ArrayControllers/",
        "@odata.type": "#HpSmartStorageArrayControllerCollection.\
1.0.0.HpSmartStorageArrayControllerCollection",
        "Description": "HP Smart Storage Array Controllers View",
        "MemberType": "HpSmartStorageArrayController.1",
        "Members": [{
                "@odata.id": "/redfish/v1/Systems/1/SmartStorage\
/ArrayControllers/0/"
        }],
        "Members@odata.count": 1,
        "Name": "HpSmartStorageArrayControllers",
        "Total": 1,
        "Type": "Collection.0.9.5",
        "links": {
        "Member": [{
                "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers/0"
                        }],
                "self": {
                        "href": "/rest/v1/Systems/1/SmartStorage/\
ArrayControllers"
                }
        }
}
"""

ARRAY_MEM_SETTINGS = """
{
    "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/SmartStorage/ArrayControllers/Members/$entity",
    "@odata.id": "/redfish/v1/Systems/1/SmartStorage/ArrayControllers/0/",
    "@odata.type": "#HpSmartStorageArrayController.\
HpSmartStorageArrayController",
    "AdapterType": "SmartArray",
    "BackupPowerSourceStatus": "Present",
    "CacheMemorySizeMiB": 1024,
    "CurrentOperatingMode": "RAID",
    "Description": "HP Smart Storage Array Controller View",
    "FirmwareVersion": {
        "Current": {
        "VersionString": "2.49"
    }
    },
    "HardwareRevision": "B",
    "Id": "0",
    "Links": {
        "LogicalDrives": {
            "@odata.id": "/redfish/v1/Systems/1/SmartStorage/\
ArrayControllers/0/LogicalDrives/"
        },
        "PhysicalDrives": {
            "@odata.id": "/redfish/v1/Systems/1/SmartStorage/\
ArrayControllers/0/DiskDrives/"
        },
        "StorageEnclosures": {
            "@odata.id": "/redfish/v1/Systems/1/SmartStorage/\
ArrayControllers/0/StorageEnclosures/"
        }
    },
    "Location": "Slot 0",
    "LocationFormat": "PCISlot",
    "Model": "HP Smart Array P244br Controller",
    "Name": "HpSmartStorageArrayController",
    "SerialNumber": "PDZVU0FLM7I03I",
    "Status": {
        "Health": "OK",
    "State": "Enabled"
    },
    "Type": "HpSmartStorageArrayController.1.0.0",
    "links": {
        "LogicalDrives": {
            "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers\
/0/LogicalDrives"
        },
        "PhysicalDrives": {
            "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers/\
0/DiskDrives"
        },
        "StorageEnclosures": {
            "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers/\
0/StorageEnclosures"
        },
        "self": {
            "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers/0"
        }
    }
}
"""

DISK_COLLECTION = """
{
    "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/SmartStorage/ArrayControllers/Members/2/DiskDrives",
    "@odata.id": "/redfish/v1/Systems/1/SmartStorage/ArrayControllers\
/2/DiskDrives/",
    "@odata.type": "\
#HpSmartStorageDiskDriveCollection.HpSmartStorageDiskDriveCollection",
    "Description": "HP Smart Storage Disk Drives View",
    "MemberType": "HpSmartStorageDiskDrive.1",
    "Members": [{
        "@odata.id": "/redfish/v1/Systems/1/SmartStorage/\
ArrayControllers/0/DiskDrives/0/"
        }],
    "Members@odata.count": 1,
    "Name": "HpSmartStorageDiskDrives",
    "Total": 1,
    "Type": "Collection.1.0.0",
    "links": {
    "Member": [{
        "href": "/rest/v1/Systems/1/SmartStorage/\
ArrayControllers/0/DiskDrives/0"
    }],
    "self": {
        "href": "/rest/v1/Systems/1/SmartStorage/\
ArrayControllers/0/DiskDrives"
        }
    }
}
"""
DISK_DETAILS_LIST = """
[{
    "@odata.context": "/redfish/v1/$metadata#Systems/Members/1\
/SmartStorage/ArrayControllers/Members/0/DiskDrives/Members/$entity",
    "@odata.id": "/redfish/v1/Systems/1/SmartStorage/ArrayControllers\
/0/DiskDrives/0/",
    "@odata.type": "#HpSmartStorageDiskDrive.HpSmartStorageDiskDrive",
    "CapacityMiB": 572325,
    "CurrentTemperatureCelsius": 25,
    "Description": "HP Smart Storage Disk Drive View",
    "EncryptedDrive": "False",
    "FirmwareVersion": {
    "Current": {
        "VersionString": "HPDC"
        }
    },
    "Id": "0",
    "InterfaceType": "SAS",
    "Location": "1I:1:1",
    "LocationFormat": "ControllerPort:Box:Bay",
    "MaximumTemperatureCelsius": 34,
    "MediaType": "HDD",
    "Model": "EG0600FBVFP",
    "Name": "HpSmartStorageDiskDrive",
    "RotationalSpeedRpm": 10000,
    "SerialNumber": "KWK1JS2X",
    "Status": {
        "Health": "OK",
        "State": "Enabled"
    },
    "Type": "HpSmartStorageDiskDrive.1.0.0",
    "links": {
        "self": {
            "href": "/rest/v1/Systems/1/SmartStorage/ArrayControllers\
/0/DiskDrives/0"
        }
    }
}]
"""
