from ...resources.card import CardManager 

from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from jwt.exceptions import ExpiredSignatureError

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('limit',
                    type=int,
                     help='''A limit on the number of objects to be returned. 
                     Limit can range between 1 and 100, and the default is 10.''',
                     required=False)

#################
# Method        #
#################


def Get(args, identify):
    limit = args['limit']
    
    cm = CardManager()
    result = cm.get_cards(identify, limit=limit)
    
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