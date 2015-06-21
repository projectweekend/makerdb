from app.utils.database import database_connection

db = database_connection()


class DatabaseCursorOpen(object):

    def process_resource(self, req, resp, resource):
        resource.db = db
        resource.cursor = db.cursor()


class DatabaseCursorClose(object):

    def process_response(self, req, resp, resource):
        resource.cursor.close()
