from flask import jsonify
from flask_restplus.namespace import RequestParser
from werkzeug.datastructures import FileStorage

#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument('Authorization',
                    help="Admin's token",
                    required=True,
                    location="headers")
Parser.add_argument('id',
                    type=int,
                    help='ID of the product to be updated',
                    required=True,
                    location='form')
Parser.add_argument('name',
                    help='Name of the product to be updated',
                    required=True,
                    location='form')
Parser.add_argument('price',
                    help='Price in cents of the product to be updated',
                    required=True,
                    location='form')
Parser.add_argument('picture',
                    help='Picture of the product to be updated',
                    type=FileStorage,
                    location='files',
                    required=True)
Parser.add_argument('description',
                    help='Description of the product to be updated',
                    required=False,
                    location='form')

#################
# Method        #
#################


def Put(args):
    pId = args['id']
    name = args['name']
    price = args['price']
    picture = args['picture']
    description = 'No description' if not args['description'] else args[
        'description']  #Do this for optional fields

    picture.save(picture.filename)

    response = jsonify({
        "statusCode": 200,
        "message": "Successfully updated a product",
        "data": {
            "id": pId,
            "name": name,
            "price": price,
            "picture": picture.filename,
            "description": description
        }
    })
    return response