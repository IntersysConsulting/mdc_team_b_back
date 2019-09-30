from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('billing',
                    help="JSON object of the address to be deleted",
                    required=True,
                    location="form")
#################
# Method        #
#################


def Delete(args):
    token = args['Authorization']
    billing = args['billing']
    response = jsonify({
        "statusCode": 200,
        "message":"Successfully updated a billing address",
        "data": {
            "Auth": token,
            "billing": billing
        }
    })
    return response