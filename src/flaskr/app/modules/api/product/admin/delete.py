from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.product import AdminProduct
from ....resources.validation import is_admin, is_not_admin_response
from bson.errors import InvalidId
from ....resources import responses
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('id',
                    help='ID of the product to be deleted',
                    required=True)

#################
# Method        #
#################


def Delete(args, identity):
    pId = args['id']
    ap = AdminProduct()

    if not is_admin(identity):
        response = is_not_admin_response
    else:
        try:
            result = ap.delete_product(pId)

            if result == 1:
                response = responses.success("Deleted a product")
            elif result == -1:
                response = responses.element_does_not_exist("Product")
            elif result == 0:
                response = responses.operation_failed("Delete a product")
            else:
                response = responses.unexpected_result(result)

        except InvalidId:
            response = jsonify({
                "statusCode": 400,
                "message": "ID is not in valid format"
            })
    return response