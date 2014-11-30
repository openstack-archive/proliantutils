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
