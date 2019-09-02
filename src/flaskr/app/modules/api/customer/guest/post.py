from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()

#################
# Method        #
#################


def Post():
    response = jsonify({
        "statusCode": 200,
        "message": "Successfully created guest account",
        "data": {
            "Authorization":
            "bearer token (Here goes whatever JWT is generated)"
        }
    })

    return response