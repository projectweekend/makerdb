import json
from time import time
import falcon
from mock import patch

from app.utils.testing import APITestCase
from app.utils.mocks import mock_add_user, mock_add_user_fail


USER_RESOURCE_ROUTE = '/v1/user'

VALID_DATA = {
    'email': 'abcd@efgh.com',
    'password': '12345678'
}

INVALID_DATA = {
    'MISSING_EMAIL': {
        'password': '12345678'
    },
    'BAD_EMAIL': {
        'email': 'not an email',
        'password': '12345678'
    },
    'MISSING_PASSWORD': {
        'email': 'abcd@efgh.com'
    },
    'BAD_PASSWORD': {
        'email': 'abcd@efgh.com',
        'password': 'short'
    },
    'NOT_REGISTERED': {
        'email': 'not@registered.com',
        'password': '11111111'
    }
}


class UserResourceTestCase(APITestCase):

    @patch('app.user.handlers.DataMixin.add_user', side_effect=mock_add_user)
    def test_create_a_user(self, add_user):
        body = self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertNotEqual(len(body['token']), 0)
        self.assertEqual(add_user.call_count, 1)

    @patch('app.user.handlers.DataMixin.add_user', side_effect=mock_add_user_fail)
    def test_create_a_dup_user(self, add_user):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_409)
        self.assertEqual(add_user.call_count, 1)

    def test_invalid_create_a_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
