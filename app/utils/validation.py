import falcon
from cerberus import Validator


class BaseValidationMixin(object):

    def _validate_request(self, request_data):
        v = Validator(self.schema)
        if not v.validate(request_data):
            raise falcon.HTTPBadRequest('Bad request', v.errors)

    def validate_create(self, request_data):
        self._validate_request(request_data)

    def validate_update(self, request_data):
        self._validate_request(request_data)
