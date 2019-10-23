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
Parser.add_argument('amount',
                    help='Amount to charge',
                    required=True)

#################
# Method        #
#################

def PayPut(args, identify):
    token = args['card']    
    amount = args['amount']

    cm = CardManager()
    pay_func = cm.whos_paying(identify)
    result = pay_func(identify, token, amount)
    
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