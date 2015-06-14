import falcon

from app.utils.auth import hash_password, verify_password, generate_token
from validation import UserCreateMixin, UserAuthenticateMixin
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

        req.context['result'] = {
            'token': generate_token(user)
        }
        res.status = falcon.HTTP_201


class AuthenticateResource(UserAuthenticateMixin, DataMixin):

    def __init__(self):
        super(AuthenticateResource, self).__init__()

    def on_post(self, req, res):
        email = req.context['data']['email']
        password = req.context['data']['password']

        user = self.find_user(email)
        if not user or not verify_password(password, user.pop('password')):
            title = 'Unauthorized',
            description = 'Credentials are not valid'
            raise falcon.HTTPUnauthorized(title=title, description=description)

        req.context['result'] = {
            'token': generate_token(user)
        }
        res.status = falcon.HTTP_200
