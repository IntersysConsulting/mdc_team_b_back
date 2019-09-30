from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError
from ...resources.cart import CartManager

#################
# Parser        #
#################

Parser = RequestParser()

#################
# Method        #
#################


@jwt_required
def Get(args, identity):

    cm = CartManager()

    try:
        if identity is not None:
            result = cm.get_cart(identity)
            if result != None:
                response = jsonify({
                    "statusCode": 200,
                    "message": "OK",
                    "data": {
                        "cart": result
                    }
                })
            else:
                response = jsonify({
                    "statusCode":
                    400,
                    "message":
                    "Could not find a cart for that ID."
                })
    except ExpiredSignatureError:

        response = jsonify({
            "statusCode": 401,
            "message": "Invalid or missing credentials",
            "data": {
                "Auth": token
            }
        })

    return response
