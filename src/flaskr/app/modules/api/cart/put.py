from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.cart import CartManager

#################
# Parser        #
#################

Parser = RequestParser()
Parser.add_argument('product_id',
                    help="The ObjectID of the product to be affected.",
                    required=True)
Parser.add_argument(
    'quantity',
    type=int,
    help="The new quantity of the product. Must be greater than 0.",
    required=True)

#################
# Method        #
#################


def Put(args, identity):
    product_id = args['product_id']
    quantity = args['quantity']
    customer_id = identity


    if quantity < 0:
        response = jsonify({
            "statusCode": 406,
            "message":"Can't accept negative products."
        })
    else:
        cm = CartManager()
        result = cm.put_in_cart(customer_id, product_id, quantity)

        if result == 0:
            response = jsonify({
                "statusCode": 400,
                "message": "Could not update for some reason."
            })
        elif result==1:
            response = jsonify({
                "statusCode": 200,
                "message": "Successfully updated the product."
            })
        else:
            response = jsonify({
                "statusCode": 400,
                "message": "Unknown error with result = {}.".format(result)
            })

    return response