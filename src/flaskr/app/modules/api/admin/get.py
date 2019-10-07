from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.validation import is_admin, is_not_admin_response
from ...resources.admin import AdminManagement
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('sort',
                    type=int,
                    help='NYI ID of the Sorting method to be used.',
                    required=False)
Parser.add_argument('page',
                    type=int,
                    help='Page the request is asking for.',
                    required=False)
Parser.add_argument('page_size',
                    type=int,
                    help='Elements to be displayed by page. Server has a default.',
                    required=False)
Parser.add_argument(
    'search_field',
    help=
    'Field in which we are looking. Expects: "Email" or "Name". Name looks up both First name and Last name.',
    required=False)
Parser.add_argument(
    'search_value',
    help=
    'Value that is being asked for. Name or Email value. Must not be blank if search_field is in the query.',
    required=False)

#################
# Method        #
#################


def Get(args, identity):
    if not is_admin(identity):
        response = is_not_admin_response
    else:
        sort = 0 if not args['sort'] else args['sort']
        page = 0 if not args['page'] else args['page']
        page_size = args['page_size']
        search_field = args['search_field']
        search_value = args['search_value']

        am = AdminManagement()
        data, total = am.get_all_admins(sort, page, page_size, search_field, search_value)
        if data == -1:
            response = jsonify({
                "statusCode": 400,
                "message": "Wrong parameter in search_field."
            })
        else:
            response = jsonify({
                "statusCode": 200,
                "message": "Success",
                "data": data,
                "total": total,
                "count": len(data)
            })

    return response