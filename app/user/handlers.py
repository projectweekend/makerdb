import falcon
from psycopg2 import IntegrityError
from app.utils.auth import hash_password, verify_password, generate_token
from app.user.validation import UserCreateMixin, UserAuthenticateMixin
from app.user.data import DataManagerMixin


class UserResource(UserCreateMixin, DataManagerMixin):

    def on_post(self, req, res):
        user_doc = {
            'email': req.context['data']['email'],
            'password': hash_password(req.context['data']['password'])
        }
        try:
            new_user = self.add_user(user_doc)
        except IntegrityError:
            title = 'Conflict'
            description = 'Email in use'
            raise falcon.HTTPConflict(title, description)
        req.context['result'] = {'token': generate_token(new_user)}
        res.status = falcon.HTTP_CREATED


class AuthenticationResource(UserAuthenticateMixin):

    def on_post(self, req, res):
        unauthorized_title = 'Unauthorized'
        unauthorized_description = 'Invalid credentials'

        email = req.context['data']['email']
        password = req.context['data']['password']

        self.cursor.callproc('sp_users_select_by_email', [email, ])

        result = self.cursor.fetchone()
        if result is None:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        user = result[0]

        valid_password = verify_password(password, user.pop('password'))
        if not valid_password:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        req.context['result'] = {'token': generate_token(user)}
        res.status = falcon.HTTP_OK
