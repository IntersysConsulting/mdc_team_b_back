from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.order import UserOrder
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('sort',
                    type=int,
                    help='ID of the sorting method to be used (NYI)',
                    required=False)
Parser.add_argument(
    'filter',
    help=
    'Comma separated string of all filters that apply. If left blank it will give every order. Otherwise it will be an inclusive filter. Only giving out the statuses that are in the filter.',
    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
#################
# Method        #
#################


def Get(args, identity):
    filter = args['filter']
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']

    uo = UserOrder()
    result = uo.get_user_orders(identity, filter, sort, page=page)

    response = jsonify({
        "statusCode": 200,
        'message': 'Success',
        "data": result
    })
    return response