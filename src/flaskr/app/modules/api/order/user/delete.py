from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Customer's token",
                    required=True,
                    location="headers")
#################
# Method        #
#################


def Delete(args):

    token = args[
        'Authorization']  #sends auth token to get user id and then the orders
    response = jsonify({
        "statusCode": 200,
        'message': 'Success',
        "data": {
            "Auth": token
        }
    })
    return response