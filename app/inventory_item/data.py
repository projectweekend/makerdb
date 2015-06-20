from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException, ItemNotFound


class DuplicateUserItemError(Exception):
    pass


class DataMixin(object):

    def __init__(self):
        self._user_items = Table('makerdb_user_items')

    def add_user_item(self, user_item):
        try:
            self._user_items.put_item(data=user_item)
        except ConditionalCheckFailedException:
            raise DuplicateUserItemError

    def find_user_item(self, user_item_id):
        try:
            result = self._user_items.get_item(id=user_item_id)
        except ItemNotFound:
            return None
        return dict(result.items())
