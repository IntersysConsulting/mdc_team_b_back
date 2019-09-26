from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.product import AdminProduct
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Admin's token",
                    required=True,
                    location="headers")
Parser.add_argument('id',
                    help='ID of the product to be deleted',
                    required=True,
                    location='form')

#################
# Method        #
#################


def Delete(args):
    pId = args['id']
    ap = AdminProduct()

    result = ap.delete_product(pId)

    if (result > 0):
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully deleted a product",
        })
    elif (result < 0):
        response = jsonify({"statusCode": 400, "message": "Item not found"})
    else:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not delete the specified product",
        })
    return response