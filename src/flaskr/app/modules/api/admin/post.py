from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.admin import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from ...resources.password_management import hash_password, verify_hash
from ...resources.mail.reset_password import send_reset_password_email

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('first_name',
                    help='First name of the admin to be registered',
                    required=True,
                    location='form')
Parser.add_argument('last_name',
                    help='Last name of the admin to be registered',
                    required=True,
                    location='form')
Parser.add_argument(
    'email',
    help='Email address under which the admin will be registered',
    required=True,
    location='form')

#################
# Method        #
#################


def Post(args):
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']

    am = AdminManagement()

    try:
        result, accessCode = am.create_admin(first_name, last_name, email)

        if result == 1:
            # We could make the admin and reset it's password. Email was sent through AM.
            send_reset_password_email(accesCode, email)
            return jsonify({
                "statusCode":
                200,
                "message":
                "Created admin and requested password reset."
            })
        elif result == 2:
            return jsonify({
                "statusCode":
                206,
                "message":
                "Created the admin but could not reset password."
            })
        elif result == 0:
            return jsonify({
                "statusCode": 400,
                "message": "Could not make the admin."
            })
        elif result == -1:
            return jsonify({
                "statusCode":
                410,
                "message":
                "There is an admin with that email already."
            })
        else:
            return jsonify({"statusCode": 400, "message": "Unexpected error."})
    except Exception:
        return jsonify({"statusCode": 500, 'message': "Internal server error"})
