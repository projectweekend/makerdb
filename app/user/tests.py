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


class PasswordResetRequestResourceTestCase(APITestCase):

    def test_password_reset_request_with_matching_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(id) FROM app_password_reset')
        result = cursor.fetchone()
        self.assertEqual(int(result[0]), 1)
        cursor.close()

    def test_password_reset_request_with_no_matching_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': INVALID_DATA['NOT_REGISTERED']['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

    def test_password_reset_request_with_invalid_data(self):
        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': INVALID_DATA['BAD_EMAIL']['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)


class PasswordResetConfirmResourceTestCase(APITestCase):

    def test_password_reset_confirm_with_matching_code(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        cursor = self.db.cursor()
        cursor.execute('SELECT code FROM app_password_reset')
        result = cursor.fetchone()
        cursor.close()

        request_data = {
            'code': result[0],
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)

        request_data = {
            'email': VALID_DATA['email'],
            'password': 'newpassword'
        }
        body = self.simulate_post(USER_AUTH_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertNotEqual(len(body['token']), 0)

    def test_password_reset_confirm_with_no_matching_code(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        request_data = {
            'code': 'does not exist',
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)

    def test_password_reset_confirm_with_invalid_data(self):
        missing_password = {
            'code': 'some-fake-code'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, missing_password)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)

        missing_code = {
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, missing_code)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)


class AuthTestResourceTestCase(APITestCase):

    def setUp(self):
        super(AuthTestResourceTestCase, self).setUp()
        self.api = api
        # Add route to test the AuthUser middleware
        self.api.add_route(AUTH_TEST_ROUTE, user_handlers.AuthTestResource())

    def test_auth_required_with_valid_token(self):
        body = self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        body = self.simulate_get(AUTH_TEST_ROUTE, body['token'])
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertEqual(body['email'], VALID_DATA['email'])

    def test_auth_required_with_invalid_token(self):
        self.simulate_get(AUTH_TEST_ROUTE, 'fake token')
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)

    def test_auth_required_with_no_token(self):
        self.simulate_get(AUTH_TEST_ROUTE)
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)
