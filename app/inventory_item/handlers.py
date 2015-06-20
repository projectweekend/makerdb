import falcon
from app.utils.hooks import auth_required
from app.inventory_item.validation import InventoryItemCreateMixin
from app.inventory_item.data import DataMixin


@falcon.before(auth_required)
class InventoryItemCollection(DataMixin, InventoryItemCreateMixin):

    def __init__(self):
        super(InventoryItemCollection, self).__init__()

    def on_post(self, req, res):
        user_email = req.context['auth_user']['email']
        req.context['result'] = self.add_user_inventory_item(user_email, req.context['data'])
        res.status = falcon.HTTP_201
