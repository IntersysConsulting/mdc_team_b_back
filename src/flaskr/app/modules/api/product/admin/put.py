from flask import jsonify
from flask_restplus.namespace import RequestParser
from flask_restplus import inputs
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
    'image',
    help='Image of the product to be updated. If blank will use previous.',
    type=FileStorage,
    location='files',
    required=False)
Parser.add_argument('digital',
                    help='Whether or not the product is digital',
                    type=inputs.boolean,
                    required=False,
                    location='form')
Parser.add_argument('description',
                    help='Description of the product to be updated',
                    required=False,
                    location='form')

#################
# Method        #
#################


def Put(args, identity):
    pId = args['id']
    name = args['name']
    price = args['price']
    image = args['image']
    description = args['description']
    digital = args['digital']
    image_name = None

    if not is_admin(identity):
        response = jsonify(is_not_admin_response)
    else:
        if image != None:
            upload_result = upload_image(image)
            image_name = upload_result["link"] if upload_result[
                'status'] == 200 else None
        else:
            image_name = None

        ap = AdminProduct()
        result = ap.update_product(pId,
                                   name,
                                   price,
                                   image_name,
                                   digital,
                                   description=description)

        if result == 1:
            if image is None or (image is not None and image_name is not None):
                response = responses.success("Update product")
            else:
                response = responses.partial_success("Update product",
                                                     "Upload image")
        elif result == 0:
            response = responses.operation_failed("Update product")
        else:
            response = responses.unexpected_result(result)
    return response
