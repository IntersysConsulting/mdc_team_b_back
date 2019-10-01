from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.validation import is_admin, is_not_admin_response
#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('id',
                    help='ID of the admin to be deleted',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Delete(args, identity):

    if not is_admin(identity):
        response = is_not_admin_response
    else:
        pass

    admin_id = args['id']

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully deleted admin",
        "data": {
            "id": admin_id
        }
    })
    return response