from sushy.main import Sushy
from proliantutils.redfish.resources.system.hpe_system import HPESystem
from proliantutils.redfish.resources.manager.hpe_manager import HPEManager

class HPESushy(Sushy):
    def get_system(self, identity):
        """Given the identity return a HPESystem object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return HPESystem(self._conn, identity,
                         redfish_version=self.redfish_version)

    def get_manager(self, identity):
        """Given the identity return a HPESystem object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return HPEManager(self._conn, identity,
                         redfish_version=self.redfish_version)
