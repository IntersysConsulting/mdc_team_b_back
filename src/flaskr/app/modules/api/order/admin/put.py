from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import AdminOrder
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('id',
                    type=int,
                    help='ID of the order to be updated',
                    required=True,
                    location='form')
Parser.add_argument('status',
                    help='Status name.',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Put(args):

    order_id = args['id']
    status = args['status']
    ao = AdminOrder()
    ao.get_all_orders()

    response = jsonify({
        "statusCode": 200,
        'message': 'Successfully updated updated'
    })
    return response