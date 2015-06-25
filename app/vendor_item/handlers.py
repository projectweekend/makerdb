from boto.dynamodb2.table import Table
import falcon
from app.config import VENDOR_NAMES_MAP
from app.utils.hooks import auth_required
from app.inventory_item.data import DataManagerMixin
from app.vendor_item.validation import VendorItemValidationMixin


VENDOR_ITEMS = Table('makerdb_vendor_items')


@falcon.before(auth_required)
class VendorItemResource(VendorItemValidationMixin, DataManagerMixin):

    def on_post(self, req, res):
        vendor_name = req.context['data']['vendor_name']
        vendor_item_id = req.context['data']['vendor_item_id']
        quantity = req.context['data']['quantity']
        try:
            vendor_name = VENDOR_NAMES_MAP[vendor_name]
        except KeyError:
            raise falcon.HTTPNotFound

        results = VENDOR_ITEMS.query_2(
            vendor_name__eq=vendor_name,
            vendor_item_id__eq=vendor_item_id)

        results = [dict(r.items()) for r in results]
        if not results:
            raise falcon.HTTPNotFound

        vendor_item = results.pop()

        item_doc = {
            'user_id': req.context['auth_user']['id'],
            'name': vendor_item['item_name'],
            'url': vendor_item['item_url'],
            'image_url': vendor_item['item_image_url'],
            'quantity': quantity,
            'vendor_name': vendor_item['vendor_name'],
            'vendor_item_id': vendor_item['vendor_item_id']
        }

        req.context['result'] = self.add_item(item_doc)
        res.status = falcon.HTTP_OK
