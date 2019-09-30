from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('first_name',
                    help='Customer first name',
                    required=False,
                    location='form')
Parser.add_argument('last_name',
                    help='Customer last name',
                    required=False,
                    location='form')
Parser.add_argument('email',
                    help='Customer email',
                    required=False,
                    location='form')
Parser.add_argument('phone',
                    help='Customer phone number',
                    required=False,
                    location='form')
#################
# Method        #
#################


def Put(args, identity):
    first_name = None if not args['first_name'] else args['first_name']
    last_name = None if not args['last_name'] else args['last_name']
    email = None if not args['email'] else args['email']
    phone = None if not args['phone'] else args['phone']
    # This endpoint was reached thanks to them accepting the TOS, so the timestamp should just be now.
    # We should not let anyone send a timestamp as this could lead to fake timestamps.

    cm = CustomerManager()
    result = cm.update_info(identity, first_name, last_name, email, phone)

    if result == -3:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "That email is already claimed by a customer."
        })
    elif result == -2:
        response = jsonify({
            "statusCode": 400,
            "message": "There is no customer with this ID!"
        })
    elif result == -1:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Guests can not leave first_name, last_name or email blank."
        })
    elif result == 0:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Could not update the customer's information."
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully updated guest information"
        })
    else:
        response = jsonify({
            "statusCode": 500,
            "message":
            "The server returned this result value, but it's not handled",
            "result": result
        })

    return response