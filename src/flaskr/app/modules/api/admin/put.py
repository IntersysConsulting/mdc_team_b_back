from flask import jsonify, request, make_response
from flask_restplus.namespace import RequestParser, request
from ...resources.admin import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token)
from ...resources.validation import is_admin, is_not_admin_response
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('current_password',
                    help='Current password of admin',
                    required=True,
                    location='form')
Parser.add_argument('first_name',
                    help='First name of the admin',
                    required=True,
                    location='form')
Parser.add_argument('last_name',
                    help='Last name of the admin',
                    required=True,
                    location='form')
Parser.add_argument('new_password',
                    help='Password that will replace the current one',
                    required=False,
                    location='form')

#################
# Method        #
#################


def Put(args, identity):
    if not is_admin(identity):
        response = is_not_admin_response
    else:
        password = args["current_password"]
        first_name = args["first_name"]
        last_name = args["last_name"]
        new_password = None if not args["new_password"] else args[
            "new_password"]
        am = AdminManagement()
        #Implement the method here

        response = jsonify({
            "statusCode": 500,
            "message": "Not yet implemented"
        })

    return response
