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
Parser.add_argument('product_id',
                    help="The ObjectID of the product to be affected.",
                    required=True)

#################
# Method        #
#################


def Post(args):
    token = args['Authorization']
    pid = args['product_id']

    return jsonify({
        "statusCode": 200,
        "message": "No changes",
        "data": {
            "Auth": token,
            "product_id": pid
        }
    })
