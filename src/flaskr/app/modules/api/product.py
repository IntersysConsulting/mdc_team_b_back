from flask import jsonify, request, make_response
from flask_restplus import Api, Resource, fields, Namespace
from ..resources.product import AdminProduct, UserProduct
from werkzeug.datastructures import FileStorage

# For the documentation of the endpoints make the response replicate the data received
# Implement two Namespaces per class, it will let us migrate to microservice if we decide on it
# After you are done implementing your file add some lines to __init__.py

any_ns = Namespace("products", description="APIs that work with products")
admin_ns = Namespace("admin/products", description="Admin APIs that work with products")

# Customer Section

@any_ns.route("/")
class Product(Resource):     
    def get(self): 
        """
        Returns a list of products
        """
        response = jsonify({"statusCode":200})
        return response 

@any_ns.route("/<int:sort>/<string:filter>/<int:page>")
class UserProducts(Resource): 
    @any_ns.param('fiter', 'A comma separated string of all the filters that apply')
    @any_ns.param('sort','The ID of the sorting method to be used.')
    @any_ns.param('page', 'The page requested (Default: 0)')
    def get(self, sort, filter, page): 
        """
        Returns a sorted and filtered list of products
        """
        response = jsonify({"statusCode":200, "data":{"sort":sort, "filter":filter, "page":page}})
        return response 


# Admin Section

product_add_parser = admin_ns.parser()
product_add_parser.add_argument('name', help='Name of the product to be added', required=True)
product_add_parser.add_argument('price', help='Price in cents of the product to be added', required=True)
product_add_parser.add_argument('picture', help='Picture of the product to be added', type=FileStorage, location='files', required=True)
product_add_parser.add_argument('description', help='Description of the product to be added', required=False)

product_update_parser = admin_ns.parser()
product_update_parser.add_argument('id', type=int, help='ID of the product to be updated', required=True)
product_update_parser.add_argument('name', help='Name of the product to be updated', required=True)
product_update_parser.add_argument('price', help='Price in cents of the product to be updated', required=True)
product_update_parser.add_argument('picture', help='Picture of the product to be updated', type=FileStorage, location='files', required=True)
product_update_parser.add_argument('description', help='Description of the product to be updated', required=False)

product_delete_parser = admin_ns.parser()
product_delete_parser.add_argument('id', type=int, help='ID of the product to be deleted', required=True)

@admin_ns.route('/')
@admin_ns.response(404, "Product not found")
@admin_ns.response(403, "User is not an admin")
class AdminProducts(Resource): 
    @admin_ns.response(201, 'Product succesfully created')
    @admin_ns.expect(product_add_parser)
    def post(self): 
        '''
        Adds a product to the database
        '''
        args = product_add_parser.parse_args()
        name = args['name']
        price = args['price']
        picture = args['picture']
        description = 'No description' if not args['description'] else args['description'] #Do this for optional fields

        response = jsonify({"statusCode":200, "data":{"name":name, "price":price, "picture":picture.filename, "description":description}})
        return response 

    @admin_ns.response(204, 'Product successfully updated')
    @admin_ns.expect(product_update_parser)
    def put(self): 
        '''
        Updates a product on the database
        '''
        args = product_update_parser.parse_args()
        pId = args['id']
        name = args['name']
        price = args['price']
        picture = args['picture']
        description = 'No description' if not args['description'] else args['description'] #Do this for optional fields
        
        response = jsonify({"statusCode":200, "data":{"id":pId, "name":name, "price":price, "picture":picture.filename, "description":description}})
        return response 

    @admin_ns.response(204, 'Product sucessfully deleted')
    @admin_ns.expect(product_delete_parser)
    def delete(self): 
        '''
        Deletes a product from the database
        '''
        args = product_delete_parser.parse_args()
        pId = args['id']
        
        response = jsonify({"statusCode":200, "data":{"id":pId}})
        return response 