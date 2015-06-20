from urlparse import urlparse
import falcon
from cerberus import Validator


class CustomValidator(Validator):

    def _validate_url_or_blank(self, url_or_blank, field, value):
        if url_or_blank and value != '':
            parsed = urlparse(value)
            valid_scheme = parsed.scheme in ['http', 'https']
            valid_netloc = parsed.netloc != ''
            valid_path = parsed.path != ''
            if not valid_scheme or not valid_netloc or not valid_path:
                self._error(field, 'Must be a valid URL')


class BaseValidationMixin(object):

    def _validate_request(self, request_data):
        v = CustomValidator(self.schema)
        if not v.validate(request_data):
            raise falcon.HTTPBadRequest('Bad request', v.errors)

    def validate_create(self, request_data):
        self._validate_request(request_data)

    def validate_update(self, request_data):
        self._validate_request(request_data)
