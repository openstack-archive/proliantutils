import json

import mock
import testtools

from proliantutils.redfish.resources.account_service import account
from proliantutils.redfish.resources.account_service import account_service


class Memberdata(testtools.TestCase):

    def test_get_member_uri(self):
        self.conn = mock.Mock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        account_obj = account_service.HPEAccountService(
            self.conn, '/redfish/v1/AccountService',
            redfish_version='1.0.2')

        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            account_data_json = json.loads(f.read())

        self.conn.get.return_value.json.side_effect = [
            account_data_json['GET_ACCOUNT_INFO'],
            account_data_json['GET_ACCOUNT_DETAILS']]

        uri = account.get_member_uri('foo',
                                     account_obj.account.get_members())

        self.assertEqual('/redfish/v1/AccountService/Accounts/1/', uri)


class HPEAccountTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEAccountTestCase, self).setUp()
        self.conn = mock.MagicMock()
        with open('proliantutils/tests/redfish/'
                  'json_samples/account_data.json', 'r') as f:
            account_data_json = json.loads(f.read())

        self.conn.get.return_value.json.return_value = account_data_json[
            'GET_ACCOUNT_DETAILS']

        self.acc_inst = account.HPEAccount(
            self.conn, '/redfish/v1/AccountService/Accounts/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.acc_inst._parse_attributes()
        self.assertEqual('foo', self.acc_inst.username)
        self.assertEqual('/redfish/v1/AccountService/Accounts/1/',
                         self.acc_inst.mem_uri)
