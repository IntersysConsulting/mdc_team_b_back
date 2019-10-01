from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
#################
# Method        #
#################


def Delete(args, identity):

    response = jsonify({
        "statusCode": 200,
        'message': 'Success'
    })
    return response