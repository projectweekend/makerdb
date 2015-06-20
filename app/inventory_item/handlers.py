import falcon
from app.utils.hooks import auth_required
from app.inventory_item.validation import InventoryItemCreateMixin
from app.inventory_item.data import DataMixin, DuplicateUserItemError


@falcon.before(auth_required)
class InventoryItemCollection(DataMixin, InventoryItemCreateMixin):

    def __init__(self):
        super(InventoryItemCollection, self).__init__()

    def on_post(self, req, res):
        res.status = falcon.HTTP_201

    def on_get(self, req, res):
        pass
