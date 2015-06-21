import json

from urlparse import urlparse
from falcon.testing import TestBase
from app import api
from app.config import DATABASE_URL
from app.utils.database import database_connection


db = database_connection()


HEADERS = {'Content-Type': 'application/json'}
USER_RESOURCE_ROUTE = '/v1/user'


class APITestCase(TestBase):

    def setUp(self):
        super(APITestCase, self).setUp()
        self.db = db
        self._empty_tables()

    def _empty_tables(self):
        parsed = urlparse(DATABASE_URL)

        app_tables_query = """
        SELECT          table_name
        FROM            information_schema.tables
        WHERE           table_schema = 'public' AND
                        table_catalog = '{0}' AND
                        table_name != 'schema_version';""".format(parsed.path.strip('/'))
        cursor = self.db.cursor()
        cursor.execute(app_tables_query)
        tables = [r[0] for r in cursor.fetchall()]
        for t in tables:
            query = 'TRUNCATE TABLE {0} CASCADE;'.format(t)
            cursor.execute(query)
            self.db.commit()
        cursor.close()

    def _simulate_request(self, method, path, data, token=None, **kwargs):
        if token:
            HEADERS['Authorization'] = token
        else:
            HEADERS.pop('Authorization', None)

        self.api = api

        result = self.simulate_request(
            path=path,
            method=method,
            headers=HEADERS,
            body=json.dumps(data),
            **kwargs)
        try:
            return json.loads(result[0])
        except IndexError:
            return None

    def simulate_get(self, path, token=None, **kwargs):
        return self._simulate_request(
            method='GET',
            path=path,
            data=None,
            token=token,
            **kwargs)

    def simulate_post(self, path, data, token=None, **kwargs):
        return self._simulate_request(
            method='POST',
            path=path,
            data=data,
            token=token,
            **kwargs)

    def simulate_put(self, path, data, token=None, **kwargs):
        return self._simulate_request(
            method='PUT',
            path=path,
            data=data,
            token=token,
            **kwargs)

    def simulate_patch(self, path, data, token=None, **kwargs):
        return self._simulate_request(
            method='PATCH',
            path=path,
            data=data,
            token=token,
            **kwargs)

    def simulate_delete(self, path, token=None, **kwargs):
        return self._simulate_request(
            method='DELETE',
            path=path,
            data=None,
            token=token,
            **kwargs)


class AuthenticatedAPITestCase(APITestCase):

    def setUp(self):
        super(AuthenticatedAPITestCase, self).setUp()
        body = self.simulate_post(USER_RESOURCE_ROUTE, {'email': 'test@test.com', 'password': '12345678'})
        self.auth_token = body['token']
