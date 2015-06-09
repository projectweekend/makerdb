import falcon

from app.utils.auth import hash_password, verify_password, generate_token
from validation import UserCreateMixin
from data import DataMixin, DuplicateUserError


class UserResource(UserCreateMixin, DataMixin):

    def __init__(self):
        super(UserResource, self).__init__()

    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])

        user = {
            'email': email,
            'password': password,
            'account_type': 'user'
        }

        try:
            self.add_user(user)
        except DuplicateUserError:
            title = 'Conflict'
            description = 'Email is already registered'
            raise falcon.HTTPConflict(title=title, description=description)

        user.pop('password')

        res.status = falcon.HTTP_201
        req.context['result'] = {
            'token': generate_token(user)
        }
