from ....resources.card import CardManager 
from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError

#################
# Parser        #
#################

Parser = RequestParser()

#################
# Method        #
#################


def Get(args, identify):    
    cm = CardManager()
    result = cm.get_cards(identify)
    
    if result is not None:
        return jsonify({
            "statusCode": 200,
            "message": "OK",
            "data": {
                "cards": result 
            }
        })
    else:
        return jsonify({
            "statusCode": 400,
            "message": "No cards registered"
        })