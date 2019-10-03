from flask_restplus import Resource, Namespace
#from ..resources.cart import UserCart # Not yet implemented
# from werkzeug.datastructures import FileStorage  # Only import if needs files
from .get import Get, Parser as get_cart_parser
from .put import Put, Parser as update_item_parser
from .delete import Delete, Parser as delete_item_parser
from flask_jwt_extended import (get_jwt_identity, jwt_required)
any_ns = Namespace(
    "carts",
    description=
    "Endpoints that allow users to interact with their carts based on their session token."
)

###################################
# Customer Section
###################################


@any_ns.route("/")
@any_ns.response(401, "Invalid or missing credentials")
class Cart(Resource):
    #############
    # GET
    #############
    @any_ns.response(200, "Cart was found")
    @any_ns.expect(get_cart_parser)
    @jwt_required
    def get(self):
        '''
        √ Returns the user's cart based on their JWT token.
        '''
        identity = get_jwt_identity()
        args = get_cart_parser.parse_args()
        return Get(args, identity)

    #############
    # PUT
    #############
    @any_ns.response(
        406,
        "The new quantity for the product is less than 1. Did you mean to use DELETE?"
    )
    @any_ns.response(200, "Product quantity successfully updated")
    @any_ns.response(400, "Product ID does not exist")
    @any_ns.expect(update_item_parser)
    @jwt_required
    def put(self):
        '''
        √  Creates a user's cart if they don't have one, and changes the amount of items a user has of an item.
        '''
        identity = get_jwt_identity()
        args = update_item_parser.parse_args()
        return Put(args, identity)

    #############
    # DELETE
    #############
    @any_ns.response(204, "Product was not in the cart")
    @any_ns.response(200, "Product was deleted successfully from the cart")
    @any_ns.response(400, "Product ID does not exist")
    @any_ns.expect(delete_item_parser)
    @jwt_required
    def delete(self):
        '''
        NYI Removes an item from the user's cart 
        '''
        identity = get_jwt_identity()
        args = delete_item_parser.parse_args()
        return Delete(args, identity)


################################### End Route
