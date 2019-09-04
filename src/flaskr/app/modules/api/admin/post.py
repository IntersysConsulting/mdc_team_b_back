from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.admin  import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

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
    if am.find_admin(email):
        return jsonify({
            'message': 'User {} already exists'.format(email)
        })

    try:
        am.create_admin(first_name, last_name, email)

        acces_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        return jsonify({
            "statusCode": 200,
            "message": "Successfully created new admin",
            "acces_token": acces_token,
            "refresh_token": refresh_token,
            "data": {
                "user": 'helolo'
            }
        })
    except Exception:
        return jsonify({
            'message': Exception
        })
