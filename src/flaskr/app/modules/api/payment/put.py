from ...resources.card import CardManager 
from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('card_token',
                    help='Token returned from front end by Stripe.js',
                    required=True)

#################
# Method        #
#################

def Put(args, identify):
    token = args['card_token']    

    cm = CardManager()
    result = cm.add_card(identify, token)
    
    if result is 0:
        return jsonify({
            "statusCode": 200,
            "message": "Card info successfully updated"
        })
    elif result is -2:
        return jsonify({
            "statusCode": 400,
            "message": "A Guest can not have card added"
        })
    else:
        return jsonify({
            "statusCode": 400,
            "message": "Card info could not be added"
        })


    