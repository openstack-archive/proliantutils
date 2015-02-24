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
