from app import api
from user import handlers as user_handlers


api.add_route('/v1/user', user_handlers.UserResource())