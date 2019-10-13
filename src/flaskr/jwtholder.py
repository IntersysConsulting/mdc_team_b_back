import os

from app import create_app
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from app.modules.resources.token import is_revoked

try:
    app = create_app(os.environ['CONFIG_TYPE'])
except KeyError:
    app = create_app(config_type='dev')

mail = Mail()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'intersysecommerce@gmail.com'
app.config['MAIL_PASSWORD'] = 'IntersysConsulting3#'

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    result = is_revoked(jti)
    return result