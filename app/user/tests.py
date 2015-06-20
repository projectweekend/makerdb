import falcon
from app import api
from app.utils.testing import APITestCase
from app.user import handlers as user_handlers


USER_RESOURCE_ROUTE = '/v1/user'
USER_AUTH_ROUTE = '/v1/authenticate'
PASSWORD_RESET_REQUEST_ROUTE = '/v1/password-reset/request'
PASSWORD_RESET_CONFIRM_ROUTE = '/v1/password-reset/confirm'
AUTH_TEST_ROUTE = '/v1/test/auth'

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

    def test_create_a_user(self):
        body = self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)
        self.assertNotEqual(len(body['token']), 0)

    def test_create_a_dup_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CONFLICT)

    def test_invalid_create_a_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)


class AuthenticationResourceTestCase(APITestCase):

    def test_successful_auth(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        body = self.simulate_post(USER_AUTH_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertNotEqual(len(body['token']), 0)

    def test_invalid_auth_request(self):
        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['MISSING_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['MISSING_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

    def test_failed_auth(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['BAD_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['NOT_REGISTERED'])
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)
