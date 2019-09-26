from passlib.hash import pbkdf2_sha256 as sha256


def hash_password(self, password):
    return sha256.hash(password)


def verify_hash(self, password, hash):
    return sha256.verify(password, hash)
