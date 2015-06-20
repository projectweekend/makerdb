import falcon
from middleware.body_parser import JSONBody
from middleware.auth import AuthUser
from middleware.validation import RequestValidation


middleware = [
    AuthUser(),
    JSONBody(),
    RequestValidation()
]

api = falcon.API(middleware=middleware)


import routes
