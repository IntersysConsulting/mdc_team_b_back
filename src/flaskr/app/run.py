import os
from flask_restplus import Api, Namespace, Resource
from flask import Flask, redirect, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from modules.api import v1_blueprint
from modules.resources.reset_token import RevokedTokenModel


app = Flask(__name__)
# CORS(app, resources={ r"*": { 'origins': 'http://localhost:3000' } })
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

# v1_blueprint = Blueprint('api', __name__, url_prefix='/api/v1/')
app.register_blueprint(v1_blueprint)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

if __name__ == "__main__":
    mail.init_app(app)
    app.run(host="127.0.0.1", port="5000", debug=True)
