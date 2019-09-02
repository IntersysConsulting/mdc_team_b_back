from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help='Customer token',
                    required=True,
                    location='headers')

#################
# Method        #
#################


def Get(args):
    token = args['Authorization']

    #Here we get all the customer account details. Then we probably save it on backend.
    response = jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": {
            "Auth": token
        }
    })
    return response