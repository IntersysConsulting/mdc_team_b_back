from ...db import Database

class RevokedTokenModel():
    def __init__(self):
        self.collection_name = "token_blacklist"
        self.db = Database()

    def add_token(self, jti):
        self.db.create(self.collection_name, {
            "token": jti
        })

    def is_jti_blacklisted(jti):
        query = self.db.find(self.collection_name, jti)
        if query:
            return "successful"
        else:
            return "unsuccessful"
