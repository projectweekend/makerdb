from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException, ItemNotFound
from app.utils.data import dynamodb_connection


class DuplicateUserError(Exception):
    pass


class UserManager(object):

    def __init__(self):
        self.table = Table('makerdb_users', connection=dynamodb_connection)

    def create(self, user):  # pragma: no cover
        try:
            self.table.put_item(data=user)
        except ConditionalCheckFailedException:
            raise DuplicateUserError

    def read(self, email):  # pragma: no cover
        try:
            result = self.table.get_item(email=email)
        except ItemNotFound:
            return None
        return dict(result.items())


class UserManagerMixin(object):

    def __init__(self):
        super(UserManagerMixin, self).__init__()
        self.user_manager = UserManager()
