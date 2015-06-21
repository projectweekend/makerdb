import json


class DataManagerMixin(object):

    def add_user(self, user_doc):
        self.cursor.callproc('sp_users_insert', [json.dumps(user_doc), ])
        result = self.cursor.fetchone()
        return result[0]

    def find_user_by_email(self, email):
        self.cursor.callproc('sp_users_select_by_email', [email, ])
        result = self.cursor.fetchone()
        return result[0] if result else None
