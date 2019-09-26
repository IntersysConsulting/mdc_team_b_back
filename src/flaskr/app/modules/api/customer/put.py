from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('Authorization',
                    help='Guest token',
                    required=True,
                    location='headers')
Parser.add_argument('first_name',
                    help='Customer first name',
                    required=True,
                    location='form')
Parser.add_argument('last_name',
                    help='Customer last name',
                    required=True,
                    location='form')
Parser.add_argument('email',
                    help='Customer email',
                    required=True,
                    location='form')
Parser.add_argument('phone',
                    help='Customer phone number',
                    required=False,
                    location='form')
#################
# Method        #
#################


def Put(args):
    token = args['Authorization']
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']
    phone = 0 if not args['phone'] else args['phone']
    # This endpoint was reached thanks to them accepting the TOS, so the timestamp should just be now.
    # We should not let anyone send a timestamp as this could lead to fake timestamps.
    

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully updated guest information",
        "data": {
            "Auth": token,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "ToS": ToS
        }
    })
    return response