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
         Size: 600 GB
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
         Size: 600 GB
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
         Size: 600 GB
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
         Size: 600 GB
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
         Size: 600 GB
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


   unassigned

      physicaldrive 5I:1:3
         Port: 5I
         Box: 1
         Bay: 3
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SAS
         Size: 600 GB
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
         Size: 600 GB
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
         Size: 600 GB
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
         Drive Type: Unassigned Drive
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
