from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Customer's token",
                    required=True,
                    location="headers")

#################
# Method        #
#################


def Post(args):
    token = args['Authorization']
    timestamp = 0
    response = jsonify({
        "statusCode": 200,
        'message': 'Order succesfully added',
        "data": {
            "Auth": token,
        }
    })
    return response