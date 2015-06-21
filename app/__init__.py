import falcon
from middleware.body_parser import JSONBodyParser
from middleware.json_response import JSONResponse
from middleware.auth import AuthUser
from middleware.validation import RequestValidation
from middleware.database import DatabaseCursorOpen, DatabaseCursorClose


middleware = [
    JSONBodyParser(),
    AuthUser(),
    DatabaseCursorOpen(),
    DatabaseCursorClose(),
    JSONResponse(),
    RequestValidation()]

api = falcon.API(middleware=middleware)


import routes
