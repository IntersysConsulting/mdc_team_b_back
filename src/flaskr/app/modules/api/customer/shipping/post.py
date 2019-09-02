from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                              help='Customer token',
                              required=True,
                              location='form')
Parser.add_argument('shipping',
                              help='Shipping address JSON object',
                              required=True,
                              location='form')
Parser.add_argument(
    'is_default',
    help='Whether the address getting updated is going to be the new default',
    required=True,
    location='form')

#################
# Method        #
#################


def Post(args):
    token = args['Authorization']
    shipping = args['shipping']
    is_default = args['is_default']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully",
        "data": {
            "Auth": token,
            "shipping": shipping,
            "is_default": is_default
        }
    })
    return response