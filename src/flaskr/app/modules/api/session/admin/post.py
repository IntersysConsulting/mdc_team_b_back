from flask import jsonify
from flask_restplus.namespace import RequestParser

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

    token = "This_would_be_a_JWT_token_for_the_user"
    response = jsonify({
        "statusCode": 200,
        "message": "Successfully logged in",
        "data": {
            "token": token
        }
    })
    return response