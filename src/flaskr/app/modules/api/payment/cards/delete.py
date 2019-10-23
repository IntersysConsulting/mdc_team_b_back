from ....resources.card import CardManager 
from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('card_id',
                    help='ID of the card to be removed.',
                    required=True)
#################
# Method        #
#################


def Delete(args, identify):
    card_id = args['card_id']
    
    cm = CardManager()
    result = cm.delete_card(identify, card_id)
    
    if  result:
        return jsonify({
            "statusCode": 200,
            "message": "Card information was deleted succesfully"
        })
    else:
        return jsonify({
            "statusCode": 400,
            "message": "Card ID does not exist"
        })