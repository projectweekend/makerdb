import falcon
from cerberus import Validator


class UserCreateMixin(object):

    schema = {
        'email': {
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'password': {
            'type': 'string',
            'required': True,
            'minlength': 8
        },
    }

    def validate_create(self, request_data):
        v = Validator(self.schema)
        if not v.validate(request_data):
            raise falcon.HTTPBadRequest('Bad request', v.errors)
