import os
from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from modules.api import api, v1_blueprint
from modules.resources.reset_token import RevokedTokenModel

app = Flask(__name__)

mail = Mail()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'intersysecommerce@gmail.com'
app.config['MAIL_PASSWORD'] = 'IntersysConsulting3#'

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

app.register_blueprint(v1_blueprint)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

@app.route('/')
def redirect_to_default_api_swagger():
    return redirect('/api/v1')


if __name__ == "__main__":
    mail.init_app(app)
    app.run(host="127.0.0.1", port="5000", debug=True)
