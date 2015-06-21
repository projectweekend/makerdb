import falcon
from app.utils.hooks import auth_required
# from psycopg2 import IntegrityError
from app.inventory_item.validation import InventoryItemValidationMixin
from app.inventory_item.data import DataManagerMixin


class InventoryItemCollectionResource(InventoryItemValidationMixin, DataManagerMixin):

    @falcon.before(auth_required)
    def on_post(self, req, res):
        item_doc = req.context['data']
        item_doc['user_id'] = req.context['auth_user']['id']
        req.context['result'] = self.add_item(item_doc)
        res.status = falcon.HTTP_CREATED

    def on_get(self, req, res):
        pass


class InventoryItemDetailResource(object):

    def on_get(self, req, res):
        pass

    def on_put(self, req, res):
        pass

    def on_delete(self, req, res):
        pass
