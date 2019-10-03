from flask import jsonify, Flask
from ....resources.token import revoke_token
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (jwt_required, get_raw_jwt)

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help='Token of the admin.',
                    required=True,
                    location='headers')

#################
# Method        #
#################


@jwt_required
def Delete(args):
    '''
    jti = unique identifier of the token
    '''
    jti = get_raw_jwt()['jti']
    print(jti)
    try:
        revoke_token(jti)
        response = jsonify({
            'message': 'Access token has been revoked',
            "statusCode": 200
        })
    except:
        response = jsonify({
            'message': 'Something went wrong',
            "statusCode": 500
        })
    return response
