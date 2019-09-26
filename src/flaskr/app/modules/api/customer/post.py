from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('Authorization',
                    help='Token the guest had before making their account.',
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


def Post(args):
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']
    password = args['password']
    phone = 0 if not args['phone'] else args['phone']

    cart = 1  #This should ask the resource to make a cart, then assign the cart's ID to this field

    cm = CustomerManager()

    cm.add(first_name, last_name, email, password, phone)

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully created customer account",
    })
    return response