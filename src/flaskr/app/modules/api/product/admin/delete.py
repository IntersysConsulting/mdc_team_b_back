from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.product import AdminProduct
from ....resources.validation import is_admin, is_not_admin_response
from bson.errors import InvalidId
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('id',
                    help='ID of the product to be deleted',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Delete(args, identity):
    pId = args['id']
    ap = AdminProduct()

    if not is_admin(identity):
        response = jsonify(is_not_admin_response)
    else:
        try:
            result = ap.delete_product(pId)

            if (result > 0):
                response = jsonify({
                    "statusCode": 200,
                    "message": "Successfully deleted a product",
                })
            elif (result < 0):
                response = jsonify({
                    "statusCode": 400,
                    "message": "Item not found"
                })
            else:
                response = jsonify({
                    "statusCode":
                    400,
                    "message":
                    "Could not delete the specified product",
                })
        except InvalidId:
            response = jsonify({
                "statusCode": 400,
                "message": "ID is not in valid format"
            })
    return response