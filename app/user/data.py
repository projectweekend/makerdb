from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException


class DuplicateUserError(Exception):
    pass


class DataMixin(object):

    def __init__(self):
        self._dynamodb = Table('makerdb_users')

    def add_user(self, user):  # pragma: no cover
        try:
            self._dynamodb.put_item(data=user)
        except ConditionalCheckFailedException:
            raise DuplicateUserError
