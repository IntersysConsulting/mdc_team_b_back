from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help='Token of the customer.',
                    required=True,
                    location='headers')

#################
# Method        #
#################


def Delete(args):
    response = jsonify({
        "statusCode": 200,
        'message': "Succesfully logged out",
        "data": {
            "token": args["Authorization"]
        }
    })
    return response