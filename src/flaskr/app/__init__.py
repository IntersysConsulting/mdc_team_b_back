from flask import Flask
from modules.db import Database
from modules.api import api, v1_blueprint

db = Database()


def create_app(config_type='dev'):
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_type])
    # api.init_app(app)
    app.register_blueprint(v1_blueprint)

    return app


if __name__ == '__main__':
    app = Flask(__name__)
    # api.init_app(app)
    app.register_blueprint(v1_blueprint)
    app.run(debug=True)
