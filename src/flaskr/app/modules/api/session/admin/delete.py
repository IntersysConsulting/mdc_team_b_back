from flask import jsonify, Flask
from ....resources.reset_token import RevokedTokenModel
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import ( jwt_required, get_raw_jwt )

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
    jti = ""+jti +""
    print(jti)
    try:
        revoked_token = RevokedTokenModel()
        revoked_token.add_token(jti)
        return {'message': 'Access token has been revoked'}
    except:
        return {'message': 'Something went wrong'}, 500
    response = jsonify({
        "statusCode": 200,
        'message': "Succesfully logged out",
        "data": {
            "token": args["Authorization"]
        }
    })
    return response
