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
Parser.add_argument(
    'quantity',
    help="Quantity of this product to be added to the cart. Default: 1",
    required=False)

#################
# Method        #
#################


def Post(args):
    token = args['Authorization']
    pid = args['product_id']
    quantity = 0 if not args['quantity'] else args['quantity']

    return jsonify({
        "statusCode": 200,
        "message": "No changes",
        "data": {
            "Auth": token,
            "product_id": pid,
            "quantity": quantity
        }
    })
