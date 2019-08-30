from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ..resources.order import AdminOrder, UserOrder
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage

user_ns = Namespace("orders", description="Endpoints that allow customers to manage their orders")
admin_ns = Namespace("admin/orders",
                     description="Endpoints that allow admins to manage store orders")

# Customer Section

#Create order
user_order_add_parser = user_ns.parser()
user_order_add_parser.add_argument('Authorization',
                                   help="Customer's token",
                                   required=True,
                                   location="headers")

#Get a user orders
user_order_get_parser = user_ns.parser()
user_order_get_parser.add_argument('Authorization',
                                   help="Customer's token",
                                   required=True,
                                   location="headers")
user_order_get_parser.add_argument('sort',
                                   type=int,
                                   help='ID of the sorting method to be used',
                                   required=False)
user_order_get_parser.add_argument(
    'filter',
    help='A comma separated string of all the filters that apply',
    required=False)
user_order_get_parser.add_argument('page',
                                   type=int,
                                   help='Page the request is asking for',
                                   required=False)

user_order_update_parser = user_ns.parser()
user_order_update_parser.add_argument('Authorization',
                                      help="Customer's token",
                                      required=True,
                                      location="headers")
user_order_update_parser.add_argument('user_billing',
                                      help='User biling address JSON object',
                                      required=True,
                                      location='form')
user_order_update_parser.add_argument('user_shipping',
                                      help='User shipping address JSON object',
                                      required=True,
                                      location='form')
user_order_update_parser.add_argument(
    'payment',
    help='User payment provider information. Depends on the provider',
    required=True,
    location='form')

user_order_delete_parser = user_ns.parser()
user_order_delete_parser.add_argument('Authorization',
                                      help="Customer's token",
                                      required=True,
                                      location="headers")


@user_ns.route("/")
class UserOrders(Resource):
    @user_ns.expect(user_order_get_parser)
    def get(self):
        '''
        Returns a sorted and filtered list of orders that the user has made
        '''
        args = user_order_get_parser.parse_args()
        token = args[
            'Authorization']  #sends auth token to get user id and then the orders
        filter = " " if not args['filter'] else args['filter']
        sort = 0 if not args['sort'] else args['sort']
        page = 0 if not args['page'] else args['page']

        response = jsonify({
            "statusCode": 200,
            'message': 'Success',
            "data": {
                "Auth": token,
                "sort": sort,
                "filter": filter,
                "page": page
            }
        })
        return response

    @user_ns.response(200, 'Order succesfully added')
    @user_ns.response(403, 'Customer already has an order')
    @user_ns.expect(user_order_add_parser)
    def post(self):
        '''
        Creates new order "In Checkout"
        It should be called as soon as the checkout button is clicked to freeze the items in. 
        It gets the item-list from the user's token by grabbing the cart ID. Then using it to grab a list of product IDs, which then it recovers.
        It will save the items as complete objects at the time it is created.
        Assigns a unique "In Checkout" status to the order. An user may not create more orders if it has an "In Checkout" order. 
        If the user already has an In Checkout order the user should be prompted to delete the old one or to resume with this one. 
        '''
        args = user_order_add_parser.parse_args()
        token = args['Authorization']
        timestamp = 0
        response = jsonify({
            "statusCode": 200,
            'message': 'Order succesfully added',
            "data": {
                "Auth": token,
            }
        })
        return response

    @user_ns.response(403, "User does not have an order to update")
    @user_ns.expect(user_order_update_parser)
    def put(self):
        '''
        Finishes an user's order by adding in billing, shipping and payment information after it was reviewed. 
        This should also clear up the user's cart. 
        '''
        args = user_order_add_parser.parse_args()
        token = args['Authorization']
        user_billing = args['user_billing']  #whole billing object
        user_shipping = args['user_shipping']  #whole shipping object
        payment = args['payment']  # Payment provider info
        timestamp = datetime.now()  # Time at which the order was finished on
        response = jsonify({
            "statusCode": 200,
            'message': 'Order succesfully added',
            "data": {
                "Auth": token,
                "items": items,
                "billing_id": user_billing,
                "shipping_id": user_shipping,
                "timestamp": timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
        })
        return response

    @user_ns.expect(user_order_delete_parser)
    def delete(self):
        '''
        Deletes the user's "In Checkout" order. This happens if the user backs-down from checkout. 
        '''
        args = user_order_get_parser.parse_args()
        token = args[
            'Authorization']  #sends auth token to get user id and then the orders
        response = jsonify({
            "statusCode": 200,
            'message': 'Success',
            "data": {
                "Auth": token
            }
        })
        return response


# Admin Section

#Update order status
admin_order_update_parser = admin_ns.parser()
admin_order_update_parser.add_argument('Authorization',
                                       help='Admin Auth token',
                                       required=True,
                                       location='headers')
admin_order_update_parser.add_argument('id',
                                       type=int,
                                       help='ID of the order to be updated',
                                       required=True,
                                       location='form')
admin_order_update_parser.add_argument('status',
                                       type=int,
                                       help='Status numerical identifier',
                                       required=True,
                                       location='form')

#Get all orders (maybe we filter out completed orders by default)
admin_order_get_parser = admin_ns.parser()
admin_order_get_parser.add_argument('Authorization',
                                    help='Admin Auth token',
                                    required=True,
                                    location='headers')
admin_order_get_parser.add_argument('sort',
                                    type=int,
                                    help='ID of the sorting method to be used',
                                    required=False)
admin_order_get_parser.add_argument(
    'filter',
    help='A comma separated string of all the filters that apply',
    required=False)
admin_order_get_parser.add_argument('page',
                                    type=int,
                                    help='Page the request is asking for',
                                    required=False)


@admin_ns.route('/')
@admin_ns.response(403, "User is not an admin")
class AdminOrders(Resource):
    @admin_ns.response(200, 'Order successfully updated')
    @admin_ns.expect(admin_order_update_parser)
    def put(self):
        '''
        Updates a order status on the database
        '''
        args = admin_order_update_parser.parse_args()
        token = args['Authorization']
        order_id = args['id']
        status = args['status']

        response = jsonify({
            "statusCode": 200,
            'message': 'Successfully updated updated',
            "data": {
                "Auth": token,
                "id": order_id,
                "status": status
            }
        })
        return response

    @admin_ns.expect(admin_order_get_parser)
    def get(self):
        """
        Returns a list of orders from all the users. May be sorted and filtered.
        """
        args = admin_order_get_parser.parse_args()
        token = args['Authorization']
        filter = " " if not args['filter'] else args['filter']
        sort = 0 if not args['sort'] else args['sort']
        page = 0 if not args['page'] else args['page']

        response = jsonify({
            "statusCode": 200,
            'message': 'Success',
            "data": {
                "Auth": token,
                "sort": sort,
                "filter": filter,
                "page": page
            }
        })
        return response
