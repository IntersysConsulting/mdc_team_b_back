from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help='Admin Auth token',
                    required=True,
                    location='headers')
Parser.add_argument('id',
                    type=int,
                    help='ID of the order to be updated',
                    required=True,
                    location='form')
Parser.add_argument('status',
                    type=int,
                    help='Status numerical identifier',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Put(args):
    token = args['Authorization']
    order_id = args['id']
    status = args['status']

    response = jsonify({
        "statusCode": 200,
        'message': 'Successfully updated updated',
        "data": {
            "Auth": token,
            "id": order_id,
            "status": status
        }
    })
    return response