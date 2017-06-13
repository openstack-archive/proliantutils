import sys

import mock
from oslo_utils import importutils
import six


SUSHY_MANAGER_SPEC = (
    'main',
    'manager',
    'resources',
    )

sushy = importutils.try_import('sushy')
if not sushy:
    import pdb
    pdb.set_trace()
    sushy = mock.MagicMock(spec_set=SUSHY_MANAGER_SPEC)
    sys.modules['sushy'] = sushy
    sys.modules['sushy.main'] = sushy.main
    sys.modules['sushy.resources'] = sushy.resources
    sys.modules['sushy.resources.manager'] = sushy.resources.manager
    sys.modules['sushy.resources.manager.manager'] = sushy.resources.manager.manager
    if 'proliantutils.redfish.resources.manager' in sys.modules:
        six.moves.reload_module(sys.modules['proliantutils.redfish.resources.manager'])
