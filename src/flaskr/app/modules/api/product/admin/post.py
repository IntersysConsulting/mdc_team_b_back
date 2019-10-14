from flask import jsonify
from flask_restplus.namespace import RequestParser
from werkzeug.datastructures import FileStorage
from ....resources.product import AdminProduct
from ....resources.validation import is_admin, is_not_admin_response
from ....resources.images import upload_image
from ....resources import responses
import tempfile
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
                    type=int,
                    required=True,
                    location='form')
Parser.add_argument('image',
                    help='Picture of the product to be added',
                    type=FileStorage,
                    location='files',
                    required=False)
Parser.add_argument('digital',
                    help="Whether the product is a digital product or not",
                    type=bool,
                    required=True,
                    location='form')
Parser.add_argument('description',
                    help='Description of the product to be added',
                    required=False,
                    location='form')  # Some fields can be optional

#################
# Method        #
#################

placeholder_image = "https://i.imgur.com/JelTlmk.png"


def Post(args, identity):
    # They are put into a python dictionary, we can access them like this.
    name = args['name']
    price = args['price']
    image = args['image']
    digital = args['digital']
    # Manage optional fields like this. This is an inline optional assignation
    #              True value            IF    condition    ELSE       False value
    description = 'No description' if not args['description'] else args[
        'description']  #Do this for optional fields

    if not is_admin(identity):
        response = jsonify(is_not_admin_response)
    else:
        if image is None:
            image_name = placeholder_image
        else:
            upload_result = upload_image(image)
            image_name = upload_result["link"] if upload_result[
                'status'] == 200 else placeholder_image

        ap = AdminProduct()
        result = ap.create_product(name,
                                   price,
                                   image_name,
                                   digital,
                                   description=description).acknowledged

        if result == 1:
            if image_name is not "":
                response = responses.success("Create new product")
            else:
                response = responses.partial_success("Create new product",
                                                     "Upload image")
        elif result == 0:
            response = responses.operation_failed("Create new product")
        else:
            response = responses.unexpected_result(result)
    return response