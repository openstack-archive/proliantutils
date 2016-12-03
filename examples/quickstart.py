import logging
import sys

# If you want it to get executed through the local copy of the repo,
# then provide the local repo path of ``proliantutils`` here,
# e.g. '/opt/stack/proliantutils'.
# Or comment out this line to have the quickstart example running from the
# pip installed variant
sys.path.insert(1, '/opt/stack/proliantutils')


from proliantutils.ilo import client
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.ilo import ris_v2
from proliantutils.ilo import redfish
from proliantutils import log


stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter(
    '%(asctime)s <%(levelname)-4s> [%(name)-15s] %(message)s '
    '[%(pathname)s:%(lineno)s - %(funcName)10s]',

    '%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(stream_formatter)

base_logger = log.get_logger(None)
base_logger.setLevel(logging.DEBUG)
base_logger.addHandler(stream_handler)

# iLO address, iLO account name and password
iLO_host_ip = '10.10.1.86'
login_account = 'Administrator'
login_password = '12iso*help'

# c = client.IloClient(iLO_host_ip, login_account, login_password)
# c = ribcl.IloClient(iLO_host_ip, login_account, login_password)
# c = ris.RISOperations(iLO_host_ip, login_account, login_password)

# c = ris_v2.RISOperations(iLO_host_ip, login_account, login_password)
c = redfish.RedfishOperations(iLO_host_ip, login_account, login_password)

# c.<operation>
# print c.get_all_licenses() - NA in REST based Operations
# print c.get_product_name()
# print c.get_vm_status()
# print c.get_vm_status('CDROM')
print c.get_host_power_status()
