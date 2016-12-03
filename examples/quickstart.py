import json
import logging
import sys

import six


# Loading the settings.json file params
with open('examples/settings.json', 'r') as f:
    settings = json.loads(f.read())

# ``path_to_local_repo``
# Either a boolean value(False only) or a path to the local proliantutils
# repo. If set to False the test driver will try importing proliantutils
# from the python distro installation, i.e. the pip installed variant;
# if it's a path the driver will use that specified path for proliantutils
# bundle for importing. Defaults to 'false'.
path_to_local_repo = settings.get('path_to_local_repo')
if isinstance(path_to_local_repo, six.string_types):
    sys.path.insert(1, path_to_local_repo)

# ``ilo_ip``, ``username``, ``password``
# IP address of the iLO along with its user account credentials with
# admin/server-profile access privilege.
ilo_ip = settings.get('ilo_ip')
username = settings.get('username')
password = settings.get('password')


from proliantutils import client
from proliantutils.ilo import ribcl
from proliantutils.ilo import ris
from proliantutils.redfish import redfish
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


if __name__ == '__main__':
    # c = client.IloClient(ilo_ip, username, password)
    # c = ribcl.IloClient(ilo_ip, username, password)
    # c = ris.RISOperations(ilo_ip, username, password)
    c = redfish.RedfishOperations(ilo_ip, username, password)

    # c.<operation>
#     c.insert_virtual_media('http://abc.com/foo.img')
#     c.insert_virtual_media('http://abc.com/bar.iso', device='CDROM')
#     c.eject_virtual_media()
#     c.eject_virtual_media('CDROM')
