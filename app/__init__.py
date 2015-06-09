import falcon
from middleware.body_parser import JSONBody
from middleware.validation import RequestValidation


middleware = [JSONBody(), RequestValidation()]

api = falcon.API(middleware=middleware)


import routes
