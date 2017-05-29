from sushy import exceptions
from sushy.resources.manager.manager import Manager

class HPEManager(Manager):
    """Class that extends the functionality of Manager resource class

    This class extends the functionality of Manager resource class
    from sushy
    """
    def set_license(self, lic_uri, lic_key):
        """Set the license on a redfish system

        :param lic_uri: path of license uri
        :param lic_key: license key in dictionary format.
        :returns: response object of the post operation
        """
        if lic_uri is not None:
            return self._conn.post(lic_uri, data=lic_key)
