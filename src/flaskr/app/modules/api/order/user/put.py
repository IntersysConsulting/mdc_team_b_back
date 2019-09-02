from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Customer's token",
                    required=True,
                    location="headers")
Parser.add_argument('user_billing',
                    help='User biling address JSON object',
                    required=True,
                    location='form')
Parser.add_argument('user_shipping',
                    help='User shipping address JSON object',
                    required=True,
                    location='form')
Parser.add_argument(
    'payment',
    help='User payment provider information. Depends on the provider',
    required=True,
    location='form')
#################
# Method        #
#################


def Put(args):
    token = args['Authorization']
    user_billing = args['user_billing']  #whole billing object
    user_shipping = args['user_shipping']  #whole shipping object
    payment = args['payment']  # Payment provider info
    timestamp = datetime.now()  # Time at which the order was finished on
    response = jsonify({
        "statusCode": 200,
        'message': 'Order succesfully added',
        "data": {
            "Auth": token,
            "items": items,
            "billing_id": user_billing,
            "shipping_id": user_shipping,
            "timestamp": timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        }
    })
    return response