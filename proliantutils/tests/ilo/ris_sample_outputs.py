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
