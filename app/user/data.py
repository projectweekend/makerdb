from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException, ItemNotFound


class DuplicateUserError(Exception):
    pass


class DataMixin(object):

    def __init__(self):
        self._users = Table('makerdb_users')

    def add_user(self, user):  # pragma: no cover
        try:
            self._users.put_item(data=user)
        except ConditionalCheckFailedException:
            raise DuplicateUserError

    def find_user(self, email):  # pragma: no cover
        try:
            result = self._users.get_item(email=email)
        except ItemNotFound:
            return None
        return dict(result.items())
