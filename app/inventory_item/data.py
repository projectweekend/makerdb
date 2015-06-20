from uuid import uuid4
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException


class DuplicateUserInventoryItemError(Exception):
    pass


class DataMixin(object):

    def __init__(self):
        self._user_items = Table('makerdb_user_items')

    def add_user_inventory_item(self, user_email, user_item):  # pragma: no cover
        user_item['user_email'] = user_email
        user_item['id'] = str(uuid4())
        try:
            self._user_items.put_item(data=user_item)
        except ConditionalCheckFailedException:
            raise DuplicateUserInventoryItemError
        return user_item

    def list_user_inventory_items(self, user_email):  # pragma: no cover
        results = self._user_items.query_2(user_email__eq=user_email)
        return [dict(r.items()) for r in results]

    def find_user_inventory_item(self, user_email, user_item_id):  # pragma: no cover
        results = self._user_items.query_2(
            user_email__eq=user_email,
            query_filter={
                'id__eq': user_item_id
            })

        results = [dict(r.items()) for r in results]

        try:
            item = results.pop()
        except IndexError:
            return False

        return item

    def update_user_inventory_item(self, user_email, user_item_id, new_values):
        results = self._user_items.query_2(
            user_email__eq=user_email,
            query_filter={
                'id__eq': user_item_id
            })

        results = [r for r in results]

        try:
            item = results.pop()
        except IndexError:
            return False

        item.update(new_values)
        item.save()

        return True

    def delete_user_inventory_item(self, user_email, user_item_id):
        results = self._user_items.query_2(
            user_email__eq=user_email,
            query_filter={
                'id__eq': user_item_id
            })

        results = [r for r in results]

        try:
            item = results.pop()
        except IndexError:
            return False

        item.delete()

        return True
