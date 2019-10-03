from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import UserOrder
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument(
    'user_billing',
    help="Index in the array of the user's billing addresses to be used.",
    required=True,
    type=int,
    location='form')
Parser.add_argument(
    'user_shipping',
    help="Index in the array of the user's billing addresses to be used.",
    required=True,
    type=int,
    location='form')
Parser.add_argument(
    'payment',
    help='User payment provider information. Depends on the provider',
    required=True,
    location='form')
#################
# Method        #
#################


def Put(args, identity):

    user_billing_id = args['user_billing']  #whole billing object
    user_shipping_id = args['user_shipping']  #whole shipping object
    payment = args['payment']  # Payment provider info

    uo = UserOrder()
    result = uo.finish_order(identity, user_shipping_id, user_billing_id,
                             payment)

    if result == -1:
        response = jsonify({
            "statusCode": 400,
            'message': 'Customer does not have a POSTed order'
        })
    elif result == 0:
        response = jsonify({
            "statusCode": 400,
            'message': 'Could not update order'
        })
    elif result == 1:
        response = jsonify({
            "statusCode": 200,
            'message': 'Order succesfully updated'
        })
    else:
        response = jsonify({
            "statusCode": 400,
            'message': 'Unexpected result={}'.format(result)
        })
    return response
