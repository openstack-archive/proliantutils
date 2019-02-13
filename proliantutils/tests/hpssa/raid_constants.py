# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

HPSSA_NO_DRIVES = '''
Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 21
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True



   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4ZN0000B41707PD
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 42
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H27F0000B41800S0
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2BR0000B41800V8
         Model: HP      EF0600FARNA
         Current Temperature (C): 32
         Maximum Temperature (C): 41
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4WD0000N4180GEJ
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 31
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''

HPSSA_DRIVES_SSD = '''
Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 21
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True



   unassigned

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: Solid State SAS
         Size: 200 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 31
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:8
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: Solid State SATA
         Size: 200 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 31
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''

HPSSA_ONE_DRIVE = '''
Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 22
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 0  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 558.9 GB
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 65535
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001C321CCA06EB7CD847939D
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 01F42227PDVTF0BRH5T0MOAB64
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   unassigned

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4ZN0000B41707PD
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 42
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H27F0000B41800S0
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2BR0000B41800V8
         Model: HP      EF0600FARNA
         Current Temperature (C): 32
         Maximum Temperature (C): 41
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4WD0000N4180GEJ
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 31
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''


HPSSA_ONE_DRIVE_RAID_50 = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 38
   Capacitor Temperature  (C): 23
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 3280165  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 100.0 GB
         Fault Tolerance: 50
         Number of Parity Groups: 2
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 25700
         Strip Size: 256 KB
         Full Stripe Size: 512 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Parity Initialization Status: Queued
         Unique Identifier: 600508B1001C0FC2145AA6F3A0AF2A57
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 02795E8FPDVTF0BRH5T0MOF6B8
         Parity Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
            physicaldrive 5I:1:3 (port 5I:box 1:bay 3, SAS, 600 GB, OK)
            physicaldrive 6I:1:5 (port 6I:box 1:bay 5, SAS, 600 GB, OK)
         Parity Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
            physicaldrive 5I:1:4 (port 5I:box 1:bay 4, SAS, 600 GB, OK)
            physicaldrive 6I:1:6 (port 6I:box 1:bay 6, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4ZN0000B41707PD
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 42
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H27F0000B41800S0
         Model: HP      EF0600FARNA
         Current Temperature (C): 38
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2BR0000B41800V8
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 41
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4WD0000N4180GEJ
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   unassigned

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G

'''

HPSSA_ONE_DRIVE_100GB_RAID_5 = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 38
   Capacitor Temperature  (C): 23
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 1563284  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 100.0 GB
         Fault Tolerance: 5
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 25700
         Strip Size: 256 KB
         Full Stripe Size: 512 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Parity Initialization Status: Queued
         Unique Identifier: 600508B1001CC42CDF101F06E5563967
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 02715627PDVTF0BRH5T0MO154D
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4ZN0000B41707PD
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 42
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H27F0000B41800S0
         Model: HP      EF0600FARNA
         Current Temperature (C): 38
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2BR0000B41800V8
         Model: HP      EF0600FARNA
         Current Temperature (C): 34
         Maximum Temperature (C): 41
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4WD0000N4180GEJ
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''


HPSSA_TWO_DRIVES_100GB_RAID5_50GB_RAID1 = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 38
   Capacitor Temperature  (C): 23
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 1563284  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 100.0 GB
         Fault Tolerance: 5
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 25700
         Strip Size: 256 KB
         Full Stripe Size: 512 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Parity Initialization Status: Queued
         Unique Identifier: 600508B1001CC42CDF101F06E5563967
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 02715627PDVTF0BRH5T0MO154D
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4ZN0000B41707PD
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 42
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H27F0000B41800S0
         Model: HP      EF0600FARNA
         Current Temperature (C): 38
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 400 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2BR0000B41800V8
         Model: HP      EF0600FARNA
         Current Temperature (C): 34
         Maximum Temperature (C): 41
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   Array: B
      Interface Type: SAS
      Unused Space: 1042189  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 2
         Size: 50.0 GB
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 12850
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001CE1E18302A8702C6AB008
         Disk Name: /dev/sdb
         Mount Points: None
         Logical Drive Label: 06715654PDVTF0BRH5T0MOACF0
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   unassigned

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4WD0000N4180GEJ
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 33
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''

HPSSA_BAD_SIZE_PHYSICAL_DRIVE = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 21
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True



   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500foo
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
'''


HPSSA_BAD_SIZE_LOGICAL_DRIVE = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 22
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 0  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 558.9foo
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 65535
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001C321CCA06EB7CD847939D
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 01F42227PDVTF0BRH5T0MOAB64
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
'''

HPSSA_SMALL_SIZE_PHYSICAL_DRIVE = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 21
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True



   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 2048 MB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
'''

ARRAY_ACCOMODATE_LOGICAL_DISK = '''

Available options are:
   Max: 1042188 (Units in MB)
   Min: 16 (Units in MB)

'''

ARRAY_ACCOMODATE_LOGICAL_DISK_INVALID = '''

Error: "raid=1" is not a valid option for array A

Available options are:
       0
       1adm
       5 (default value)

'''

HPSSA_NO_DRIVES_3_PHYSICAL_DISKS = '''
Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 21
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True



   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 700 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''

ONE_DRIVE_RAID_1 = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 38
   Capacitor Temperature  (C): 23
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 1042189  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 50.0 GB
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 12850
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001C02BDBCB659B8A264186A
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 02896A0EPDVTF0BRH5T0MOEBAA
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD5
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

   unassigned

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 500 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 35
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

'''

DRIVE_2_RAID_1_OKAY_TO_SHARE = '''

Available options are:
   Max: 521094 (Units in MB)
   Min: 16 (Units in MB)



'''

TWO_DRIVES_50GB_RAID1 = '''

Smart Array P822 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDVTF0BRH5T0MO
   Cache Serial Number: PBKUD0BRH5T3I6
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 4.68
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 3 secs
   Surface Scan Mode: Idle
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Inconsistency Repair Policy: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 15 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 10% Read / 90% Write
   Drive Write Cache: Disabled
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Temperature (C): 88
   Cache Module Temperature (C): 38
   Capacitor Temperature  (C): 23
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.4
   Driver Supports HP SSD Smart Path: True

   Array: A
      Interface Type: SAS
      Unused Space: 939791  MB
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable



      Logical Drive: 1
         Size: 50.0 GB
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 12850
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001C02BDBCB659B8A264186A
         Disk Name: /dev/sda
         Mount Points: None
         Logical Drive Label: 02896A0EPDVTF0BRH5T0MOEBAA
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache
      Logical Drive: 2
         Size: 50.0 GB
         Fault Tolerance: 1
         Heads: 255
         Sectors Per Track: 32
         Cylinders: 12850
         Strip Size: 256 KB
         Full Stripe Size: 256 KB
         Status: OK
         MultiDomain Status: OK
         Caching:  Enabled
         Unique Identifier: 600508B1001C1614116817E8A9DA1D2F
         Disk Name: /dev/sdb
         Mount Points: None
         Logical Drive Label: 06896EEAPDVTF0BRH5T0MO55C7
         Mirror Group 0:
            physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)
         Mirror Group 1:
            physicaldrive 5I:1:2 (port 5I:box 1:bay 2, SAS, 600 GB, OK)
         Drive Type: Data
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G55D0000N4173JLT
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 43
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6

   unassigned

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 600 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7H2DM0000B41800Y0
         Model: HP      EF0600FARNA
         Current Temperature (C): 37
         Maximum Temperature (C): 44
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6


   SEP (Vendor ID PMCSIERA, Model SRCv24x6G) 380
      Device Number: 380
      Firmware Version: RevB
      WWID: 5001438028842E1F
      Vendor ID: PMCSIERA
      Model: SRCv24x6G
'''


NO_DRIVES_HPSSA_7_DISKS = '''

Smart Array P822 in Slot 3
   Bus Interface: PCI
   Slot: 3
   Serial Number: PDVTF0BRH5T0KV

   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Interface Type: SAS
         Size: 199 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7G4QV0000B41803GZ
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Interface Type: SAS
         Size: 200 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7HK0Y0000N419008G
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Interface Type: SAS
         Size: 600 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1L50000B4180V5Y
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Interface Type: SAS
         Size: 599 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1K30000B41800TT
         Model: HP      EF0600FARNA

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Interface Type: SAS
         Size: 598 GB
         Firmware Revision: HPDB
         Serial Number: 2AVUR97N
         Model: HP      EF0600FATFF

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVJR1N
         Model: HP      EF0600FATFF

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVENJN
         Model: HP      EF0600FATFF
'''


ONE_DRIVE_RAID_1_50_GB = '''

Smart Array P822 in Slot 3
   Slot: 3
   Serial Number: PDVTF0BRH5T0KV

   Array: A
      Interface Type: SAS
      Unused Space: 1042189  MB (91.1%)
      Used Space: 100.0 GB (8.9%)

      Logical Drive: 1
         Size: 50.0 GB
         Fault Tolerance: 1
         Status: OK
         MultiDomain Status: OK
         Unique Identifier: 600508B1001C861A72C774A7394AE2AC
         Disk Name: /dev/sda
         Logical Drive Label: 013400ABPDVTF0BRH5T0KV22C5
         LD Acceleration Method: Controller Cache

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Interface Type: SAS
         Size: 199 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7G4QV0000B41803GZ
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Interface Type: SAS
         Size: 200 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7HK0Y0000N419008G
         Model: HP      EF0600FARNA

   unassigned

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Interface Type: SAS
         Size: 600 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1L50000B4180V5Y
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Interface Type: SAS
         Size: 599 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1K30000B41800TT
         Model: HP      EF0600FARNA

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Interface Type: SAS
         Size: 598 GB
         Firmware Revision: HPDB
         Serial Number: 2AVUR97N
         Model: HP      EF0600FATFF

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVJR1N
         Model: HP      EF0600FATFF

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVENJN
         Model: HP      EF0600FATFF
'''


TWO_DRIVES_50GB_RAID1_MAXGB_RAID5 = '''

Smart Array P822 in Slot 3
   Slot: 3
   Serial Number: PDVTF0BRH5T0KV

   Array: A
      Interface Type: SAS
      Unused Space: 1042189  MB (91.1%)
      Used Space: 100.0 GB (8.9%)
      Status: OK

      Logical Drive: 1
         Size: 50.0 GB
         Fault Tolerance: 1
         Status: OK
         Unique Identifier: 600508B1001C861A72C774A7394AE2AC
         Disk Name: /dev/sda

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Interface Type: SAS
         Size: 199 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7G4QV0000B41803GZ
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:2
         Port: 5I
         Box: 1
         Bay: 2
         Status: OK
         Interface Type: SAS
         Size: 200 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7HK0Y0000N419008G
         Model: HP      EF0600FARNA


   Array: B
      Interface Type: SAS
      Unused Space: 0  MB (0.0%)
      Used Space: 1.6 TB (100.0%)
      Status: OK
      MultiDomain Status: OK
      Array Type: Data
      HP SSD Smart Path: disable

      Logical Drive: 2
         Size: 1.1 TB
         Fault Tolerance: 5
         Status: OK
         Unique Identifier: 600508B1001CE9DE8551AEE29D5A72F7

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Interface Type: SAS
         Size: 600 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1L50000B4180V5Y
         Model: HP      EF0600FARNA

      physicaldrive 5I:1:4
         Port: 5I
         Box: 1
         Bay: 4
         Status: OK
         Interface Type: SAS
         Size: 599 GB
         Firmware Revision: HPD6
         Serial Number: 6SL7H1K30000B41800TT
         Model: HP      EF0600FARNA

      physicaldrive 6I:1:5
         Port: 6I
         Box: 1
         Bay: 5
         Status: OK
         Interface Type: SAS
         Size: 598 GB
         Firmware Revision: HPDB
         Serial Number: 2AVUR97N
         Model: HP      EF0600FATFF

   unassigned

      physicaldrive 6I:1:6
         Port: 6I
         Box: 1
         Bay: 6
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVJR1N

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Interface Type: SAS
         Size: 500 GB
         Firmware Revision: HPDB
         Serial Number: 2AVVENJN
         Model: HP      EF0600FATFF
'''

HPSSA_HBA_MODE = '''

Smart Array P822 in Slot 3
   Bus Interface: PCI
   Slot: 3
   Serial Number: PDVTF0BRH5T0KV
   Cache Serial Number: PBKUD0BRH5T3UM
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Hardware Revision: B
   Firmware Version: 5.22
   Cache Board Present: True
   Cache Status: Not Configured
   Total Cache Size: 2.0 GB
   Total Cache Memory Available: 1.8 GB
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   Controller Temperature (C): 88
   Cache Module Temperature (C): 37
   Capacitor Temperature  (C): 24
   Number of Ports: 6 (2 Internal / 4 External )
   Driver Name: hpsa
   Driver Version: 3.4.14
   HBA Mode Enabled: True
   PCI Address (Domain:Bus:Device.Function): 0000:0D:00.0
   Host Serial Number: SGH401AERD
   Sanitize Erase Supported: False
   Primary Boot Volume: None
   Secondary Boot Volume: None


   Port Name: 5I
         Port ID: 0
         Port Connection Number: 0
         SAS Address: 5001438028842E40
         Port Location: Internal

   Internal Drive Cage at Port 5I, Box 1, OK
      Power Supply Status: Not Redundant
      Drive Bays: 4
      Port: 5I
      Box: 1
      Location: Internal

   Physical Drives
      physicaldrive 5I:1:1 (port 5I:box 1:bay 1, SAS, 600 GB, OK)



   unassigned

      physicaldrive 5I:1:1
         Port: 5I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: HBA Mode Drive
         Interface Type: SAS
         Size: 600 GB
         Drive exposed to OS: True
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G4QV0000B41803GZ
         Model: HP      EF0600FARNA
         Current Temperature (C): 36
         Maximum Temperature (C): 45
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
         Disk Name: /dev/sda
         Mount Points: None
         Sanitize Erase Supported: False
'''

SSA_ERASE_DRIVE = '''

Smart Array P440 in Slot 2
   Bus Interface: PCI
   Slot: 2
   Serial Number: PDNMF0ARH8Y342
   RAID 6 (ADG) Status: Enabled
   Controller Status: OK
   Firmware Version: 4.52-0
   Spare Activation Mode: Activate on physical drive failure (default)
   Encryption: Disabled
   Driver Name: hpsa
   Driver Version: 3.4.16
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Controller Mode Reboot: Not Required
   Host Serial Number: SGH537Y7AY
   Sanitize Erase Supported: True
   Primary Boot Volume: None
   Secondary Boot Volume: None


   Port Name: 1I
         Port ID: 0
         Port Connection Number: 0
         SAS Address: 5001438035544EC0
         Port Location: Internal
         Managed Cable Connected: False

   Physical Drives
      physicaldrive 1I:2:1 (port 1I:box 2:bay 1, SAS HDD, 300 GB, OK)

   unassigned

      physicaldrive 1I:2:1
         Port: 1I
         Box: 2
         Bay: 1
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Drive exposed to OS: False
         Logical/Physical Block Size: 512/512
         Rotational Speed: 15100
         Firmware Revision: HPD4
         Serial Number: S7K0C3FJ0000K601EZLM
         WWID: 5000C5008E183B1D
         Model: HP      EH0300JEDHC
         Current Temperature (C): 42
         Maximum Temperature (C): 52
         PHY Count: 2
         PHY Transfer Rate: 12.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
         Sanitize Erase Supported: True
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
         Shingled Magnetic Recording Support: None

      physicaldrive 6I:1:7
         Port: 6I
         Box: 1
         Bay: 7
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: Solid State SAS
         Size: 200 GB
         Native Block Size: 512
         Rotational Speed: 15000
         Firmware Revision: HPD6
         Serial Number: 6SL7G54Q0000N4180W34
         Model: HP      EF0600FARNA
         Current Temperature (C): 31
         Maximum Temperature (C): 39
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         Drive Authentication Status: OK
         Carrier Application Version: 11
         Carrier Bootloader Version: 6
'''

SSA_ERASE_IN_PROGRESS = '''
Smart Array P440 in Slot 2
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Sanitize Erase Supported: True
   Primary Boot Volume: None
   Secondary Boot Volume: None

   unassigned

      physicaldrive 1I:2:1
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Status: Erase In Progress
         Drive Type: Unassigned Drive
         Sanitize Erase Supported: True
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
'''

SSA_ERASE_COMPLETE = '''
Smart Array P440 in Slot 2
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Sanitize Erase Supported: True
   Primary Boot Volume: None
   Secondary Boot Volume: None

   unassigned

      physicaldrive 1I:2:1
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Status: Erase Complete. Reenable Before Using.
         Drive Type: Unassigned Drive
         Sanitize Erase Supported: True
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
'''

SSA_ERASE_NOT_SUPPORTED = '''

Smart Array P440 in Slot 2
   Controller Status: OK
   Firmware Version: 4.52-0
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Controller Mode Reboot: Not Required
   Sanitize Erase Supported: False
   Primary Boot Volume: None
   Secondary Boot Volume: None

   unassigned

      physicaldrive 1I:2:1
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Status: OK
         Drive Type: Unassigned Drive
         Sanitize Erase Supported: False
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
'''

SSA_ERASE_COMPLETE_NOT_SUPPORTED = '''

Smart Array P440 in Slot 2
   Controller Status: OK
   Firmware Version: 4.52-0
   Spare Activation Mode: Activate on physical drive failure (default)
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Controller Mode Reboot: Not Required
   Sanitize Erase Supported: False
   Primary Boot Volume: None
   Secondary Boot Volume: None

   unassigned

      physicaldrive 1I:2:1
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Status: Erase Complete. Reenable Before Using.
         Drive Type: Unassigned Drive
         Sanitize Erase Supported: False
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
'''

SSA_ERASE_IN_PROGRESS_NOT_SUPPORTED = '''
Smart Array P440 in Slot 2
   Controller Mode: RAID
   Pending Controller Mode: RAID
   Sanitize Erase Supported: True
   Primary Boot Volume: None
   Secondary Boot Volume: None

   unassigned

      physicaldrive 1I:2:1
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 300 GB
         Status: Erase In Progress
         Drive Type: Unassigned Drive
         Sanitize Erase Supported: False
         Sanitize Estimated Max Erase Time: 0 hour(s)36 minute(s)
         Unrestricted Sanitize Supported: False
'''

SSACLI_PARSING_TESTS = '''
Smart HBA H240 in Slot 1 (RAID Mode)
   Slot: 1
   Controller Mode: RAID Mode

   Internal Drive Cage at Port 1I, Box 1, OK
      Drive Bays: 4
      Port: 1I
      Box: 1

   Physical Drives
      physicaldrive 1I:1:4 (port 1I:box 1:bay 4, SAS HDD, 900 GB, OK)
      physicaldrive 1I:1:3 (port 1I:box 1:bay 3, SAS HDD, 900 GB, OK)

   Internal Drive Cage at Port 2I, Box 1, OK
      Drive Bays: 4
      Port: 2I
      Box: 1

   Physical Drives
      physicaldrive 2I:1:5 (port 2I:box 1:bay 5, SAS HDD, 900 GB, OK)
      physicaldrive 2I:1:6 (port 2I:box 1:bay 6, SAS HDD, 900 GB, OK)

   Unassigned
      physicaldrive 1I:1:4
         Port: 1I
         Box: 1
         Bay: 4
         Size: 900 GB
         Interface Type: SAS

Smart HBA H240 in Slot 2 (RAID Mode)
   Slot: 2
   Controller Mode: RAID Mode
   PCI Address (Domain:Bus:Device.Function): 0000:0B:00.0

   Array: H
      Interface Type: SAS

      Logical Drive: 8
         Size: 838.3 GB
         Status: OK

      physicaldrive 2I:2:8
         Port: 2I
         Box: 2
         Bay: 8
         Size: 900 GB
         Interface Type: SAS

Smart HBA H240 in Slot 3 (RAID Mode)
   Slot: 3
   Controller Mode: RAID Mode

Smart HBA H240ar in Slot 0 (Embedded) (RAID Mode)
   Bus Interface: PCI
   Slot: 0
'''
