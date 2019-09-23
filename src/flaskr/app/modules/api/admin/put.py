from flask import jsonify, request, make_response
from flask_restplus.namespace import RequestParser, request
from ...resources.admin  import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token)

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Admin's session token",
                    required=True)
Parser.add_argument('current_password',
                    help='Current password of admin',
                    required=True,
                    location='form')
Parser.add_argument('password',
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

def Put(args):
    am = AdminManagement()
    response = jsonify({"": ""})
    if args['code'] and args['email']:
        response = am.create_password(args['code'], args['password'], args['email'])

    return response
