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
    'filter',
    help='A description of the filtering parameters to be used',
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


def Get(args):
    filter = " " if not args['filter'] else args['filter']
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']
    page_size = None if not args['page_size'] else args['page_size']
    up = UserProduct()

    productList = up.GetProducts(filter, sort, page=page, page_size=page_size)

    response = jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": productList,
        "count": len(productList)
    })
    return response