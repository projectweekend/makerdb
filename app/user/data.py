import json


class DataManagerMixin(object):

    def add_user(self, user_doc):
        self.cursor.callproc('sp_users_insert', [json.dumps(user_doc), ])
        result = self.cursor.fetchone()
        try:
            return result[0]
        except IndexError:
            return None
