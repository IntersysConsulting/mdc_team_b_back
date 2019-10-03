from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_restplus import inputs
from ....resources.customer import CustomerManager
#################
# Parser        #
#################
Parser = RequestParser()
#We need the old address to find the object we will replace
Parser.add_argument('index',
                    type=int,
                    required=True,
                    location='form',
                    help="Index of the address to be updated")
Parser.add_argument('address', required=False, location='form')
Parser.add_argument('between', required=False, location='form')
Parser.add_argument('country', required=False, location='form')
Parser.add_argument('state', required=False, location='form')
Parser.add_argument('city', required=False, location='form')
Parser.add_argument('zip_code', required=False, location='form')
Parser.add_argument('first_name', required=False, location='form')
Parser.add_argument('last_name', required=False, location='form')
Parser.add_argument('delivery_notes', required=False, location='form')
Parser.add_argument(
    'is_default',
    help=
    'Blank for false, filled in if you want to override the current default',
    type=inputs.boolean,
    required=False,
    location='form')
#################
# Method        #
#################


def Put(args, identity):
    index = args['index']
    address = args['address']
    between = args['between']
    country = args['country']
    state = args['state']
    city = args['city']
    zip_code = args['zip_code']
    first_name = args['first_name']
    last_name = args['last_name']
    delivery_notes = args['delivery_notes']
    is_default = args['is_default']

    cm = CustomerManager()
    result = cm.update_shipping(identity, index, address, between, country, state, city,
                               zip_code, first_name, last_name, delivery_notes, is_default)

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
            "message": "Could not update the billing address",
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully updated a billing address",
        })
    else:
        response = jsonify({
            "statusCode": 500,
            "message": "Unexpected result = {}".format(result),
        })
    return response