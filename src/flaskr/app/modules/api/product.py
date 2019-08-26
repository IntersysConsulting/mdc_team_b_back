from flask import jsonify, request, make_response
from flask_restplus import Api, Resource, fields, Namespace
from ..resources.product import AdminProduct, UserProduct

any_ns = Namespace("products", description="APIs that work with products")
admin_ns = Namespace("admin/products", description="Admin APIs that work with products")

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
        Returns a filtered list of products
        """
        response = jsonify({"statusCode":200, "data":{"sort":sort, "filter":filter, "page":page}})
        return response 


@admin_ns.route('/')
@admin_ns.response(404, "Product not found")
@admin_ns.response(403, "User is not an admin")
class AdminProducts(Resource): 
    @admin_ns.response(201, 'Product succesfully created')
    def post(self): 
        return UserProduct.GetWithFilter() 

    @admin_ns.response(204, 'Product successfully updated')
    def put(self): 
        return 1 

    @admin_ns.response(204, 'Product sucessfully deleted')
    def delete(self): 
        return 1 