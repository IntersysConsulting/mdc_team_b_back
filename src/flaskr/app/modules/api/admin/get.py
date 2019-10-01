from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.validation import is_admin, is_not_admin_response
#################
# Parser        #
#################
Parser = RequestParser()
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


def Get(args, identity):
    if not is_admin(identity):
        response = is_not_admin_response
    else:
        pass
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