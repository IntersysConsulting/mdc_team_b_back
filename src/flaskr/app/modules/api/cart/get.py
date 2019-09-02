from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument(
    'Authorization',
    help=
    "The autorization token bearer. This is a placeholder and should be handled with JWT.",
    required=True,
    location="headers")

#################
# Method        #
#################


def Get(args):
    token = args['Authorization']

    return jsonify({
        "statusCode": 200,
        "message": "OK",
        "data": {
            "Auth": token
        }
    })
