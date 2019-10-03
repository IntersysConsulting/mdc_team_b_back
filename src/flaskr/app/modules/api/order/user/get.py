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
    help='A comma separated string of all the filters that apply (NYI)',
    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
#################
# Method        #
#################


def Get(args, identity):
    filter = " " if not args['filter'] else args['filter']
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']

    uo = UserOrder()
    result = uo.get_user_orders(identity, filter, sort, page=page)
    print("Result = {}".format(result))

    response = jsonify({
        "statusCode": 200,
        'message': 'Success',
        "data": result
    })
    return response