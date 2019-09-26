from passlib.hash import pbkdf2_sha256 as sha256


def hash_password(password):
    return sha256.hash(password)


def verify_hash(password, hash):
    return sha256.verify(password, hash)
