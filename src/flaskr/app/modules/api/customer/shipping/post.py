from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.customer import CustomerManager
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('address', required=True, location='form')
Parser.add_argument('between', required=True, location='form')
Parser.add_argument('country', required=True, location='form')
Parser.add_argument('state', required=True, location='form')
Parser.add_argument('city', required=True, location='form')
Parser.add_argument('zip_code', required=True, location='form')
Parser.add_argument('first_name', required=True, location='form')
Parser.add_argument('last_name', required=True, location='form')
Parser.add_argument('delivery_notes', required=False, location='form')
Parser.add_argument(
    'is_default',
    help=
    'Blank for false, filled in if you want to override the current default',
    type=bool,
    required=False,
    location='form')

#################
# Method        #
#################


def Post(args, identity):
    address = args['address']
    between = args['between']
    country = args['country']
    state = args['state']
    city = args['city']
    zip_code = args['zip_code']
    first_name = args['first_name']
    last_name = args['last_name']
    is_default = False if not args['is_default'] else True
    delivery_notes = args['delivery_notes']

    cm = CustomerManager()
    result = cm.add_shipping(identity, address, between, country, state, city,
                             zip_code, first_name, last_name, delivery_notes,
                             is_default)

    if result == -3:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Failed to push old default into the back of the array."
        })
    elif result == -2:
        response = jsonify({
            "statusCode": 400,
            "message": "Duplicate address, no need to insert."
        })
    elif result == -1:
        response = jsonify({
            "statusCode": 400,
            "message": "Customer does not exist."
        })
    elif result == 0:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not insert the new address."
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully added a shipping address."
        })
    else:
        response = jsonify({
            "statusCode":
            400,
            "message":
            "Unexpected with result = {}".format(result)
        })
    return response