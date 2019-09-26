from flask import jsonify
from flask_restplus import Resource
from ....resources.admin import AdminManagement
from flask_restplus.namespace import RequestParser
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

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
    result, _id = am.login_admin(email, password)

    if result == 1:
        access_token = create_access_token(identity=_id)
        refresh_token = create_refresh_token(identity=_id)

        response = jsonify({
            "statusCode": 200,
            "message": "Welcome admin",
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
    elif result == 0:
        response = jsonify({"statusCode": 400, "message": "Wrong password"})
    elif result == -1:
        response = jsonify({"statusCode": 400, "message": "Wrong email"})
    else:
        response = jsonify({"statusCode": 400, "message": "Unexpected error"})
        return response
