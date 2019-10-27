from ....resources.card import CardManager 
from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('card',
                    help='''This will expect an card_id o a token from Stripe.js''',
                    required=True)
                    
Parser.add_argument('order_id',
                    help=r"Order's identifier",
                    required=True)

#################
# Method        #
#################

CLIENT = 1
GUEST = 0

def PayPut(args, identify):
    token = args['card']    
    order_id = args['order_id']

    cm = CardManager()
    pay_func = cm.whos_paying(identify)
    if pay_func:
        result = cm.put_charge_customer(identify, order_id, token)
    else:
        result = cm.put_charge_guest(order_id, token)

    if result is 0:
        return jsonify({
            "statusCode": 200,
            "message": "Successfully charged"
        })
    if result is -1:
         return jsonify({
            "statusCode": 400,
            "message": "Error while trying top make the charge"
        })
    else:
         return jsonify({
            "statusCode": 400,
            "message": "The card's ID format is not correct"
        })