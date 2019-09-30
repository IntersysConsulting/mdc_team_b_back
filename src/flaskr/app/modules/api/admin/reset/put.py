from flask import jsonify, request, make_response
from flask_restplus.namespace import RequestParser, request
from ....resources.admin import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token)

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument(
    'access_code',
    help="Access code the user got in their email to reset their password",
    required=True)
Parser.add_argument('email',
                    help="The user's email",
                    required=True,
                    location='form')
Parser.add_argument('password',
                    help='The new password',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Put(args):
    email = args['email']
    password = args['password']
    code = args['access_code']

    am = AdminManagement()
    result, _id = am.reset_password(code, password, email)

    if result == 1:  # Successfully reset
        # Logs the user in
        access_token = create_access_token(identity=str(_id))
        refresh_token = create_refresh_token(identity=str(_id))

        response = jsonify({
            "statusCode": 200,
            "message": "Successfully reset the admin's password.",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    elif result == 0:  # Wrong code
        response = jsonify({
            "statusCode": 400,
            "message": "The access code is wrong.",
        })
    elif result == -1:  # User does not exist
        response = jsonify({
            "statusCode": 400,
            "message": "The account does not exist.",
        })
    elif result == -2:  # User did not request password change
        response = jsonify({
            "statusCode":
            400,
            "message":
            "The account did not request a password reset.",
        })
    elif result == -3:  # User's account is disabled
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Your account has been disabled. Contact an administrator.",
        })
    elif result == -4:  # We could not access the database at some point
        response = jsonify({
            "statusCode":
            500,
            "message":
            "We could not coonect to the database. Please contact an administrator."
        })
    else:  #Unexpected response
        response = jsonify({
            "statusCode": 400,
            "message": "Something went wrong",
        })

    return response
