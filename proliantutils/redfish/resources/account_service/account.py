from sushy.resources import base


def get_member_uri(username, members):
    """Returns the uri of account to be updated

    :param username: username of account
    :param members: collection of accounts

    :returns account uri
    """
    for member in members:
        if member.username == username:
            return member.mem_uri


class HPEAccount(base.ResourceBase):

    username = base.Field('UserName')

    mem_uri = base.Field('@odata.id')


class HPEAccountCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return HPEAccount
