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
        query = Database.find(self.collection_name, jti)
        return bool(query)
