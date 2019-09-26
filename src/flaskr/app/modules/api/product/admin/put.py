from flask import jsonify
from flask_restplus.namespace import RequestParser
from werkzeug.datastructures import FileStorage
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
                    help='ID of the product to be updated',
                    required=True,
                    location='form')
Parser.add_argument(
    'name',
    help='Name of the product to be updated. If blank will use previous.',
    required=False,
    location='form')
Parser.add_argument(
    'price',
    help=
    'Price in cents of the product to be updated. If blank will use previous.',
    required=False,
    location='form')
Parser.add_argument(
    'picture',
    help='Picture of the product to be updated. If blank will use previous.',
    type=FileStorage,
    location='files',
    required=False)
Parser.add_argument('digital',
                    help='Whether or not the product is digital',
                    type=bool,
                    required=False,
                    location='form')
Parser.add_argument('description',
                    help='Description of the product to be updated',
                    required=False,
                    location='form')

#################
# Method        #
#################


def Put(args):
    pId = args['id']
    name = None if not args['name'] else args['name']
    price = None if not args['price'] else args['price']
    picture = None if not args['picture'] else args['picture']
    description = 'No description' if not args['description'] else args[
        'description']  #Do this for optional fields
    digital = None if not args['digital'] else args['digital']

    picture_name = None
    if picture != None:
        picture.save(picture.filename)
        picture_name = picture.filename

    ap = AdminProduct()
    result = ap.update_product(pId,
                               name,
                               price,
                               picture_name,
                               digital,
                               description=description)

    if result > 0:
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully updated a product",
        })
    else:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not update the specified product",
        })
    return response