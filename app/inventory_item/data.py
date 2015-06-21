import json


class DataManagerMixin(object):

    def add_item(self, item_doc):
        self.cursor.callproc('sp_inventory_items_insert', [json.dumps(item_doc), ])
        result = self.cursor.fetchone()
        return result[0]

    def list_items(self, params):
        self.cursor.callproc('sp_inventory_items_list', [json.dumps(params), ])
        result = self.cursor.fetchone()
        return {
            'count': result[0],
            'items': result[1] if result[1] else []
        }

    def get_item(self, params):
        self.cursor.callproc('sp_inventory_items_select', [json.dumps(params), ])
        result = self.cursor.fetchone()
        return result[0] if result else None
