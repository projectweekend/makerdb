import falcon
from psycopg2 import IntegrityError
from app.utils.auth import hash_password, verify_password, generate_token
from app.user.validation import UserCreateMixin, UserAuthenticateMixin

USER_FIELDS = ['id', 'email', 'password', 'is_active', 'is_admin']
USER_TOKEN_FIELDS = ['id', 'email', 'is_active', 'is_admin']


class UserResource(UserCreateMixin):

    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])

        try:
            self.cursor.callproc('sp_users_insert', [email, password])
        except IntegrityError:
            title = 'Conflict'
            description = 'Email in use'
            raise falcon.HTTPConflict(title, description)

        result = self.cursor.fetchone()

        req.context['result'] = {'token': generate_token(result[0])}
        res.status = falcon.HTTP_CREATED


class AuthenticationResource(UserAuthenticateMixin):

    def on_post(self, req, res):
        unauthorized_title = 'Unauthorized'
        unauthorized_description = 'Invalid credentials'

        email = req.context['data']['email']
        password = req.context['data']['password']

        self.cursor.callproc('sp_lookup_user_by_email', [email, ])

        result = self.cursor.fetchone()
        if result is None:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        user_dict = dict(zip(USER_FIELDS, result))

        valid_password = verify_password(password, user_dict.pop('password'))
        if not valid_password:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        req.context['result'] = {'token': generate_token(user_dict)}
        res.status = falcon.HTTP_OK
