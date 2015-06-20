import falcon
from mock import patch

from app.utils.testing import AuthenticatedAPITestCase


INVENTORY_ITEM_ROUTE = '/v1/inventory-item'

VALID_DATA = {
    'item_name': 'Super Cool Thing',
    'item_url': '',
    'item_image_url': '',
    'item_quantity': 1,
    'vendor_item_id': '',
    'vendor_name': '',
    'vendor_site': ''
}

INVALID_DATA = {
    'item_name': '',
    'item_url': 'not url',
    'item_image_url': 'not url',
    'item_quantity': 'not int',
    'vendor_item_id': 123,
    'vendor_name': 1234,
    'vendor_site': 'not url'
}


class ItemInventoryTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(ItemInventoryTestCase, self).setUp()

    def test_create_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

    def test_invalid_create_inventory_item(self):
        body = self.simulate_post(INVENTORY_ITEM_ROUTE, INVALID_DATA, token=self.auth_token)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        error_keys = body['description'].keys()
        self.assertIn('item_name', error_keys)
        self.assertIn('item_url', error_keys)
        self.assertIn('item_image_url', error_keys)
        self.assertIn('item_quantity', error_keys)
        self.assertIn('vendor_item_id', error_keys)
        self.assertIn('vendor_name', error_keys)
        self.assertIn('vendor_site', error_keys)
