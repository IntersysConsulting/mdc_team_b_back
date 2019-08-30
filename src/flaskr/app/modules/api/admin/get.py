from flask import jsonify
from flask_restplus.namespace import RequestParser

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('Authorization',
                    help="Admin's session token",
                    required=True)
Parser.add_argument('sort',
                    type=int,
                    help='ID of the Sorting method to be used',
                    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for',
                    required=False)

#################
# Method        #
#################


def Get(args):
    sort = 0 if not args['sort'] else args['sort']
    page = 0 if not args['page'] else args['page']
    response = jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": {
            "sort": sort,
            "page": page
        }
    })
    return response