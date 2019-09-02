#   Implement https://pythonhosted.org/Flask-JWT/
#   In this file authenticate() and identity() should be handled
from passlib.hash import pbkdf2_sha256 as sha256

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}