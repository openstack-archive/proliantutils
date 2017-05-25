from sushy.resources import base

SECURE_BOOT_CURRENT_BOOT_MAP = {"Enabled" : True,
                                "Disabled" : False}

SECURE_BOOT_ENABLE_MAP = {"true" : True,
                          "false": False}

SECURE_BOOT_CURRENT_BOOT_REV_MAP = { v:k for (k,v) in SECURE_BOOT_CURRENT_BOOT_MAP.items()}

SECURE_BOOT_ENABLE_REV_MAP = { v:k for (k,v) in SECURE_BOOT_ENABLE_MAP.items()}


class SecureBootResource(base.ResourceBase):

    #_secure_boot = SecureBoot("SecureBoot", required=True)
    secure_boot_current = base.Field("SecureBootCurrentBoot",
                                     adapter=SECURE_BOOT_CURRENT_BOOT_MAP.get)
    secure_boot_enable = base.Field("SecureBootEnable",
                                    adapter=SECURE_BOOT_ENABLE_MAP.get)
    
    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a SecureBootResource

        :param connector: A Connector instance
        :param identity: The identity of the SecureBootResource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(SecureBootResource, self).__init__(connector, identity, redfish_version)
        
