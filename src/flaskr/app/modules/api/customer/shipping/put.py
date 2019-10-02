from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
#We need the old address to find the object we will replace
Parser.add_argument('old_shipping_address',
                    help='Old billing address JSON object',
                    required=True,
                    location='form')
Parser.add_argument('shipping',
                    help='New shipping address JSON object',
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


def Put(args):    
    token = args['Authorization']
    old_shipping = args['old_shipping_address']
    shipping = args['shipping']
    is_default = args['is_default']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully",
        "data": {
            "Auth": token,
            "old_shipping_address": old_shipping,
            "shipping": shipping,
            "is_default": is_default
        }
    })
    return response