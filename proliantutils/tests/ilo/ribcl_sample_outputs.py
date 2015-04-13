# Copyright 2014 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Test Utils for iLO test modules."""

GET_VM_STATUS_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
   <GET_VM_STATUS VM_APPLET="DISCONNECTED" DEVICE="FLOPPY"
        BOOT_OPTION="BOOT_ALWAYS" WRITE_PROTECT="NO"
        IMAGE_INSERTED="YES"
        IMAGE_URL="http://1.2.3.4/floppy.img" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

GET_VM_STATUS_CDROM_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
   <GET_VM_STATUS VM_APPLET="DISCONNECTED" DEVICE="CDROM"
        BOOT_OPTION="BOOT_ONCE" WRITE_PROTECT="YES"
        IMAGE_INSERTED="NO" IMAGE_URL="" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

GET_VM_STATUS_ERROR_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0035"
             MESSAGE="An invalid Virtual Media option has been given" />
</RIBCL>
'''

GET_ALL_LICENSES_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
   <GET_ALL_LICENSES>
      <LICENSE>
         <LICENSE_TYPE VALUE="iLO 3 Advanced" />
         <LICENSE_KEY VALUE="XXXXX-XXXXX-XXXXX-XXXXX" />
         <LICENSE_INSTALL_DATE VALUE="Mon Dec  2 15:25:28 2013" />
         <LICENSE_CLASS VALUE="FQL" />
      </LICENSE>
   </GET_ALL_LICENSES>
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

GET_ONE_TIME_BOOT_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
   <ONE_TIME_BOOT>
      <BOOT_TYPE VALUE="Normal" />
   </ONE_TIME_BOOT>
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

GET_HOST_POWER_STATUS_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
   <GET_HOST_POWER HOST_POWER="ON" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

RESET_SERVER_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="Server being reset." />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

PRESS_POWER_BTN_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

SET_ONE_TIME_BOOT_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

SET_VM_STATUS_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

INSERT_VIRTUAL_MEDIA_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

EJECT_VIRTUAL_MEDIA_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0039"
             MESSAGE="No image present in the Virtual Media drive" />
</RIBCL>
'''

SET_HOST_POWER_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="Host power is already ON." />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

LOGIN_FAIL_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x005F" MESSAGE="Login failed." />
</RIBCL>
'''

HOLD_PWR_BTN_XML = '''
<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="Host power is already OFF." />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>

<?xml version="1.0" encoding="UTF-8"?>
<RIBCL VERSION="2.23">
   <RESPONSE STATUS="0x0000" MESSAGE="No error" />
</RIBCL>
'''

BOOT_MODE_NOT_SUPPORTED = '''
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x003C"
    MESSAGE='Feature not supported - GET_PENDING_BOOT_MODE'
    />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
'''

GET_PRODUCT_NAME = '''
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
  <GET_PRODUCT_NAME>
    <PRODUCT_NAME VALUE ="ProLiant DL380 G7"/>
  </GET_PRODUCT_NAME>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
'''

RESET_ILO_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<INFORM>Integrated Lights-Out will reset at the end of the script.</INFORM>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

RESET_ILO_CREDENTIAL_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

RESET_ILO_CREDENTIAL_FAIL_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0004"
    MESSAGE='Password is too short.'
     />
</RIBCL>
"""

GET_PERSISTENT_BOOT_DEVICE_HDD_UEFI_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<PERSISTENT_BOOT>
    <DEVICE value="Boot0007"
        DESCRIPTION="Embedded SAS : Smart Array P830i Controller - 279.367 GB,
             RAID 1 Logical Drive(Target:0, Lun:0)"/>
    <DEVICE value="Boot000B"
        DESCRIPTION="iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM"/>
    <DEVICE value="Boot000A"
        DESCRIPTION="iLO Virtual USB 1 : HP iLO Virtual USB Key"/>
    <DEVICE value="Boot0009"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 :HP Ethernet 1Gb
            4-port 331FLR Adapter - NIC (IPv4) "/>
    <DEVICE value="Boot0008"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 :HP Ethernet 1Gb
            4-port 331FLR Adapter - NIC (IPv6) "/>
</PERSISTENT_BOOT>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

GET_PERSISTENT_BOOT_DEVICE_NIC_UEFI_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<PERSISTENT_BOOT>
    <DEVICE value="Boot0009"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 :HP Ethernet 1Gb
            4-port 331FLR Adapter - NIC (IPv4) "/>
    <DEVICE value="Boot0007"
        DESCRIPTION="Embedded SAS : Smart Array P830i Controller - 279.367 GB,
             RAID 1 Logical Drive(Target:0, Lun:0)"/>
    <DEVICE value="Boot000B"
        DESCRIPTION="iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM"/>
    <DEVICE value="Boot000A"
        DESCRIPTION="iLO Virtual USB 1 : HP iLO Virtual USB Key"/>
    <DEVICE value="Boot0008"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 :HP Ethernet 1Gb
            4-port 331FLR Adapter - NIC (IPv6) "/>
</PERSISTENT_BOOT>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

GET_PERSISTENT_BOOT_DEVICE_BIOS_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<PERSISTENT_BOOT>
    <DEVICE value="CDROM"/>
    <DEVICE value="NETWORK"/>
    <DEVICE value="USB"/>
    <DEVICE value="FLOPPY"/>
    <DEVICE value="HDD"/>
</PERSISTENT_BOOT>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

GET_PERSISTENT_BOOT_DEVICE_CDROM_UEFI_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<PERSISTENT_BOOT>
    <DEVICE value="Boot000B"
        DESCRIPTION="iLO Virtual USB 2 : HP iLO Virtual USB CD/DVD ROM"/>
    <DEVICE value="Boot0007"
        DESCRIPTION="Embedded SAS : Smart Array P830i Controller - 279.367 GB,
             RAID 1 Logical Drive( Target:0, Lun:0)"/>
    <DEVICE value="Boot0009"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 : HP Ethernet 1Gb
             4-port 331FLR Adapter - NIC (IPv4) "/>
    <DEVICE value="Boot0008"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 : HP Ethernet 1Gb
             4-port 331FLR Adapter - NIC (IPv6) "/>
    <DEVICE value="Boot000A"
        DESCRIPTION="iLO Virtual USB 1 : HP iLO Virtual USB Key"/>
</PERSISTENT_BOOT>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

GET_PERSISTENT_BOOT_DEVICE_CDROM_MISSING_UEFI_XML = """
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<PERSISTENT_BOOT>
    <DEVICE value="Boot0007"
        DESCRIPTION="Embedded SAS : Smart Array P830i Controller - 279.367 GB,
             RAID 1 Logical Drive( Target:0, Lun:0)"/>
    <DEVICE value="Boot0009"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 : HP Ethernet 1Gb
             4-port 331FLR Adapter - NIC (IPv4) "/>
    <DEVICE value="Boot0008"
        DESCRIPTION="Embedded FlexibleLOM 1 Port 1 : HP Ethernet 1Gb
             4-port 331FLR Adapter - NIC (IPv6) "/>
    <DEVICE value="Boot000A"
        DESCRIPTION="iLO Virtual USB 1 : HP iLO Virtual USB Key"/>
</PERSISTENT_BOOT>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
"""

GET_NIC_DEVICES_DATA = '''
[{"DESCRIPTION": "Slot 1 : Smart Array P840 Controller - 279.37 GiB, RAID 0\
  Logical Drive(Target:0, Lun:0)", "value": "Boot000E"}, {"DESCRIPTION": \
  "Slot 1 : Smart Array P840 Controller - 279.37 GiB, RAID 0 Logical Drive\
  (Target:0, Lun:1)", "value": "Boot000F"}, {"DESCRIPTION": "Embedded LOM 1\
  Port 1 : HP Ethernet 1Gb 4-port 331i Adapter - NIC (iSCSI IPv4) ", "value":\
  "Boot0004"}, {"DESCRIPTION": "Embedded LOM 1 Port 2 : HP Ethernet 1Gb \
  4-port 331i Adapter - NIC (PXE IPv4) ", "value": "Boot0003"},
  {"DESCRIPTION": "Embedded LOM 1 Port 2 : HP Ethernet 1Gb \
   4-port 331i Adapter - NIC IPv4 ", "value": "Boot0001"},
  {"DESCRIPTION": "Generic USB Boot", "value": "Boot0000"}]
'''

GET_NIC_DATA = '''
[
    {
        "DESCRIPTION": "Slot 1 : Smart Array P840 Controller - 279.37 GiB,\
                        RAID 0 Logical Drive(Target:0, Lun:0)",
        "value": "Boot000E"
    },
    {
        "DESCRIPTION": "Slot1:SmartArrayP840Controller-279.37GiB, RAID0 \
                        LogicalDrive(Target: 0, Lun: 1)",
        "value": "Boot000F"
    },
    {
        "DESCRIPTION": "EmbeddedLOM1 Port1: HPEthernet1Gb4-port331iAdapter-\
                        NIC(iSCSIIPv4)",
        "value": "Boot0004"
    },
    {
        "DESCRIPTION": "EmbeddedLOM1Port2: HPEthernet1Gb4-port331iAdapter-\
                        NIC(PXEIPv4)",
        "value": "Boot0003"
    },
    {
        "DESCRIPTION": "EmbeddedLOM1Port2: HPEthernet1Gb 4-port331iAdapter-\
                        NIC IPv4",
        "value": "Boot0001"
    },
    {
        "DESCRIPTION": "GenericUSBBoot",
        "value": "Boot0000"
    }
]
'''

GET_HOST_UUID = '''
<RIMP>
<HSI>
<SBSN>2M220102JA      </SBSN>
<SPN>ProLiant ML110 G7</SPN>
<UUID>6567662M220102JA</UUID>
<SP>1</SP>
<cUUID>37363536-3636-4D32-3232-303130324A41</cUUID>
<VIRTUAL>
<STATE>Inactive</STATE>
<VID>
<BSN></BSN>
<cUUID></cUUID>
</VID>
</VIRTUAL>
</HSI>
<MP>
<ST>1</ST>
<PN>Integrated Lights-Out 3 (iLO 3)</PN>
<FWRI>1.70</FWRI>
<BBLK>01/08/2011</BBLK>
<HWRI>ASIC: 12</HWRI>
<SN>ILO2M220102JA      </SN>
<UUID>ILO6567662M220102JA</UUID>
<IPM>1</IPM>
<SSO>0</SSO>
<PWRM>1.7</PWRM>
</MP>
</RIMP>
'''

GET_HOST_HEALTH_DATA = '''
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<GET_EMBEDDED_HEALTH_DATA>
    <FANS>
       <FAN>
            <ZONE VALUE = "System"/>
            <LABEL VALUE = "Fan 1"/>
            <STATUS VALUE = "OK"/>
                <SPEED VALUE = "31" UNIT="Percentage"/>
       </FAN>
       <FAN>
            <ZONE VALUE = "System"/>
            <LABEL VALUE = "Fan 7"/>
            <STATUS VALUE = "OK"/>
                <SPEED VALUE = "13" UNIT="Percentage"/>
       </FAN>
       <FAN>
            <ZONE VALUE = "System"/>
            <LABEL VALUE = "Fan 8"/>
            <STATUS VALUE = "OK"/>
                <SPEED VALUE = "10" UNIT="Percentage"/>
       </FAN>
    </FANS>
    <TEMPERATURE>
       <TEMP>
            <LABEL VALUE = "01-Inlet Ambient"/>
            <LOCATION VALUE = "Ambient"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "16" UNIT="Celsius"/>
            <CAUTION VALUE = "42" UNIT="Celsius"/>
            <CRITICAL VALUE = "46" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "02-CPU"/>
            <LOCATION VALUE = "CPU"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "40" UNIT="Celsius"/>
            <CAUTION VALUE = "74" UNIT="Celsius"/>
            <CRITICAL VALUE = "75" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "03-P1 DIMM 1-4"/>
            <LOCATION VALUE = "Memory"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "26" UNIT="Celsius"/>
            <CAUTION VALUE = "87" UNIT="Celsius"/>
            <CRITICAL VALUE = "92" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "04-P1 Mem Zone"/>
            <LOCATION VALUE = "Memory"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "33" UNIT="Celsius"/>
            <CAUTION VALUE = "70" UNIT="Celsius"/>
            <CRITICAL VALUE = "75" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "05-P1 Mem Zone"/>
            <LOCATION VALUE = "Memory"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "31" UNIT="Celsius"/>
            <CAUTION VALUE = "70" UNIT="Celsius"/>
            <CRITICAL VALUE = "75" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "06-HD Max"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "50" UNIT="Celsius"/>
            <CAUTION VALUE = "60" UNIT="Celsius"/>
            <CRITICAL VALUE = "65" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "07-VR P1"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "30" UNIT="Celsius"/>
            <CAUTION VALUE = "110" UNIT="Celsius"/>
            <CRITICAL VALUE = "120" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "08-VR P1"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "37" UNIT="Celsius"/>
            <CAUTION VALUE = "110" UNIT="Celsius"/>
            <CRITICAL VALUE = "120" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "09-VR P1 Zone"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "28" UNIT="Celsius"/>
            <CAUTION VALUE = "92" UNIT="Celsius"/>
            <CRITICAL VALUE = "97" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "10-VR P1Mem Zone"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "26" UNIT="Celsius"/>
            <CAUTION VALUE = "95" UNIT="Celsius"/>
            <CRITICAL VALUE = "100" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "15-System Board"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "22" UNIT="Celsius"/>
            <CAUTION VALUE = "50" UNIT="Celsius"/>
            <CRITICAL VALUE = "55" UNIT="Celsius"/>
       </TEMP>
       <TEMP>
            <LABEL VALUE = "16-System Board"/>
            <LOCATION VALUE = "System"/>
            <STATUS VALUE = "OK"/>
            <CURRENTREADING VALUE = "29" UNIT="Celsius"/>
            <CAUTION VALUE = "65" UNIT="Celsius"/>
            <CRITICAL VALUE = "70" UNIT="Celsius"/>
       </TEMP>
    </TEMPERATURE>
    <POWER_SUPPLIES>
       <POWER_SUPPLY_SUMMARY>
            <PRESENT_POWER_READING VALUE = "37 Watts"/>
            <POWER_MANAGEMENT_CONTROLLER_FIRMWARE_VERSION VALUE = "1.7"/>
            <HIGH_EFFICIENCY_MODE VALUE = "Balanced"/>
       </POWER_SUPPLY_SUMMARY>
       <SUPPLY>
            <LABEL VALUE = "Power Supply 1"/>
            <STATUS VALUE = "OK"/>
       </SUPPLY>
       <SUPPLY>
            <LABEL VALUE = "Power Supply 2"/>
            <STATUS VALUE = "Not Installed"/>
       </SUPPLY>
    </POWER_SUPPLIES>
    <VRM>
      <MODULE>
            <LABEL VALUE = "VRM 1"/>
            <STATUS VALUE = "OK"/>
      </MODULE>
    </VRM>
    <PROCESSORS>
       <PROCESSOR>
            <LABEL VALUE = "Proc 1"/>
            <SPEED VALUE = "3300 MHz"/>
            <EXECUTION_TECHNOLOGY VALUE = "4/4 cores; 8 threads"/>
            <MEMORY_TECHNOLOGY VALUE = "64-bit Capable"/>
            <INTERNAL_L1_CACHE VALUE = "128 KB"/>
            <INTERNAL_L2_CACHE VALUE = "1024 KB"/>
            <INTERNAL_L3_CACHE VALUE = "8192 KB"/>
       </PROCESSOR>
    </PROCESSORS>
    <MEMORY>
       <MEMORY_COMPONENTS>
            <MEMORY_COMPONENT>
                <MEMORY_LOCATION VALUE = "DIMM  1 "/>
                <MEMORY_SIZE VALUE = "Not Installed"/>
                <MEMORY_SPEED VALUE = "0 MHz"/>
            </MEMORY_COMPONENT>
            <MEMORY_COMPONENT>
                <MEMORY_LOCATION VALUE = "DIMM  2 "/>
                <MEMORY_SIZE VALUE = "4096 MB"/>
                <MEMORY_SPEED VALUE = "1333 MHz"/>
            </MEMORY_COMPONENT>
            <MEMORY_COMPONENT>
                <MEMORY_LOCATION VALUE = "DIMM  3 "/>
                <MEMORY_SIZE VALUE = "Not Installed"/>
                <MEMORY_SPEED VALUE = "0 MHz"/>
            </MEMORY_COMPONENT>
            <MEMORY_COMPONENT>
                <MEMORY_LOCATION VALUE = "DIMM  4 "/>
                <MEMORY_SIZE VALUE = "4096 MB"/>
                <MEMORY_SPEED VALUE = "1333 MHz"/>
            </MEMORY_COMPONENT>
       </MEMORY_COMPONENTS>
    </MEMORY>
    <NIC_INFOMATION>
       <NIC>
            <NETWORK_PORT VALUE = "Port 1"/>
            <MAC_ADDRESS VALUE = "e4:11:5b:a9:ae:70"/>
       </NIC>
       <NIC>
            <NETWORK_PORT VALUE = "Port 2"/>
            <MAC_ADDRESS VALUE = "e4:11:5b:a9:ae:71"/>
       </NIC>
       <iLO>
            <NETWORK_PORT VALUE = "iLO Dedicated Network Port"/>
            <MAC_ADDRESS VALUE = "e4:11:5b:a9:ae:73"/>
       </iLO>
    </NIC_INFOMATION>
    <FIRMWARE_INFORMATION>
       <INDEX_1>
            <FIRMWARE_NAME VALUE = "HP ProLiant System ROM"/>
            <FIRMWARE_VERSION VALUE = "07/01/2013"/>
       </INDEX_1>
       <INDEX_2>
            <FIRMWARE_NAME VALUE = "HP ProLiant System ROM - Backup"/>
            <FIRMWARE_VERSION VALUE = "12/04/2012"/>
       </INDEX_2>
       <INDEX_3>
            <FIRMWARE_NAME VALUE = "HP ProLiant System ROM Bootblock"/>
            <FIRMWARE_VERSION VALUE = "01/08/2011"/>
       </INDEX_3>
       <INDEX_4>
            <FIRMWARE_NAME VALUE = "iLO"/>
            <FIRMWARE_VERSION VALUE = "1.70 Pass 25 Jan 09 2014"/>
       </INDEX_4>
       <INDEX_5>
            <FIRMWARE_NAME VALUE = "Power Management Controller"/>
            <FIRMWARE_VERSION VALUE = "Version 1.7"/>
       </INDEX_5>
       <INDEX_6>
            <FIRMWARE_NAME VALUE = "CPLD - PAL0"/>
            <FIRMWARE_VERSION VALUE = "ProLiant ML110 G7 PAL version 0x0C"/>
       </INDEX_6>
    </FIRMWARE_INFORMATION>
    <DRIVES>
    </DRIVES>
    <HEALTH_AT_A_GLANCE>
       <FANS STATUS= "OK"/>
       <TEMPERATURE STATUS= "OK"/>
       <VRM STATUS= "OK"/>
       <POWER_SUPPLIES STATUS= "OK"/>
       <POWER_SUPPLIES REDUNDANCY= "Not Redundant"/>
       <DRIVE STATUS= "OK"/>
    </HEALTH_AT_A_GLANCE>
</GET_EMBEDDED_HEALTH_DATA>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
'''

GET_HOST_POWER_READINGS = '''
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
<GET_POWER_READINGS>
<PRESENT_POWER_READING VALUE="37" UNIT="Watts"/>
<AVERAGE_POWER_READING VALUE="37" UNIT="Watts"/>
<MAXIMUM_POWER_READING VALUE="82" UNIT="Watts"/>
<MINIMUM_POWER_READING VALUE="37" UNIT="Watts"/>
</GET_POWER_READINGS>
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
<?xml version="1.0"?>
<RIBCL VERSION="2.23">
<RESPONSE
    STATUS="0x0000"
    MESSAGE='No error'
     />
</RIBCL>
'''

GET_EMBEDDED_HEALTH_OUTPUT = '''
{
    "GET_EMBEDDED_HEALTH_DATA": {
        "FANS": {
            "FAN": [
                {
                    "LABEL": {
                        "VALUE": "Fan Block 1"
                    },
                    "SPEED": {
                        "UNIT": "Percentage",
                        "VALUE": "12"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    },
                    "ZONE": {
                        "VALUE": "System"
                    }
                },
                {
                    "LABEL": {
                        "VALUE": "Fan Block 2"
                    },
                    "SPEED": {
                        "UNIT": "Percentage",
                        "VALUE": "12"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    },
                    "ZONE": {
                        "VALUE": "System"
                    }
                },
                {
                    "LABEL": {
                        "VALUE": "Fan Block 3"
                    },
                    "SPEED": {
                        "UNIT": "Percentage",
                        "VALUE": "18"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    },
                    "ZONE": {
                        "VALUE": "System"
                    }
                },
                {
                    "LABEL": {
                        "VALUE": "Fan Block 4"
                    },
                    "SPEED": {
                        "UNIT": "Percentage",
                        "VALUE": "18"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    },
                    "ZONE": {
                        "VALUE": "System"
                    }
                }
            ]
        },
        "FIRMWARE_INFORMATION": {
            "INDEX_1": {
                "FIRMWARE_NAME": {
                    "VALUE": "HP ProLiant System ROM"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "11/26/2014"
                }
            },
            "INDEX_10": {
                "FIRMWARE_NAME": {
                    "VALUE": "HP Smart Array P830i Controller"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "1.62"
                }
            },
            "INDEX_2": {
                "FIRMWARE_NAME": {
                    "VALUE": "HP ProLiant System ROM - Backup"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "11/26/2014"
                }
            },
            "INDEX_3": {
                "FIRMWARE_NAME": {
                    "VALUE": "HP ProLiant System ROM Bootblock"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": ""
                }
            },
            "INDEX_4": {
                "FIRMWARE_NAME": {
                    "VALUE": "iLO"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "2.02 Sep 05 2014"
                }
            },
            "INDEX_5": {
                "FIRMWARE_FAMILY": {
                    "VALUE": "0Ch"
                },
                "FIRMWARE_NAME": {
                    "VALUE": "Power Management Controller Firmware"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "4.1"
                }
            },
            "INDEX_6": {
                "FIRMWARE_NAME": {
                    "VALUE": "Power Management Controller FW Bootloader"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "2.7"
                }
            },
            "INDEX_7": {
                "FIRMWARE_NAME": {
                    "VALUE": "System Programmable Logic Device"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "Version 0x0B"
                }
            },
            "INDEX_8": {
                "FIRMWARE_NAME": {
                    "VALUE": "SAS Programmable Logic Device"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "Version 0x04"
                }
            },
            "INDEX_9": {
                "FIRMWARE_NAME": {
                    "VALUE": "Server Platform Services (SPS) Firmware"
                },
                "FIRMWARE_VERSION": {
                    "VALUE": "2.3.0.FA.0"
                }
            }
        },
        "HEALTH_AT_A_GLANCE": {
            "BIOS_HARDWARE": {
                "STATUS": "OK"
            },
            "FANS": [
                {
                    "STATUS": "OK"
                },
                {
                    "REDUNDANCY": "Redundant"
                }
            ],
            "MEMORY": {
                "STATUS": "Other"
            },
            "NETWORK": {
                "STATUS": "OK"
            },
            "POWER_SUPPLIES": [
                {
                    "STATUS": "OK"
                },
                {
                    "REDUNDANCY": "Redundant"
                }
            ],
            "PROCESSOR": {
                "STATUS": "OK"
            },
            "STORAGE": {
                "STATUS": "OK"
            },
            "TEMPERATURE": {
                "STATUS": "OK"
            }
        },
        "MEMORY": {
            "ADVANCED_MEMORY_PROTECTION": {
                "AMP_MODE_STATUS": {
                    "VALUE": "Unknown"
                },
                "AVAILABLE_AMP_MODES": {
                    "VALUE": "Unknown"
                },
                "CONFIGURED_AMP_MODE": {
                    "VALUE": "Unknown"
                }
            },
            "MEMORY_DETAILS": {
                "Memory_Board_1": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "1866 MHz"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "Yes"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "1.50 v"
                        },
                        "PART": {
                            "NUMBER": "731657-081"
                        },
                        "RANKS": {
                            "VALUE": "1"
                        },
                        "SIZE": {
                            "VALUE": "8192 MB"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Good, In Use"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "RDIMM"
                        },
                        "TYPE": {
                            "VALUE": "DIMM DDR3"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "1866 MHz"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "Yes"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "1.50 v"
                        },
                        "PART": {
                            "NUMBER": "731657-081"
                        },
                        "RANKS": {
                            "VALUE": "1"
                        },
                        "SIZE": {
                            "VALUE": "8192 MB"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Good, In Use"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "RDIMM"
                        },
                        "TYPE": {
                            "VALUE": "DIMM DDR3"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_2": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_3": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "1866 MHz"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "Yes"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "1.50 v"
                        },
                        "PART": {
                            "NUMBER": "731657-081"
                        },
                        "RANKS": {
                            "VALUE": "1"
                        },
                        "SIZE": {
                            "VALUE": "8192 MB"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Good, In Use"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "RDIMM"
                        },
                        "TYPE": {
                            "VALUE": "DIMM DDR3"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "1866 MHz"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "Yes"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "1.50 v"
                        },
                        "PART": {
                            "NUMBER": "731657-081"
                        },
                        "RANKS": {
                            "VALUE": "1"
                        },
                        "SIZE": {
                            "VALUE": "8192 MB"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Good, In Use"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "RDIMM"
                        },
                        "TYPE": {
                            "VALUE": "DIMM DDR3"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_4": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_5": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_6": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_7": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ],
                "Memory_Board_8": [
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "1"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "2"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "3"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "4"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "5"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "6"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "7"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "8"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "9"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "10"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "11"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    },
                    {
                        "FREQUENCY": {
                            "VALUE": "N/A"
                        },
                        "HP_SMART_MEMORY": {
                            "VALUE": "N/A"
                        },
                        "MINIMUM_VOLTAGE": {
                            "VALUE": "N/A"
                        },
                        "PART": {
                            "NUMBER": "N/A"
                        },
                        "RANKS": {
                            "VALUE": "N/A"
                        },
                        "SIZE": {
                            "VALUE": "N/A"
                        },
                        "SOCKET": {
                            "VALUE": "12"
                        },
                        "STATUS": {
                            "VALUE": "Not Present"
                        },
                        "TECHNOLOGY": {
                            "VALUE": "N/A"
                        },
                        "TYPE": {
                            "VALUE": "N/A"
                        }
                    }
                ]
            },
            "MEMORY_DETAILS_SUMMARY": {
                "Memory_Board_1": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "1067 MHz"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "1.50 v"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "16 GB"
                    }
                },
                "Memory_Board_2": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                },
                "Memory_Board_3": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "1067 MHz"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "1.50 v"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "16 GB"
                    }
                },
                "Memory_Board_4": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                },
                "Memory_Board_5": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                },
                "Memory_Board_6": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                },
                "Memory_Board_7": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                },
                "Memory_Board_8": {
                    "NUMBER_OF_SOCKETS": {
                        "VALUE": "12"
                    },
                    "OPERATING_FREQUENCY": {
                        "VALUE": "N/A"
                    },
                    "OPERATING_VOLTAGE": {
                        "VALUE": "N/A"
                    },
                    "TOTAL_MEMORY_SIZE": {
                        "VALUE": "N/A"
                    }
                }
            }
        },
        "NIC_INFORMATION": {
            "NIC": [
                {
                    "IP_ADDRESS": {
                        "VALUE": "N/A"
                    },
                    "LOCATION": {
                        "VALUE": "Embedded"
                    },
                    "MAC_ADDRESS": {
                        "VALUE": "40:a8:f0:1e:86:74"
                    },
                    "NETWORK_PORT": {
                        "VALUE": "Port 1"
                    },
                    "PORT_DESCRIPTION": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                },
                {
                    "IP_ADDRESS": {
                        "VALUE": "N/A"
                    },
                    "LOCATION": {
                        "VALUE": "Embedded"
                    },
                    "MAC_ADDRESS": {
                        "VALUE": "40:a8:f0:1e:86:75"
                    },
                    "NETWORK_PORT": {
                        "VALUE": "Port 2"
                    },
                    "PORT_DESCRIPTION": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                },
                {
                    "IP_ADDRESS": {
                        "VALUE": "N/A"
                    },
                    "LOCATION": {
                        "VALUE": "Embedded"
                    },
                    "MAC_ADDRESS": {
                        "VALUE": "40:a8:f0:1e:86:76"
                    },
                    "NETWORK_PORT": {
                        "VALUE": "Port 3"
                    },
                    "PORT_DESCRIPTION": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                },
                {
                    "IP_ADDRESS": {
                        "VALUE": "N/A"
                    },
                    "LOCATION": {
                        "VALUE": "Embedded"
                    },
                    "MAC_ADDRESS": {
                        "VALUE": "40:a8:f0:1e:86:77"
                    },
                    "NETWORK_PORT": {
                        "VALUE": "Port 4"
                    },
                    "PORT_DESCRIPTION": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                }
            ],
            "iLO": {
                "IP_ADDRESS": {
                    "VALUE": "10.10.1.66"
                },
                "LOCATION": {
                    "VALUE": "Embedded"
                },
                "MAC_ADDRESS": {
                    "VALUE": "fc:15:b4:18:c0:d4"
                },
                "NETWORK_PORT": {
                    "VALUE": "iLO Dedicated Network Port"
                },
                "PORT_DESCRIPTION": {
                    "VALUE": "iLO Dedicated Network Port"
                },
                "STATUS": {
                    "VALUE": "OK"
                }
            }
        },
        "POWER_SUPPLIES": {
            "POWER_SUPPLY_SUMMARY": {
                "HIGH_EFFICIENCY_MODE": {
                    "VALUE": "Balanced"
                },
                "HP_POWER_DISCOVERY_SERVICES_REDUNDANCY_STATUS": {
                    "VALUE": "N/A"
                },
                "POWER_MANAGEMENT_CONTROLLER_FIRMWARE_VERSION": {
                    "VALUE": "4.1"
                },
                "POWER_SYSTEM_REDUNDANCY": {
                    "VALUE": "Redundant"
                },
                "PRESENT_POWER_READING": {
                    "VALUE": "162 Watts"
                }
            },
            "SUPPLY": [
                {
                    "CAPACITY": {
                        "VALUE": "1200 Watts"
                    },
                    "FIRMWARE_VERSION": {
                        "VALUE": "1.00"
                    },
                    "HOTPLUG_CAPABLE": {
                        "VALUE": "Yes"
                    },
                    "LABEL": {
                        "VALUE": "Power Supply 1"
                    },
                    "MODEL": {
                        "VALUE": "656364-B21"
                    },
                    "PDS": {
                        "VALUE": "Yes"
                    },
                    "PRESENT": {
                        "VALUE": "Yes"
                    },
                    "SERIAL_NUMBER": {
                        "VALUE": "5BXRC0D4D6X0X1"
                    },
                    "SPARE": {
                        "VALUE": "660185-001"
                    },
                    "STATUS": {
                        "VALUE": "Good, In Use"
                    }
                },
                {
                    "CAPACITY": {
                        "VALUE": "1200 Watts"
                    },
                    "FIRMWARE_VERSION": {
                        "VALUE": "1.00"
                    },
                    "HOTPLUG_CAPABLE": {
                        "VALUE": "Yes"
                    },
                    "LABEL": {
                        "VALUE": "Power Supply 2"
                    },
                    "MODEL": {
                        "VALUE": "656364-B21"
                    },
                    "PDS": {
                        "VALUE": "Yes"
                    },
                    "PRESENT": {
                        "VALUE": "Yes"
                    },
                    "SERIAL_NUMBER": {
                        "VALUE": "5BXRC0D4D6X0WR"
                    },
                    "SPARE": {
                        "VALUE": "660185-001"
                    },
                    "STATUS": {
                        "VALUE": "Good, In Use"
                    }
                },
                {
                    "CAPACITY": {
                        "VALUE": "N/A Watts"
                    },
                    "FIRMWARE_VERSION": {
                        "VALUE": "N/A"
                    },
                    "HOTPLUG_CAPABLE": {
                        "VALUE": "Yes"
                    },
                    "LABEL": {
                        "VALUE": "Power Supply 3"
                    },
                    "MODEL": {
                        "VALUE": "N/A"
                    },
                    "PDS": {
                        "VALUE": "Other"
                    },
                    "PRESENT": {
                        "VALUE": "No"
                    },
                    "SERIAL_NUMBER": {
                        "VALUE": "N/A"
                    },
                    "SPARE": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                },
                {
                    "CAPACITY": {
                        "VALUE": "N/A Watts"
                    },
                    "FIRMWARE_VERSION": {
                        "VALUE": "N/A"
                    },
                    "HOTPLUG_CAPABLE": {
                        "VALUE": "Yes"
                    },
                    "LABEL": {
                        "VALUE": "Power Supply 4"
                    },
                    "MODEL": {
                        "VALUE": "N/A"
                    },
                    "PDS": {
                        "VALUE": "Other"
                    },
                    "PRESENT": {
                        "VALUE": "No"
                    },
                    "SERIAL_NUMBER": {
                        "VALUE": "N/A"
                    },
                    "SPARE": {
                        "VALUE": "N/A"
                    },
                    "STATUS": {
                        "VALUE": "Unknown"
                    }
                }
            ]
        },
        "PROCESSORS": {
            "PROCESSOR": [
                {
                    "EXECUTION_TECHNOLOGY": {
                        "VALUE": "8/8 cores; 16 threads"
                    },
                    "INTERNAL_L1_CACHE": {
                        "VALUE": "64 KB"
                    },
                    "INTERNAL_L2_CACHE": {
                        "VALUE": "256 KB"
                    },
                    "INTERNAL_L3_CACHE": {
                        "VALUE": "16384 KB"
                    },
                    "LABEL": {
                        "VALUE": "Proc 1"
                    },
                    "MEMORY_TECHNOLOGY": {
                        "VALUE": "64-bit Capable"
                    },
                    "NAME": {
                        "VALUE": "Intel(R) Xeon(R) CPU E7-4820 v2 @ 2.00GHz"
                    },
                    "SPEED": {
                        "VALUE": "2000 MHz"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "EXECUTION_TECHNOLOGY": {
                        "VALUE": "8/8 cores; 16 threads"
                    },
                    "INTERNAL_L1_CACHE": {
                        "VALUE": "64 KB"
                    },
                    "INTERNAL_L2_CACHE": {
                        "VALUE": "256 KB"
                    },
                    "INTERNAL_L3_CACHE": {
                        "VALUE": "16384 KB"
                    },
                    "LABEL": {
                        "VALUE": "Proc 2"
                    },
                    "MEMORY_TECHNOLOGY": {
                        "VALUE": "64-bit Capable"
                    },
                    "NAME": {
                        "VALUE": "Intel(R) Xeon(R) CPU E7-4820 v2 @ 2.00GHz"
                    },
                    "SPEED": {
                        "VALUE": "2000 MHz"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                }
            ]
        },
        "STORAGE": {
            "CONTROLLER": {
                "CACHE_MODULE_MEMORY": {
                    "VALUE": "2097152 KB"
                },
                "CACHE_MODULE_SERIAL_NUM": {
                    "VALUE": "PBKUD0BRH6U3KO"
                },
                "CACHE_MODULE_STATUS": {
                    "VALUE": "OK"
                },
                "CONTROLLER_STATUS": {
                    "VALUE": "OK"
                },
                "DRIVE_ENCLOSURE": [
                    {
                        "DRIVE_BAY": {
                            "VALUE": "04"
                        },
                        "LABEL": {
                            "VALUE": "Port 1I Box 1"
                        },
                        "STATUS": {
                            "VALUE": "OK"
                        }
                    },
                    {
                        "DRIVE_BAY": {
                            "VALUE": "01"
                        },
                        "LABEL": {
                            "VALUE": "Port 1I Box 0"
                        },
                        "STATUS": {
                            "VALUE": "OK"
                        }
                    }
                ],
                "ENCRYPTION_CSP_STATUS": {
                    "VALUE": "OK"
                },
                "ENCRYPTION_SELF_TEST_STATUS": {
                    "VALUE": "OK"
                },
                "ENCRYPTION_STATUS": {
                    "VALUE": "Not Enabled"
                },
                "FW_VERSION": {
                    "VALUE": "1.62"
                },
                "LABEL": {
                    "VALUE": "Controller on System Board"
                },
                "LOGICAL_DRIVE": {
                    "CAPACITY": {
                        "VALUE": "99 GB"
                    },
                    "ENCRYPTION_STATUS": {
                        "VALUE": "Not Encrypted"
                    },
                    "FAULT_TOLERANCE": {
                        "VALUE": "RAID 1/RAID 1+0"
                    },
                    "LABEL": {
                        "VALUE": "01"
                    },
                    "PHYSICAL_DRIVE": [
                        {
                            "CAPACITY": {
                                "VALUE": "279 GB"
                            },
                            "DRIVE_CONFIGURATION": {
                                "VALUE": "Configured"
                            },
                            "ENCRYPTION_STATUS": {
                                "VALUE": "Not Encrypted"
                            },
                            "FW_VERSION": {
                                "VALUE": "HPD0"
                            },
                            "LABEL": {
                                "VALUE": "Port 1I Box 1 Bay 1"
                            },
                            "LOCATION": {
                                "VALUE": "Port 1I Box 1 Bay 1"
                            },
                            "MODEL": {
                                "VALUE": "EG0300FCSPH"
                            },
                            "SERIAL_NUMBER": {
                                "VALUE": "64R0A18KFTM91426"
                            },
                            "STATUS": {
                                "VALUE": "OK"
                            }
                        },
                        {
                            "CAPACITY": {
                                "VALUE": "279 GB"
                            },
                            "DRIVE_CONFIGURATION": {
                                "VALUE": "Configured"
                            },
                            "ENCRYPTION_STATUS": {
                                "VALUE": "Not Encrypted"
                            },
                            "FW_VERSION": {
                                "VALUE": "HPD0"
                            },
                            "LABEL": {
                                "VALUE": "Port 1I Box 1 Bay 2"
                            },
                            "LOCATION": {
                                "VALUE": "Port 1I Box 1 Bay 2"
                            },
                            "MODEL": {
                                "VALUE": "EG0300FCSPH"
                            },
                            "SERIAL_NUMBER": {
                                "VALUE": "64R0A109FTM91426"
                            },
                            "STATUS": {
                                "VALUE": "OK"
                            }
                        }
                    ],
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                "MODEL": {
                    "VALUE": "HP Smart Array P830i Controller"
                },
                "SERIAL_NUMBER": {
                    "VALUE": "001438031389320"
                },
                "STATUS": {
                    "VALUE": "OK"
                }
            },
            "DISCOVERY_STATUS": {
                "STATUS": {
                    "VALUE": "Discovery Complete"
                }
            }
        },
        "TEMPERATURE": {
            "TEMP": [
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "42"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "46"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "27"
                    },
                    "LABEL": {
                        "VALUE": "01-Inlet Ambient"
                    },
                    "LOCATION": {
                        "VALUE": "Ambient"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "70"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "40"
                    },
                    "LABEL": {
                        "VALUE": "02-CPU 1"
                    },
                    "LOCATION": {
                        "VALUE": "CPU"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "70"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "40"
                    },
                    "LABEL": {
                        "VALUE": "03-CPU 2"
                    },
                    "LOCATION": {
                        "VALUE": "CPU"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "04-CPU 3"
                    },
                    "LOCATION": {
                        "VALUE": "CPU"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "05-CPU 4"
                    },
                    "LOCATION": {
                        "VALUE": "CPU"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "87"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "34"
                    },
                    "LABEL": {
                        "VALUE": "06-P1 DIMM 1-24"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "87"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "34"
                    },
                    "LABEL": {
                        "VALUE": "07-P2 DIMM 25-48"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "08-P3 DIMM 49-72"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "09-P4 DIMM 73-96"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "95"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "51"
                    },
                    "LABEL": {
                        "VALUE": "10-P1 Mem Buff"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "95"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "51"
                    },
                    "LABEL": {
                        "VALUE": "11-P2 Mem Buff"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "12-P3 Mem Buff"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "13-P4 Mem Buff"
                    },
                    "LOCATION": {
                        "VALUE": "Memory"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "60"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "35"
                    },
                    "LABEL": {
                        "VALUE": "14-HD Max"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "105"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "68"
                    },
                    "LABEL": {
                        "VALUE": "15-Chipset"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "33"
                    },
                    "LABEL": {
                        "VALUE": "16-P/S 1"
                    },
                    "LOCATION": {
                        "VALUE": "Power Supply"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "31"
                    },
                    "LABEL": {
                        "VALUE": "17-P/S 2"
                    },
                    "LOCATION": {
                        "VALUE": "Power Supply"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "18-P/S 3"
                    },
                    "LOCATION": {
                        "VALUE": "Power Supply"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "19-P/S 4"
                    },
                    "LOCATION": {
                        "VALUE": "Power Supply"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "70"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "75"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "30"
                    },
                    "LABEL": {
                        "VALUE": "20-P/S Zone"
                    },
                    "LOCATION": {
                        "VALUE": "Power Supply"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "115"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "120"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "46"
                    },
                    "LABEL": {
                        "VALUE": "21-VR P1"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "115"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "120"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "45"
                    },
                    "LABEL": {
                        "VALUE": "22-VR P2"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "23-VR P3"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "24-VR P4"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "90"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "41"
                    },
                    "LABEL": {
                        "VALUE": "25-VR P1 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "90"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "40"
                    },
                    "LABEL": {
                        "VALUE": "26-VR P2 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "90"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "36"
                    },
                    "LABEL": {
                        "VALUE": "27-VR P3 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "90"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "30"
                    },
                    "LABEL": {
                        "VALUE": "28-VR P4 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "29-VR P1 Mem"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "30-VR P2 Mem"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "31-VR P3 Mem"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "32-VR P4 Mem"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "65"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "29"
                    },
                    "LABEL": {
                        "VALUE": "33-SuperCAP Max"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "100"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "82"
                    },
                    "LABEL": {
                        "VALUE": "34-HD Controller"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "35-PCI 1"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "36-PCI 2"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "37-PCI 3"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "38-PCI 4"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "39-PCI 5"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "40-PCI 6"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "41-PCI 7"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "42-PCI 8"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "43-PCI 9"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "40"
                    },
                    "LABEL": {
                        "VALUE": "44-PCI 1 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "43"
                    },
                    "LABEL": {
                        "VALUE": "45-PCI 2 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "43"
                    },
                    "LABEL": {
                        "VALUE": "46-PCI 3 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "42"
                    },
                    "LABEL": {
                        "VALUE": "47-PCI 4 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "41"
                    },
                    "LABEL": {
                        "VALUE": "48-PCI 5 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "41"
                    },
                    "LABEL": {
                        "VALUE": "49-PCI 6 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "41"
                    },
                    "LABEL": {
                        "VALUE": "50-PCI 7 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "43"
                    },
                    "LABEL": {
                        "VALUE": "51-PCI 8 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "43"
                    },
                    "LABEL": {
                        "VALUE": "52-PCI 9 Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "VALUE": "N/A"
                    },
                    "CRITICAL": {
                        "VALUE": "N/A"
                    },
                    "CURRENTREADING": {
                        "VALUE": "N/A"
                    },
                    "LABEL": {
                        "VALUE": "53-LOM Card"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "Not Installed"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "43"
                    },
                    "LABEL": {
                        "VALUE": "54-I/O Zone"
                    },
                    "LOCATION": {
                        "VALUE": "I/O Board"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                },
                {
                    "CAUTION": {
                        "UNIT": "Celsius",
                        "VALUE": "80"
                    },
                    "CRITICAL": {
                        "UNIT": "Celsius",
                        "VALUE": "85"
                    },
                    "CURRENTREADING": {
                        "UNIT": "Celsius",
                        "VALUE": "49"
                    },
                    "LABEL": {
                        "VALUE": "55-SPI Board"
                    },
                    "LOCATION": {
                        "VALUE": "System"
                    },
                    "STATUS": {
                        "VALUE": "OK"
                    }
                }
            ]
        },
        "VRM": {}
    },
    "RESPONSE": {
        "MESSAGE": "No error",
        "STATUS": "0x0000"
    },
    "VERSION": "2.23"
}
'''

FIRMWARE_EMBEDDED_HEALTH_OUTPUT = '''
{
    "iLO": "2.02 Sep 05 2014",
    "Power Management Controller FW Bootloader": "2.7",
    "SAS Programmable Logic Device": "Version 0x04",
    "HP ProLiant System ROM": "11/26/2014",
    "HP Smart Array P830i Controller": "1.62",
    "Server Platform Services (SPS) Firmware": "2.3.0.FA.0",
    "HP ProLiant System ROM - Backup": "11/26/2014",
    "System Programmable Logic Device": "Version 0x0B",
    "Power Management Controller Firmware": "4.1"
}
'''
