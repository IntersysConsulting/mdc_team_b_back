from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager

#################
# Parser        #
#################
Parser = RequestParser()

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
Parser.add_argument('password',
                    help='Customer password',
                    required=True,
                    location='form')
Parser.add_argument('phone',
                    help='Customer phone number',
                    required=False,
                    location='form')

#################
# Method        #
#################


def Post(args, _id):
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']
    password = args['password']
    phone = 0 if not args['phone'] else args['phone']

    cm = CustomerManager()

    result = cm.create_new_customer(_id, first_name, last_name, email,
                                    password, phone)

    if result == 1:

        response = jsonify({
            "statusCode": 200,
            "message": "Successfully created customer account",
        })
    elif result == -1:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Email is already under use in the database",
        })
    elif result == -1:
        response = jsonify({
            "statusCode": 400,
            "message": "User is already registered",
        })
    else:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not create the requested account",
        })
    return response