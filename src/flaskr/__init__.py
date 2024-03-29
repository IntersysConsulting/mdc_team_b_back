from flask import Flask
from os import environ
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    port = int(environ['PORT'])
    app.run(host='0.0.0.0', port=port)
