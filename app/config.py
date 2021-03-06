import os


TWO_WEEKS = 1209600
TOKEN_EXPIRES = TWO_WEEKS

SECRET_KEY = os.getenv('SECRET_KEY', None)
assert SECRET_KEY

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgres://postgres@{0}:5432/postgres'.format(os.getenv('DB_PORT_5432_TCP_ADDR', None)))
assert DATABASE_URL
