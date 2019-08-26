from flask import Flask
from app.modules.db import Database
from app.modules.api import api

db = Database()


def create_app(config_type='dev'):
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_type])  
    api.init_app(app)

    return app

if __name__ == '__main__':
    app = Flask(__name__)
    api.init_app(app)
    app.run(debug=True)    