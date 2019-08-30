from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Admin's session token",
                    required=True)
Parser.add_argument('id',
                    type=int,
                    help='ID of the admin to be deleted',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Delete(args):
    admin_id = args['id']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully deleted admin",
        "data": {
            "id": admin_id
        }
    })
    return response