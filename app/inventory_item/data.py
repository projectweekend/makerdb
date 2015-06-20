from uuid import uuid4
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException, ItemNotFound


class DataMixin(object):

    def __init__(self):
        self._user_items = Table('makerdb_user_items')

    def add_user_inventory_item(self, user_email, user_item):  # pragma: no cover
        user_item['user_email'] = user_email
        user_item['id'] = str(uuid4())
        self._user_items.put_item(data=user_item)
        return user_item

    def find_user_inventory_item(self, user_email, user_item_id):  # pragma: no cover
        try:
            result = self._user_items.get_item(user_email=user_email, id=user_item_id)
        except ItemNotFound:
            return None
        return dict(result.items())
