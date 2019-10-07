from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import AdminOrder
from ....resources.validation import is_admin, is_not_admin_response
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('sort',
                    type=int,
                    help='ID of the sorting method to be used',
                    required=False)
Parser.add_argument(
    'filter',
    help=
    'A comma separated string of all the status names that we are excluding. Capitalizes the first letter of each word.',
    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
Parser.add_argument('page_size',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
#################
# Method        #
#################


def Get(args, identity):

    filter = "" if not args['filter'] else args["filter"]
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']
    page_size = args['page_size']

    if is_admin(identity):
        ao = AdminOrder()
        orders, total = ao.get_all_orders(filter, sort, page, page_size)

        response = jsonify({
            "statusCode": 200,
            'message': 'Success',
            'data': orders,
            'count': len(orders),
            'total': total
        })
    else:
        response = is_not_admin_response
    return response