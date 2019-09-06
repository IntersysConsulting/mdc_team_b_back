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
                "acces_token": acces_token,
                "refresh_token": refresh_token
            }
        })

        return response
