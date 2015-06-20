import falcon
from mock import patch
from app.utils.testing import AuthenticatedAPITestCase
from app.utils.mocks import (
    mock_add_user_inventory_item, mock_find_user_inventory_item
)


INVENTORY_ITEM_ROUTE = '/v1/inventory-item'

VALID_DATA = {
    'name': 'Super Cool Thing',
    'url': '',
    'image_url': '',
    'quantity': 1,
    'vendor_item_id': '',
    'vendor_name': '',
    'vendor_site': ''
}

INVALID_DATA = {
    'name': '',
    'url': 'not url',
    'image_url': 'not url',
    'quantity': 'not int',
    'vendor_item_id': 123,
    'vendor_name': 1234,
    'vendor_site': 'not url'
}


class ItemInventoryTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(ItemInventoryTestCase, self).setUp()

    @patch('app.inventory_item.handlers.DataMixin.add_user_inventory_item', side_effect=mock_add_user_inventory_item)
    def test_create_inventory_item(self, add_user_inventory_item):
        body = self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertIn('id', body.keys())
        self.assertEqual(body['name'], VALID_DATA['name'])
        self.assertEqual(body['url'], VALID_DATA['url'])
        self.assertEqual(body['image_url'], VALID_DATA['image_url'])
        self.assertEqual(body['quantity'], VALID_DATA['quantity'])
        self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
        self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
        self.assertEqual(body['vendor_site'], VALID_DATA['vendor_site'])
        self.assertEqual(add_user_inventory_item.call_count, 1)

    def test_invalid_create_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_ROUTE, INVALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        error_keys = body['description'].keys()
        self.assertIn('name', error_keys)
        self.assertIn('url', error_keys)
        self.assertIn('image_url', error_keys)
        self.assertIn('quantity', error_keys)
        self.assertIn('vendor_item_id', error_keys)
        self.assertIn('vendor_name', error_keys)
        self.assertIn('vendor_site', error_keys)
