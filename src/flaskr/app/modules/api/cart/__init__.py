from flask_restplus import Resource, Namespace
#from ..resources.cart import UserCart # Not yet implemented
# from werkzeug.datastructures import FileStorage  # Only import if needs files
from .get import Get, Parser as get_cart_parser
from .post import Post, Parser as add_item_parser
from .put import Put, Parser as update_item_parser
from .delete import Delete, Parser as delete_item_parser

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
    def get(self):
        '''
        Returns the user's cart based on their JWT token.
        '''
        args = get_cart_parser.parse_args()
        return Get(args)


################################### End Route


@any_ns.route("/update/")
@any_ns.response(401, "Invalid or missing credentials")
@any_ns.response(400, "Product ID does not exist")
class UpdateCart(Resource):
    #############
    # POST
    #############
    @any_ns.response(200, "Product successfully added to the cart")
    @any_ns.expect(add_item_parser)
    def post(self):
        '''
        Adds a new item to the user's cart (Item must not exist in the cart)
        If the item already exists in the cart this responds with a message that states No changes. 
        '''
        args = add_item_parser.parse_args()
        return Post(args)

    #############
    # PUT
    #############
    @any_ns.response(
        406,
        "The new quantity for the product is less than 1. Did you mean to use DELETE?"
    )
    @any_ns.response(200, "Product quantity successfully updated")
    @any_ns.expect(update_item_parser)
    def put(self):
        '''
        Updates quantity on an item that is already in the user's cart (New quantity must be greater than 1)
        '''
        args = update_item_parser.parse_args()
        return Put(args)

    #############
    # DELETE
    #############
    @any_ns.response(204, "Product was not in the cart")
    @any_ns.response(200, "Product was deleted successfully from the cart")
    @any_ns.expect(delete_item_parser)
    def delete(self):
        '''
        Removes an item from the user's cart 
        '''
        args = delete_item_parser.parse_args()
        return Delete(args)


################################### End Route