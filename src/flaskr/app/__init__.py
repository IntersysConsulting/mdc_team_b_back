from flask import Flask
from .modules.db import Database
from .modules.api import api, v1_blueprint

def create_app(config_type='dev'):
    from config import config
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'intersysecommerce@gmail.com'
    app.config['MAIL_PASSWORD'] = 'IntersysConsulting3#'

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    app.config.from_object(config[config_type])
    app.register_blueprint(v1_blueprint)

    return app


if __name__ == '__main__':
    app = Flask(__name__)
    # api.init_app(app)
    app.register_blueprint(v1_blueprint)
    app.run(debug=True)
