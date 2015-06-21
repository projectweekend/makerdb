import falcon
from app.utils.testing import AuthenticatedAPITestCase


INVENTORY_ITEM_RESOURCE_ROUTE = '/v1/inventory-item'

VALID_DATA = {
    'name': 'Cool Item',
    'url': 'http://www.adafruit.com/products/2466',
    'image_url': 'http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif',
    'quantity': 1,
    'vendor_name': 'Adafruit',
    'vendor_item_id': '2466'
}

INVALID_DATA = {
    'name': '',
    'url': 'not url',
    'image_url': 'not url',
    'quantity': 'not int'
}


class InventoryItemResourceTestCase(AuthenticatedAPITestCase):

    def test_create_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_RESOURCE_ROUTE, VALID_DATA, token=self.auth_token)
        print(body)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)
        self.assertEqual(body['name'], VALID_DATA['name'])
        self.assertEqual(body['url'], VALID_DATA['url'])
        self.assertEqual(body['image_url'], VALID_DATA['image_url'])
        self.assertEqual(body['quantity'], VALID_DATA['quantity'])
        self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
        self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
        self.assertIn('id', body.keys())
        self.assertIn('user_id', body.keys())
