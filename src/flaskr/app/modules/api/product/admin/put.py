from flask import jsonify
from flask_restplus.namespace import RequestParser
from werkzeug.datastructures import FileStorage
from ....resources.product import AdminProduct
from ....resources.validation import is_admin, is_not_admin_response
from ....resources.images import upload_image
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


def Put(args, identity):
    pId = args['id']
    name = None if not args['name'] else args['name']
    price = None if not args['price'] else args['price']
    picture = None if not args['picture'] else args['picture']
    description = None if not args['description'] else args[
        'description']  #Do this for optional fields
    digital = None if not args['digital'] else args['digital']
    image_name = None

    if not is_admin(identity):
        response = jsonify(is_not_admin_response)
    else:
        if picture != None:
            tmpDir = tempfile.TemporaryDirectory()
            image_dir = "{}\\{}".format(tmpDir.name, picture.filename)
            print("Saving the picture in {}".format(image_dir))
            picture.save(image_dir)
            image_result = upload_image(image_dir)
            print("Image result was: {}".format(image_result))
            image_name = image_result["link"]
            tmpDir.cleanup()

        ap = AdminProduct()
        result = ap.update_product(pId,
                                   name,
                                   price,
                                   image_name,
                                   digital,
                                   description=description)

        if result > 0:
            if image_result['status'] == 200:
                response = jsonify({
                    "statusCode": 200,
                    "message": "Successfully updated a product",
                })
            else:
                response = jsonify({
                    "statusCode":
                    206,
                    "message":
                    "Successfully updated a product, but the image could not be updated.",
                })
        else:
            response = jsonify({
                "statusCode":
                400,
                "message":
                "Could not update the specified product",
            })
    return response