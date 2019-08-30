from flask import jsonify
from flask_restplus import Resource, fields, Namespace
#from ..resources.cart import UserCart # Not yet implemented
from werkzeug.datastructures import FileStorage

any_ns = Namespace(
    "carts",
    description=
    "Endpoints that allow users to interact with their carts based on their session token."
)

# Customer Section

get_cart_parser = any_ns.parser()
get_cart_parser.add_argument(
    'Authorization',
    help=
    "The autorization token bearer. This is a placeholder and should be handled with JWT.",
    required=True,
    location="headers")


# This responds to www.servername.com:5000/carts/
@any_ns.route("/")
@any_ns.response(401, "Invalid or missing credentials")
class Cart(Resource):
    @any_ns.response(200, "Cart was found")
    @any_ns.expect(get_cart_parser)
    #To be defined
    def get(self):
        '''
        Returns the user's cart based on their JWT token.
        '''
        args = get_cart_parser.parse_args()
        token = args['Authorization']

        return jsonify({
            "statusCode": 200,
            "message": "OK",
            "data": {
                "Auth": token
            }
        })


add_remove_item_parser = any_ns.parser()

add_remove_item_parser.add_argument(
    'Authorization',
    help=
    "The autorization token bearer. This is a placeholder and should be handled with JWT.",
    required=True,
    location="headers")
add_remove_item_parser.add_argument(
    'product_id',
    help="The ObjectID of the product to be affected.",
    required=True)

update_item_parser = any_ns.parser()
update_item_parser.add_argument(
    'Authorization',
    help=
    "The autorization token bearer. This is a placeholder and should be handled with JWT.",
    required=True,
    location="headers")
update_item_parser.add_argument(
    'product_id',
    help="The ObjectID of the product to be affected.",
    required=True)
update_item_parser.add_argument(
    'quantity',
    type=int,
    help="The new quantity of the product. Must be greater than 0.",
    required=True)


@any_ns.route("/update/")
@any_ns.response(401, "Invalid or missing credentials")
@any_ns.response(400, "Product ID does not exist")
class UCart(Resource):
    @any_ns.response(200, "Product successfully added to the cart")
    @any_ns.expect(add_remove_item_parser)
    def post(self):
        '''
        Adds a new item to the user's cart (Item must not exist in the cart)
        If the item already exists in the cart this responds with a message that states No changes. 
        '''
        args = add_remove_item_parser.parse_args()
        token = args['Authorization']
        pid = args['product_id']

        return jsonify({
            "statusCode": 200,
            "message": "No changes",
            "data": {
                "Auth": token,
                "product_id": pid
            }
        })

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
        token = args['Authorization']
        pid = args['product_id']
        quantity = args['quantity']

        code = 200 if quantity > 0 else 406
        msg = "OK" if quantity > 0 else "Less than 1"
        return jsonify({
            "statusCode": code,
            "data": {
                "Auth": token,
                "product_id": pid,
                "quantity": quantity
            }
        })

    @any_ns.response(204, "Product was not in the cart")
    @any_ns.response(200, "Product was deleted successfully from the cart")
    @any_ns.expect(add_remove_item_parser)
    def delete(self):
        '''
        Removes an item from the user's cart 
        '''
        args = add_remove_item_parser.parse_args()
        token = args['Authorization']
        pid = args['product_id']

        return jsonify({
            "statusCode": 200,
            "message": "",
            "data": {
                "Auth": token,
                "product_id": pid
            }
        })


# Admins don't have any actions they can do over carts directly.