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


def Delete(args, identity):
    uo = UserOrder()
    result = uo.cancel_checkout(identity)
    if result == -1:
        response = jsonify({
            "statusCode": 400,
            'message': 'Could not delete the order.'
        })
    elif result == 0:
        response = jsonify({"statusCode": 204, 'message': 'No changes.'})
    elif result == 1:
        response = jsonify({
            "statusCode":
            200,
            'message':
            'Successfully deleted the in-checkout order.'
        })
    else:
        response = jsonify({
            "statusCode":
            500,
            'message':
            'Unexpected error with result={}'.format(result)
        })

    return response