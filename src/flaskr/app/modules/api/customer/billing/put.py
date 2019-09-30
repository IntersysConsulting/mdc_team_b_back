from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
#We need the old address to find the object we will replace
Parser.add_argument('old_billing_address',
                    help='Old billing address JSON object',
                    required=True,
                    location='form')
Parser.add_argument('billing',
                    help='New billing address JSON object',
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
    old_billing = args['old_billing_address']
    billing = args['billing']
    is_default = args['is_default']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully updated a billing address",
        "data": {
            "Auth": token,
            "old_billing_address": old_billing,
            "billing": billing,
            "is_default": is_default
        }
    })
    return response