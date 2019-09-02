from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Customer's token",
                    required=True,
                    location="headers")
Parser.add_argument('sort',
                    type=int,
                    help='ID of the sorting method to be used',
                    required=False)
Parser.add_argument(
    'filter',
    help='A comma separated string of all the filters that apply',
    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)
#################
# Method        #
#################


def Get(args):
    token = args[
        'Authorization']  #sends auth token to get user id and then the orders
    filter = " " if not args['filter'] else args['filter']
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']

    response = jsonify({
        "statusCode": 200,
        'message': 'Success',
        "data": {
            "Auth": token,
            "sort": sort,
            "filter": filter,
            "page": page
        }
    })
    return response