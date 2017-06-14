import mock
import testtools

from proliantutils.redfish.resources.account_service import account_service


class HPEAccountServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountServiceTestCase, self).setUp()
        self.conn = mock.MagicMock()

        self.acc_inst = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

    def test_update_credentials(self):
        member_uri = '/redfish/v1/AccountService/Accounts/1/'
        password = {'Password': 'fake-password'}
        self.acc_inst.update_credentials(member_uri, password)
        self.acc_inst._conn.patch.assert_called_once_with(
            member_uri, data={'Password': 'fake-password'})
