from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError
from ...resources.cart import CartManager

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('product_id',
                    help="The ObjectID of the product to be affected.",
                    required=True)

#################
# Method        #
#################

@jwt_required
def Delete(args, identity):
    pid = args['product_id']
    cm = CartManager()
    response = None
    try:
        if identity is not None:
            cart = cm.get_cart(identity)
            if len(cart):
                result = cm.delete_cart(identity, pid, cart)
                if result == 0:
                    response = jsonify({
                    "statusCode":
                    204,
                    "message":
                    "Product was not in cart."
                })

                if result == 1:
                    response = jsonify({
                    "statusCode":
                    200,
                    "message":
                    "Product was deleted successfully from the cart."
                })                    
                
                if result == 2:
                    response = jsonify({
                    "statusCode":
                    400,
                    "message":
                    "Product does not exist."
                })

                

    except ExpiredSignatureError:
        response = jsonify({
            "statusCode": 401,
            "message": "Invalid or missing credentials",
            "data": {
                "Auth": identity
            }
        })
    
    return response