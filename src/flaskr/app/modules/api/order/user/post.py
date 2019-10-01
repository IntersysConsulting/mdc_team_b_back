from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import UserOrder
#################
# Parser        #
#################
Parser = RequestParser()

#################
# Method        #
#################


def Post(args, identity):
    om = UserOrder()

    result = om.checkout_order(identity)

    if result == -2:
        response = jsonify({
            "statusCode":
            400,
            'message':
            'Customer already has an order in checkout. Delete this one before requesting another one.'
        })
    elif result == -1:
        response = jsonify({
            "statusCode":
            400,
            'message':
            'Customer does not have items on their cart.'
        })
    elif result == 0:
        response = jsonify({
            "statusCode": 400,
            'message': 'Order could not be added.'
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            'message': 'Order succesfully added.'
        })
    else:
        response = jsonify({
            "statusCode": 400,
            'message': 'Unexpected result = {}.'.format(result)
        })
    return response