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
    return jsonify({
        "statusCode": 200,
        "message": "OK"
    })