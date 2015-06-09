import json

from falcon.testing import TestBase
from app import api


HEADERS = {'Content-Type': 'application/json'}


class APITestCase(TestBase):

    def setUp(self):
        super(APITestCase, self).setUp()

    def _simulate_request(self, method, path, data, token=None):
        if token:
            HEADERS['Authorization'] = token

        self.api = api

        result = self.simulate_request(
            path=path,
            method=method,
            headers=HEADERS,
            body=json.dumps(data))
        return json.loads(result[0])

    def simulate_get(self, path, token=None):
        return self._simulate_request(
            method='GET',
            path=path,
            data=None,
            token=token)

    def simulate_post(self, path, data, token=None):
        return self._simulate_request(
            method='POST',
            path=path,
            data=data,
            token=token)

    def simulate_put(self, path, data, token=None):
        return self._simulate_request(
            method='PUT',
            path=path,
            data=data,
            token=token)

    def simulate_patch(self, path, data, token=None):
        return self._simulate_request(
            method='PATCH',
            path=path,
            data=data,
            token=token)

    def simulate_delete(self, path, token=None):
        return self._simulate_request(
            method='DELETE',
            path=path,
            data=None,
            token=token)