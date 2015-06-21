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


class InventoryItemCollectionTestCase(AuthenticatedAPITestCase):

    def test_create_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_RESOURCE_ROUTE, VALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)
        self.assertEqual(body['name'], VALID_DATA['name'])
        self.assertEqual(body['url'], VALID_DATA['url'])
        self.assertEqual(body['image_url'], VALID_DATA['image_url'])
        self.assertEqual(body['quantity'], VALID_DATA['quantity'])
        self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
        self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
        self.assertIn('id', body.keys())
        self.assertIn('user_id', body.keys())

    def test_create_inventory_item_invalid(self):
        body = self.simulate_post(INVENTORY_ITEM_RESOURCE_ROUTE, INVALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        error_keys = body['description'].keys()
        self.assertIn('name', error_keys)
        self.assertIn('url', error_keys)
        self.assertIn('image_url', error_keys)
        self.assertIn('quantity', error_keys)
        self.assertIn('vendor_name', error_keys)
        self.assertIn('vendor_item_id', error_keys)

    def test_list_inventory_items(self):
        self.simulate_post(INVENTORY_ITEM_RESOURCE_ROUTE, VALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        body = self.simulate_get(INVENTORY_ITEM_RESOURCE_ROUTE, query_string='skip=0&take=5', token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertEqual(body['count'], 1)
        self.assertEqual(len(body['items']), 1)
        self.assertEqual(body['items'][0]['name'], VALID_DATA['name'])
        self.assertEqual(body['items'][0]['url'], VALID_DATA['url'])
        self.assertEqual(body['items'][0]['image_url'], VALID_DATA['image_url'])
        self.assertEqual(body['items'][0]['quantity'], VALID_DATA['quantity'])
        self.assertEqual(body['items'][0]['vendor_name'], VALID_DATA['vendor_name'])
        self.assertEqual(body['items'][0]['vendor_item_id'], VALID_DATA['vendor_item_id'])
        self.assertIn('id', body['items'][0].keys())
        self.assertIn('user_id', body['items'][0].keys())

    def test_list_inventory_items_no_skip_take(self):
        self.simulate_get(INVENTORY_ITEM_RESOURCE_ROUTE, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)


class InventoryItemDetailTestCase(AuthenticatedAPITestCase):

    def test_get_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_RESOURCE_ROUTE, VALID_DATA, token=self.auth_token)
        detail_route = '{0}/{1}'.format(INVENTORY_ITEM_RESOURCE_ROUTE, body['id'])

        body = self.simulate_get(detail_route, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertEqual(body['name'], VALID_DATA['name'])
        self.assertEqual(body['url'], VALID_DATA['url'])
        self.assertEqual(body['image_url'], VALID_DATA['image_url'])
        self.assertEqual(body['quantity'], VALID_DATA['quantity'])
        self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
        self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
        self.assertIn('id', body.keys())
        self.assertIn('user_id', body.keys())
