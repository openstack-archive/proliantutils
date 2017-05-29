from sushy import exceptions
from sushy.resources.manager.manager import Manager

class HPEManager(Manager):

    def set_license(self, lic_uri, lic_key):
        if lic_uri is not None:
            return self._conn.post(lic_uri, data=lic_key)
