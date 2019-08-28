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
from ..resources.product import AdminProduct, UserProduct
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage

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
any_ns = Namespace("products", description="APIs that work with products")
admin_ns = Namespace("admin/products",
                     description="Admin APIs that work with products")

# Customer Section

get_product_parser = any_ns.parser()
get_product_parser.add_argument('sort',
                                type=int,
                                help='ID of the Sorting method to be used',
                                required=False)
get_product_parser.add_argument(
    'filter',
    help='A description of the filtering parameters to be used',
    required=False)
get_product_parser.add_argument('page',
                                type=int,
                                help='Page the request is asking for',
                                required=False)


# This responds to www.servername.com:5000/namespace/
# In this case /products/
@any_ns.route("/")
class Product(Resource):
    @any_ns.expect(get_product_parser)
    def get(self):
        '''
        Returns a list of products. May be sorted, and filtered optionally.
        '''
        args = get_product_parser.parse_args()
        filter = " " if not args['filter'] else args['filter']
        sort = 0 if not args['sort'] else args['sort']
        page = 0 if not args['page'] else args['page']
        response = jsonify({
            "statusCode": 200,
            "data": {
                "sort": sort,
                "filter": filter,
                "page": page
            }
        })
        return response

    # Old way to do it, new one may be longer but works flawlessly with optional parameters while the old one fails to respond in swagger
    # @any_ns.route("/")
    # class Product(Resource):
    #     # This implemets the GET over the route
    #     def get(self):
    #         # This adds a description of the method to the documentation. Make it as descriptive as possible.
    #         """
    #         Returns a list of products
    #         """
    #         #To build a response we jsonify it
    #         response = jsonify({"statusCode":200})
    #         return response
    # # This responds to www.servername.com:5000/namespace/1/filter_sample/1
    # # This route accepts parameters which can be passed on to the GET
    # # In this case /Products/1/filter_sample/1
    # @any_ns.route("/<int:sort>/<string:filter>/<int:page>/")
    # class UserProducts(Resource):
    #     # This is how you document a parameter for get views / views that get parameters from route
    #     # All the parameters from routes are required.
    #     @any_ns.param('filter', 'A comma separated string of all the filters that apply')
    #     @any_ns.param('sort','The ID of the sorting method to be used.')
    #     @any_ns.param('page', 'The page requested (Default: 0)')
    #     # The parameters get passed on to the function like this. Name must match the <type:name>
    #     def get(self, sort, filter, page):
    #         """
    #         Returns a sorted and filtered list of products
    #         """
    #         # We reply with data in this case.
    #         response = jsonify({"statusCode":200, "data":{"sort":sort, "filter":filter, "page":page}})
    #         return response


# Admin Section

# This is how you document parameters in the body of a PUT (Update), POST (Add) and DELETE (Delete)
# We make a parser for every operation, and we describe each of them accordingly.
# You will usually only ask for ID on Delete, everything but ID on Create, and Delete+Create for Update

#Add product
product_add_parser = admin_ns.parser()
# location = 'form' Means it is expected in the data field of the HTTP request
product_add_parser.add_argument('name',
                                help='Name of the product to be added',
                                required=True,
                                location='form')
product_add_parser.add_argument(
    'price',
    help='Price in cents of the product to be added',
    required=True,
    location='form')
product_add_parser.add_argument('picture',
                                help='Picture of the product to be added',
                                type=FileStorage,
                                location='files',
                                required=True)
product_add_parser.add_argument('description',
                                help='Description of the product to be added',
                                required=False,
                                location='form')  # Some fields can be optional

#Update product
product_update_parser = admin_ns.parser()
product_update_parser.add_argument('id',
                                   type=int,
                                   help='ID of the product to be updated',
                                   required=True,
                                   location='form')
product_update_parser.add_argument('name',
                                   help='Name of the product to be updated',
                                   required=True,
                                   location='form')
product_update_parser.add_argument(
    'price',
    help='Price in cents of the product to be updated',
    required=True,
    location='form')
product_update_parser.add_argument('picture',
                                   help='Picture of the product to be updated',
                                   type=FileStorage,
                                   location='files',
                                   required=True)
product_update_parser.add_argument(
    'description',
    help='Description of the product to be updated',
    required=False,
    location='form')

#Delete product
product_delete_parser = admin_ns.parser()
product_delete_parser.add_argument('id',
                                   type=int,
                                   help='ID of the product to be deleted',
                                   required=True,
                                   location='form')


# This responds to website:5000/admin/products/, it uses a different namespace (admin_ns, not any_ns)
@admin_ns.route('/')
# This is how you document a general response for ALL the options in an endpoint, 404 and 403 for example.
@admin_ns.response(404, "Product not found")
@admin_ns.response(403, "User is not an admin")
class AdminProducts(Resource):
    # This is how you document a per-action response, in this case, this is exclusive to the POST method
    @admin_ns.response(201, 'Product succesfully created')
    # This is how you make the endpoint expect something in the DATA field of the message.
    # You give it the parser corresponding to the action.
    @admin_ns.expect(product_add_parser)
    def post(self):
        '''
        Adds a product to the database
        '''
        # To get the parameters from the DATA of the message we access them like this
        args = product_add_parser.parse_args()
        # They are put into a python dictionary, we can access them like this.
        name = args['name']
        price = args['price']
        picture = args['picture']
        # Manage optional fields like this. This is an inline optional assignation
        #              True value            IF    condition    ELSE       False value
        description = 'No description' if not args['description'] else args[
            'description']  #Do this for optional fields

        picture.save(picture.filename)

        response = jsonify({
            "statusCode": 200,
            "data": {
                "name": name,
                "price": price,
                "picture": picture.filename,
                "description": description
            }
        })
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
        description = 'No description' if not args['description'] else args[
            'description']  #Do this for optional fields

        picture.save(picture.filename)

        response = jsonify({
            "statusCode": 200,
            "data": {
                "id": pId,
                "name": name,
                "price": price,
                "picture": picture.filename,
                "description": description
            }
        })
        return response

    @admin_ns.response(204, 'Product sucessfully deleted')
    @admin_ns.expect(product_delete_parser)
    def delete(self):
        '''
        Deletes a product from the database
        '''
        args = product_delete_parser.parse_args()
        pId = args['id']

        response = jsonify({"statusCode": 200, "data": {"id": pId}})
        return response
