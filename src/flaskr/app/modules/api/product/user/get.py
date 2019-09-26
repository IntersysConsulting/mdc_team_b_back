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
#################
# Method        #
#################


def Get(args):
    filter = " " if not args['filter'] else args['filter']
    # int x = isTrue?5:2
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']
    up = UserProduct()

    productList = up.GetProducts(filter, sort)

    response = jsonify({
        "statusCode": 200,
        "message": "Success",
        "bears": True,
        "data": productList
    })
    return response