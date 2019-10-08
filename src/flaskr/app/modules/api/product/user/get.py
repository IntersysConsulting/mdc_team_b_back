from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.product import UserProduct

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('sort',
                    type=int,
                    help='ID of the Sorting method to be used',
                    required=False)
Parser.add_argument(
    'search_name',
    help='A description of the filtering parameters to be used',
    required=False)
Parser.add_argument(
    'digital_filtering',
    type=int,
    help=
    'If value is: -1, results will exclude digital products. 1, results will exclude physical products. 0, results will include everything.',
    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
Parser.add_argument('page_size',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
Parser.add_argument(
    'product_id',
    help=
    'Overrides every other parameter. Turns the request into a specific search that returns 1 item.',
    required=False)
#################
# Method        #
#################


def Get(args):
    search_name = args['search_name']
    digital_filtering = 0 if not args['digital_filtering'] else args[
        'digital_filtering ']
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']
    page_size = None if not args['page_size'] else args['page_size']
    product_id = None if not args['product_id'] else args['product_id']
    up = UserProduct()

    if product_id != None:
        productList, total = up.get_one(product_id), 1
    else:
        productList, total = up.get_products(search_name,
                                             digital_filtering,
                                             sort,
                                             page=page,
                                             page_size=page_size)

    response = jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": productList,
        "count": len(productList),
        "total": total
    })
    return response