from flask import jsonify
from flask_restplus.namespace import RequestParser

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

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully created new admin",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
    })
    return response