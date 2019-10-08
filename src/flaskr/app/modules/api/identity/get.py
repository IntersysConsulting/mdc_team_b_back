from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources import validation

#################
# Parser        #
#################

#################
# Method        #
#################


def Get(identity):

    if validation.is_guest(identity):
        role = "Guest"
    elif validation.is_customer(identity):
        role = "Customer"
    elif validation.is_admin(identity):
        role = "Admin"
    else:
        role = "Unknown / None"

    response = jsonify({"statusCode": 200, "message": "Success", "role": role})

    return response