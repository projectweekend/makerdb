# import falcon
# from app.utils.testing import AuthenticatedAPITestCase


# INVENTORY_ITEM_ROUTE = '/v1/inventory-item'

# VALID_DATA = {
#     'name': 'Super Cool Thing',
#     'url': '',
#     'image_url': '',
#     'quantity': 1,
#     'vendor_item_id': '',
#     'vendor_name': '',
#     'vendor_site': ''
# }

# INVALID_DATA = {
#     'name': '',
#     'url': 'not url',
#     'image_url': 'not url',
#     'quantity': 'not int',
#     'vendor_item_id': 123,
#     'vendor_name': 1234,
#     'vendor_site': 'not url'
# }


# class ItemInventoryTestCase(AuthenticatedAPITestCase):

#     def test_create_inventory_item(self):
#         body = self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_201)
#         self.assertIn('id', body.keys())
#         self.assertEqual(body['name'], VALID_DATA['name'])
#         self.assertEqual(body['url'], VALID_DATA['url'])
#         self.assertEqual(body['image_url'], VALID_DATA['image_url'])
#         self.assertEqual(body['quantity'], VALID_DATA['quantity'])
#         self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
#         self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
#         self.assertEqual(body['vendor_site'], VALID_DATA['vendor_site'])

#     def test_create_dup_inventory_item(self):
#         self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_201)

#         self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_409)

#     def test_invalid_create_inventory_item(self):
#         body = self.simulate_post(INVENTORY_ITEM_ROUTE, INVALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_400)
#         error_keys = body['description'].keys()
#         self.assertIn('name', error_keys)
#         self.assertIn('url', error_keys)
#         self.assertIn('image_url', error_keys)
#         self.assertIn('quantity', error_keys)
#         self.assertIn('vendor_item_id', error_keys)
#         self.assertIn('vendor_name', error_keys)
#         self.assertIn('vendor_site', error_keys)

#     def test_list_inventory_items(self):
#         self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_201)

#         body = self.simulate_get(INVENTORY_ITEM_ROUTE, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_200)
#         self.assertEqual(len(body), 1)
#         self.assertIn('id', body[0].keys())
#         self.assertEqual(body[0]['name'], VALID_DATA['name'])
#         self.assertEqual(body[0]['url'], VALID_DATA['url'])
#         self.assertEqual(body[0]['image_url'], VALID_DATA['image_url'])
#         self.assertEqual(body[0]['quantity'], VALID_DATA['quantity'])
#         self.assertEqual(body[0]['vendor_item_id'], VALID_DATA['vendor_item_id'])
#         self.assertEqual(body[0]['vendor_name'], VALID_DATA['vendor_name'])
#         self.assertEqual(body[0]['vendor_site'], VALID_DATA['vendor_site'])

#     def test_get_inventory_item(self):
#         body = self.simulate_post(INVENTORY_ITEM_ROUTE, VALID_DATA, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_201)

#         route = '{0}/{1}'.format(INVENTORY_ITEM_ROUTE, body['id'])
#         body = self.simulate_get(route, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_200)
#         self.assertIn('id', body.keys())
#         self.assertEqual(body['name'], VALID_DATA['name'])
#         self.assertEqual(body['url'], VALID_DATA['url'])
#         self.assertEqual(body['image_url'], VALID_DATA['image_url'])
#         self.assertEqual(body['quantity'], VALID_DATA['quantity'])
#         self.assertEqual(body['vendor_item_id'], VALID_DATA['vendor_item_id'])
#         self.assertEqual(body['vendor_name'], VALID_DATA['vendor_name'])
#         self.assertEqual(body['vendor_site'], VALID_DATA['vendor_site'])

#     def test_get_inventory_item_not_exists(self):
#         route = '{0}/{1}'.format(INVENTORY_ITEM_ROUTE, 'whatever')
#         self.simulate_get(route, token=self.auth_token)
#         self.assertEqual(self.srmock.status, falcon.HTTP_404)
