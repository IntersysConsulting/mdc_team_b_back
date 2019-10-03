# Import description
# jsonify: Allows us to make json responses for HTTP
from flask import jsonify
# Resource: Implements REST Resource. All EndPoints should be done within classes that inherit from Resource
# fields:   Access to field-types
# Namespace:Creates namespaces for our routes. You should have at least two:
#   any_ns   = /collection_name         | Implements public methods that are accessible without admin privileges (Most GETs)
#   admin_ns = /admin/collection_name   | Implements methods that NEED admin privileges (Most POST, PUT, and DELETEs)
from flask_restplus import Resource, fields, Namespace
# This is for actual back end functionality, don't worry about it for documentation
# Should be from ..resources.collection import AdminCollection, UserCollection
from ...resources.product import AdminProduct, UserProduct
from werkzeug.datastructures import FileStorage
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage
from .user.get import Get as UserGet, Parser as get_product_parser
from .admin.post import Post as AdminPost, Parser as product_add_parser
from .admin.put import Put as AdminPut, Parser as product_update_parser
from .admin.delete import Delete as AdminDelete, Parser as product_delete_parser
from flask_jwt_extended import (get_jwt_identity, jwt_required)
# For the documentation of the endpoints make the response replicate the data received
# Implement two Namespaces per class, it will let us migrate to microservice if we decide on it
# After you are done implementing your file add some lines to __init__.py

# Want to see it in action?
# After putting your namespaces in the __init__ ...
# Run: src/flaskr/app/run.py then use your browser to go to http://localhost:5000/ (Ctrl+click on vscode)
# You may need to do pip install -r requirements.txt at the root of the project

# This file will be heavily documented, don't worry about it on your own.

# This makes the API respond to www.servername.com:5000/namespace
# It will help with the endpoints. Trust me.
any_ns = Namespace(
    "products", description="Endpoints that give information about products")
admin_ns = Namespace(
    "admin/products",
    description="Endpoints that allow admins to manage products")

#########################################################
#   User section
#########################################################


# This responds to www.servername.com:5000/namespace/
# In this case /products/
@any_ns.route("/")
class Product(Resource):
    @any_ns.expect(get_product_parser)
    def get(self):
        '''
        √ Returns a list of products. May be sorted, and filtered optionally.
        '''
        args = get_product_parser.parse_args()

        return UserGet(args)


#########################################################
#   Admin section
#########################################################


# This responds to website:5000/admin/products/, it uses a different namespace (admin_ns, not any_ns)
@admin_ns.route('/')
# This is how you document a general response for ALL the options in an endpoint, 404 and 403 for example.
@admin_ns.response(404, "Product not found")
@admin_ns.response(403, "User is not an admin")
class AdminProducts(Resource):
    # This is how you document a per-action response, in this case, this is exclusive to the POST method
    @admin_ns.response(200, 'Product succesfully created')
    # This is how you make the endpoint expect something in the DATA field of the message.
    # You give it the parser corresponding to the action.
    @admin_ns.expect(product_add_parser)
    @jwt_required
    def post(self):
        '''
        √ Adds a product to the database
        '''
        # To get the parameters from the DATA of the message we access them like this
        identity = get_jwt_identity()
        args = product_add_parser.parse_args()

        return AdminPost(args, identity)

    @admin_ns.response(200, 'Product successfully updated')
    @admin_ns.expect(product_update_parser)
    @jwt_required
    def put(self):
        '''
        √ Updates a product on the database
        '''
        identity = get_jwt_identity()
        args = product_update_parser.parse_args()

        return AdminPut(args, identity)

    @admin_ns.response(200, 'Product sucessfully deleted')
    @admin_ns.expect(product_delete_parser)
    @jwt_required
    def delete(self):
        '''
        √ Deletes a product from the database
        '''
        identity = get_jwt_identity()
        args = product_delete_parser.parse_args()

        return AdminDelete(args, identity)
