import ris
import ribcl

class IloClient(object) :
    
    def __new__(self, host, login, password, timeout=60, port=443, bios_password=None ):
         
        client = ribcl.RIBCLOperations(host, login, password, timeout, port)
        model = client.get_product_name()
         
        if 'Gen9' in model:
            client = ris.RISOperations(host, login, password, bios_password)
        
        return client