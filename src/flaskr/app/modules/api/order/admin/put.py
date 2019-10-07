from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import AdminOrder
from ....resources.validation import is_admin, is_not_admin_response
from ....resources import responses
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('id',
                    help='ID of the order to be updated',
                    required=True,
                    location='form')
Parser.add_argument('status',
                    help='Name of the status to be assigned to the order.',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Put(args, identity):
    if is_admin(identity):
        order_id = args['id']
        status = args['status']
        ao = AdminOrder()
        result = ao.change_order_status(order_id, status)
        if result == -3:
            response = responses.change_is_not_valid()
        elif result == -2:
            response = responses.element_does_not_exist("Order")
        elif result == -1:
            response = responses.element_does_not_exist("Status")
        elif result == 0:
            response = responses.operation_failed("Update status")
        elif result == 1:
            response = jsonify({
                "statusCode":
                200,
                'message':
                'Successfully updated the status of the order.'
            })
        else:
            response = responses.unexpected_result(result)
    else:
        response = is_not_admin_response
    # print("Response = {}".format(response))
    return response