from flask import jsonify
from flask_restplus.namespace import RequestParser
from werkzeug.datastructures import FileStorage
from ....resources.product import AdminProduct

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('name',
                    help='Name of the product to be added',
                    required=True,
                    location='form')
Parser.add_argument('price',
                    help='Price in cents of the product to be added',
                    required=True,
                    location='form')
Parser.add_argument('picture',
                    help='Picture of the product to be added',
                    type=FileStorage,
                    location='files',
                    required=True)
Parser.add_argument('digital',
                    help="Whether the product is a digital product or not",
                    type=bool,
                    location='form')
Parser.add_argument('description',
                    help='Description of the product to be added',
                    required=False,
                    location='form')  # Some fields can be optional

#################
# Method        #
#################


def Post(args):
    # They are put into a python dictionary, we can access them like this.
    name = args['name']
    price = args['price']
    picture = args['picture']
    digital = args['digital']
    # Manage optional fields like this. This is an inline optional assignation
    #              True value            IF    condition    ELSE       False value
    description = 'No description' if not args['description'] else args[
        'description']  #Do this for optional fields

    picture.save(picture.filename)

    ap = AdminProduct()
    success = ap.create_product(name,
                                price,
                                picture.filename,
                                digital,
                                description=description).acknowledged

    if (success):
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully created a product",
        })
    else:
        response = jsonify({
            "statusCode": 400,
            "message": "There was an error creating a product",
        })
    return response