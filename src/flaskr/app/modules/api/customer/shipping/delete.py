from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                                    help="Customer Token",
                                    required=True,
                                    location='headers')
Parser.add_argument(
    'shipping',
    help="JSON object of the address to be deleted",
    required=True,
    location="form")
#################
# Method        #
#################


def Delete(args):
    
    token = args['Authorization']
    shipping = args['shipping']
    response = jsonify({
        "statusCode": 200,
        "message": "Successfully updated a shipping address",
        "data": {
            "Auth": token,
            "shipping": shipping
        }
    })
    return response