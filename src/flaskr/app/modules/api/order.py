from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ..resources.order import AdminOrder, UserOrder
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage

user_ns = Namespace("orders", description="APIs that work with orders")
admin_ns = Namespace("admin/orders",
                     description="Admin APIs that work with orders")

# Customer Section

#Create order
user_order_add_parser = user_ns.parser()
user_order_add_parser.add_argument('token',
                                   type=int,
                                   help='User token',
                                   required=True,
                                   location='form')
user_order_add_parser.add_argument('items',
                                   help='Cart object',
                                   required=True,
                                   location='form')
user_order_add_parser.add_argument('user_billing',
                                   help='User biling method',
                                   required=True,
                                   location='form')
user_order_add_parser.add_argument('user_shipping',
                                   help='User shipping method',
                                   required=True,
                                   location='form')

#Get a user orders
user_order_get_parser = user_ns.parser()
user_order_get_parser.add_argument('token',
                                   type=int,
                                   help='User token',
                                   required=True,
                                   location='form')
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


@user_ns.route("/")
class UserOrders(Resource):
    @user_ns.response(200, 'Order succesfully added')
    @user_ns.expect(user_order_add_parser)
    def post(self):
        '''
        Creates new order
        '''
        args = user_order_add_parser.parse_args()
        token = args['token']
        items = args['items']  #whole item objects array
        user_billing = args['user_billing']  #whole billing object
        user_shipping = args['user_shipping']  #whole shipping object
        timestamp = 1  #timestamp shouldn't be added here, this is just illustrative
        response = jsonify({
            "statusCode": 200,
            'message': 'Order succesfully added',
            "data": {
                "Auth": token,
                "items": items,
                "billing_id": user_billing,
                "shipping_id": user_shipping,
                "timestamp": timestamp
            }
        })
        return response

    @user_ns.expect(user_order_get_parser)
    def get(self):
        """
        Returns a sorted and filtered list of orders that the user has made
        """
        args = user_order_get_parser.parse_args()
        token = args[
            'token']  #sends auth token to get user id and then the orders
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


# Admin Section

#Update order status
admin_order_update_parser = admin_ns.parser()
admin_order_update_parser.add_argument('token',
                                       help='Admin Auth token',
                                       required=True,
                                       location='form')
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
admin_order_get_parser.add_argument('token',
                                    help='Admin Auth token',
                                    required=True,
                                    location='form')
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
        token = args['token']
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
        token = args['token']
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


# any_ns = Namespace("orders", description="Guest APIs that work with orders")
# Guest section
# create order
# guest_order_add_parser = any_ns.parser()
# #Before creating a guest order we update the guest account info to add email, ToS, and Name
# #We don't save email in the order, we save the user id. We get the ID by sending the token
# guest_order_add_parser.add_argument('token', help='Guest token', required=True, location='form')
# guest_order_add_parser.add_argument('items', help='Cart object', required=True, location='form')
# guest_order_add_parser.add_argument('billing', help='Guest billing address', required=True, location='form')
# guest_order_add_parser.add_argument('shipping', help='Guest shipping address', required=True, location='form')
# @any_ns.route("/")
# class GuestOrders(Resource):
#     @any_ns.expect(guest_order_add_parser)
#     def post(self):
#         '''
#         Creates new order
#         '''
#         args = guest_order_add_parser.parse_args()
#         token = args['token']
#         items = args['items']
#         guest_billing = args['billing']
#         guest_shipping = args['shipping']
#         timestamp = 1 #timestamp shouldn't be added here, this is just illustrative
#         response = jsonify({"statusCode":200, "data":{"Auth":token, "items":items, "billing":guest_billing, "shipping":guest_shipping, "timestamp": timestamp}})
#         return response
