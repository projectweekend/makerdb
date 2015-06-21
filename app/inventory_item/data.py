import json


class DataManagerMixin(object):

    def add_item(self, item_doc):
        self.cursor.callproc('sp_inventory_items_insert', [json.dumps(item_doc), ])
        result = self.cursor.fetchone()
        return result[0]
