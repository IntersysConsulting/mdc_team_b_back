from flask import jsonify
from ....resources.admin  import AdminManagement
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument("email",
                    help="Admin's e-mail tied to their account.",
                    required=True,
                    location="form")
Parser.add_argument("password",
                    help="Admin's password.",
                    required=True,
                    location="form")
#################
# Method        #
#################


def Post(args):
    email = args['email']
    password = args['password']

    am = AdminManagement()
    if am.login_admin(email, password):
        acces_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response = jsonify({
            "statusCode": 200,
            "message": "Successfully logged in",
            "data": {
                "acces_token": acces_token
            }
        })

        return response


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            acces_token = create_access_token(identity= data['username'])
            refresh_token = create_refresh_token(identity= data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'acces_token': acces_token,
                'refresh_token': refresh_token,
            }
        else:
            return {'message': 'Wrong credentials'}
