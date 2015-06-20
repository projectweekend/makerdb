import falcon
from app.utils.hooks import auth_required
from app.inventory_item.validation import InventoryItemCreateMixin
from app.inventory_item.data import DataMixin, DuplicateUserInventoryItemError


@falcon.before(auth_required)
class InventoryItemCollection(DataMixin, InventoryItemCreateMixin):

    def __init__(self):
        super(InventoryItemCollection, self).__init__()

    def on_post(self, req, res):
        user_email = req.context['auth_user']['email']
        try:
            req.context['result'] = self.add_user_inventory_item(user_email, req.context['data'])
        except DuplicateUserInventoryItemError:
            title = 'Conflict'
            description = 'Inventory item with name exists'
            raise falcon.HTTPConflict(title=title, description=description)

        res.status = falcon.HTTP_201

    def on_get(self, req, res):
        user_email = req.context['auth_user']['email']
        req.context['result'] = self.list_user_inventory_items(user_email)
        res.status = falcon.HTTP_200
