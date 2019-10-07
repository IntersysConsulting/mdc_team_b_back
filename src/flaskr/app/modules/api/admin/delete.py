from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.validation import is_admin, is_not_admin_response
from ...resources.admin import AdminManagement
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
        admin_id = args['id']
        print("{} == {} ? ".format(identity, admin_id))
        if identity == admin_id:
            response = jsonify({
                "statusCode": 406,
                "message": "Admin can not delete itself."
            })
        else:
            am = AdminManagement()
            result = am.delete_admin(admin_id)
            if result == 1:
                response = jsonify({
                    "statusCode": 200,
                    "message": "Successfully deleted admin"
                })
            elif result == 0:
                response = jsonify({
                    "statusCode":
                    406,
                    "message":
                    "Could not delete admin. Either didn't exist or failed to delete."
                })
            else:
                response = jsonify({
                    "statusCode":
                    500,
                    "message":
                    "Unexpected result={}".format(result)
                })
    return response