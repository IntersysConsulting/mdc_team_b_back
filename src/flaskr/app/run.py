import os
from flask import Flask
from modules.api import api


app = Flask(__name__)
api.init_app(app)

if __name__ == "__main__": 
    app.run(host="127.0.0.1", port="5000", debug=True)