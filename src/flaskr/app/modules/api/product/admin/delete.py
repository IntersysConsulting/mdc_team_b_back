from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Admin's token",
                    required=True,
                    location="headers")
Parser.add_argument('id',
                    type=int,
                    help='ID of the product to be deleted',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Delete(args):
    pId = args['id']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully deleted a product",
        "data": {
            "id": pId
        }
    })
    return response