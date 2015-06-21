import falcon
from app.utils.hooks import auth_required
from app.inventory_item.validation import InventoryItemValidationMixin
from app.inventory_item.data import DataManagerMixin


@falcon.before(auth_required)
class InventoryItemCollectionResource(InventoryItemValidationMixin, DataManagerMixin):

    def on_post(self, req, res):
        item_doc = req.context['data']
        item_doc['user_id'] = req.context['auth_user']['id']
        req.context['result'] = self.add_item(item_doc)
        res.status = falcon.HTTP_CREATED

    def on_get(self, req, res):
        params = {
            'skip': req.get_param_as_int('skip', required=True),
            'take': req.get_param_as_int('take', required=True),
            'user_id': req.context['auth_user']['id']
        }
        req.context['result'] = self.list_items(params)
        res.status = falcon.HTTP_OK


@falcon.before(auth_required)
class InventoryItemDetailResource(InventoryItemValidationMixin, DataManagerMixin):

    def on_get(self, req, res, item_id):
        params = {
            'id': item_id,
            'user_id': req.context['auth_user']['id']
        }
        req.context['result'] = self.get_item(params)
        if not req.context['result']:
            raise falcon.HTTPNotFound
        res.status = falcon.HTTP_OK

    def on_put(self, req, res, item_id):
        item_doc = req.context['data']
        item_doc['id'] = item_id
        item_doc['user_id'] = req.context['auth_user']['id']
        req.context['result'] = self.update_item(item_doc)
        if not req.context['result']:
            raise falcon.HTTPNotFound
        res.status = falcon.HTTP_OK

    def on_delete(self, req, res, item_id):
        params = {
            'id': item_id,
            'user_id': req.context['auth_user']['id']
        }
        req.context['result'] = self.delete_item(params)
        if not req.context['result']:
            raise falcon.HTTPNotFound
        res.status = falcon.HTTP_NO_CONTENT
