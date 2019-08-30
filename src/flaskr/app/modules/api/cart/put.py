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
Parser.add_argument(
    'product_id',
    help="The ObjectID of the product to be affected.",
    required=True)
Parser.add_argument(
    'quantity',
    type=int,
    help="The new quantity of the product. Must be greater than 0.",
    required=True)

#################
# Method        #
#################

def Put(args):
    token = args['Authorization']
    pid = args['product_id']
    quantity = args['quantity']

    code = 200 if quantity > 0 else 406
    msg = "OK" if quantity > 0 else "Less than 1"
    return jsonify({
        "statusCode": code,
        "data": {
            "Auth": token,
            "product_id": pid,
            "quantity": quantity
        }
    })