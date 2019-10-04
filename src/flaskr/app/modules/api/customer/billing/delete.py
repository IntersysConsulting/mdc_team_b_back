from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.customer import CustomerManager
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('index',
                    help="Index of the address to be deleted",
                    type=int,
                    required=True,
                    location="form")

#################
# Method        #
#################


def Delete(args, identity):
    index = args['index']
    cm = CustomerManager()
    result = cm.delete_billing(identity, index)

    if result == -2:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Address index given is out of the array.",
        })
    elif result == -1:
        response = jsonify({
            "statusCode": 400,
            "message": "User is not a customer",
        })
    elif result == 0:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not delete the billing address",
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully deleted a billing address",
        })
    else:
        response = jsonify({
            "statusCode": 500,
            "message": "Unexpected result = {}".format(result),
        })
    return response