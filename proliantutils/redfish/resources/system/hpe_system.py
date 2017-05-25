from sushy import exceptions
from sushy.resources.system.system import System
from proliantutils.redfish.resources.system.secure_boot import SecureBootResource

class HPESystem(System):

    def _get_resource_path(self, resource_name):
        """Helper function to find the resource path"""
        resource_path = self.json.get(resource_name)
        if not resource_path:
            raise exceptions.MissingAttributeError(attribute=resource_name,
                                                   resource=self._path)
        return resource_path.get('@odata.id')

    @property
    def secure_boot_resource(self):
        secure_boot_resource = SecureBootResource(
            self._conn, self._get_resource_path('SecureBoot'),
            redfish_version=self.redfish_version)
        return secure_boot_resource

    def secure_boot_config(self, data):
        if data is not None:
            target_uri = self._get_resource_path('SecureBoot')
            self._conn.post(target_uri, data=data)
        
