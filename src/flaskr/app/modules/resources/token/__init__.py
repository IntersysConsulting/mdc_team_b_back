from ...db import Database

db = Database()
collection_name = "token_blacklist"


def revoke_token(jti):
    db.create(collection_name, {"token": jti})


def is_revoked(jti):
    '''
    Checks the database to see if a token is revoked (User logged out)
    Returns true if the JTI is in the database
    '''
    token = db.find(collection_name, {"token": jti})

    return token != None
