import os
from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from modules.api import api, v1_blueprint

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
# api.init_app(app)
app.register_blueprint(v1_blueprint)


@app.route('/')
def redirect_to_default_api_swagger():
    return redirect('/api/v1')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
