from boto.dynamodb2.table import Table
import falcon
from app.utils.hooks import auth_required


VENDOR_ITEMS = Table('makerdb_vendor_items')


@falcon.before(auth_required)
class VendorItemCollectionResource(object):

    def on_get(self, req, res):
        vendor_name = req.get_param('vendor_name', required=True)
        results = VENDOR_ITEMS.query_2(vendor_name__eq=vendor_name)
        req.context['result'] = [dict(r.tiems()) for r in results]
        res.status = falcon.HTTP_OK


@falcon.before(auth_required)
class VendorItemDetailResource(object):

    def on_get(self, req, res, vendor_name, vendor_item_id):
        results = VENDOR_ITEMS.query_2(
            vendor_name__eq=vendor_name,
            vendor_item_id__eq=vendor_item_id)
        req.context['result'] = [dict(r.tiems()) for r in results]
        res.status = falcon.HTTP_OK
