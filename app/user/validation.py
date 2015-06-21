from app.utils.validation import BaseValidationMixin


class UserValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'email': {
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'password': {
            'type': 'string',
            'required': True,
            'minlength': 8
        }
    }


class AuthenticateValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'email': {
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'password': {
            'type': 'string',
            'required': True
        }
    }
