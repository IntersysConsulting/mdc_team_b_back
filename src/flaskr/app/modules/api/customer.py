from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ..resources.customer import Customer
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage
from datetime import datetime

guest_ns = Namespace(
    "customers/guest",
    description="Endpoints that allow users to work with guest accounts")
customer_ns = Namespace(
    "customers", description="Endpoints that interact with guest and customer accounts")

#########################################################
#   Guest Account section
#########################################################

update_guest_info_parser = guest_ns.parser()
update_guest_info_parser.add_argument('Authorization',
                                      help='Guest token',
                                      required=True,
                                      location='headers')
update_guest_info_parser.add_argument('first_name',
                                      help='Customer first name',
                                      required=True,
                                      location='form')
update_guest_info_parser.add_argument('last_name',
                                      help='Customer last name',
                                      required=True,
                                      location='form')
update_guest_info_parser.add_argument('email',
                                      help='Customer email',
                                      required=True,
                                      location='form')
update_guest_info_parser.add_argument('phone',
                                      help='Customer phone number',
                                      required=False,
                                      location='form')
#update_guest_info_parser.add_argument('ToS', help='ToS code', required=True, location='form') # This is not a code. Instead it should be a timestamp generated in the back end. Nobody should have access to modifying this field


@guest_ns.route("/")
class GuestOptions(Resource):
    def post(self):
        '''
        Creates guest account so guest can use a cart
        '''
        first_name = " "  #illustrative, you wont actually send these empty strings in the POST
        last_name = " "
        email = " "
        password = " "
        phone = 0
        ToS = 0
        is_guest = True
        timestamp = datetime.now(
        )  # This is important to have as you need to know when a guest was created. Will be overriden if they become a full user.
        cart = 1  #This should ask the resource to make a cart, then assign the cart's ID to this field

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully created guest account",
            "data": { "Authorization": "bearer token (Here goes whatever JWT is generated)" }
        })
        return response

    @guest_ns.response(200, 'Successfully updated guest information')
    @guest_ns.expect(update_guest_info_parser)
    def put(self):
        '''
        When a guest wants to finish a purchase we get their information to be stored in their guest account. 
        '''
        args = update_guest_info_parser.parse_args()
        token = args['Authorization']
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = 0 if not args['phone'] else args['phone']
        # This endpoint was reached thanks to them accepting the TOS, so the timestamp should just be now.
        # We should not let anyone send a timestamp as this could lead to fake timestamps.
        ToS = datetime.now().strftime(
            "%d-%b-%Y (%H:%M:%S.%f)"
        )  #An indicative that the ToS were accepted

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully updated guest information",
            "data": {
                "Auth": token,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "ToS": ToS
            }
        })
        return response


#########################################################
#   Customer Account section
#########################################################

create_new_acc_parser = customer_ns.parser()
create_new_acc_parser.add_argument(
    'Authorization',
    help='Token the guest had before making their account.',
    required=True,
    location='headers')
create_new_acc_parser.add_argument('first_name',
                                   help='Customer first name',
                                   required=True,
                                   location='form')
create_new_acc_parser.add_argument('last_name',
                                   help='Customer last name',
                                   required=True,
                                   location='form')
create_new_acc_parser.add_argument('email',
                                   help='Customer email',
                                   required=True,
                                   location='form')
create_new_acc_parser.add_argument('password',
                                   help='Customer password',
                                   required=True,
                                   location='form')
create_new_acc_parser.add_argument('phone',
                                   help='Customer phone number',
                                   required=False,
                                   location='form')

get_acc_details = customer_ns.parser()
get_acc_details.add_argument('Authorization',
                             help='Customer token',
                             required=True,
                             location='headers')


@customer_ns.route("/")  #pagename:port/customer/
class CustomerOptions(Resource):
    @customer_ns.response(200, 'Account succesfully created')
    @customer_ns.expect(create_new_acc_parser)
    def post(self):
        '''
        Creates a new account. 
        Passes the old guest auth token as a parameter to modify the document in the database.
        This allows us to retain shipping and billing addresses that were previously assigned, and to retain the user's cart after they sign up.
        In reality it should only respond with the Authorization token
        '''
        args = create_new_acc_parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        password = args['password']
        phone = 0 if not args['phone'] else args['phone']
        ToS = datetime.now()
        timestamp = datetime.now()
        cart = 1  #This should ask the resource to make a cart, then assign the cart's ID to this field
        response = jsonify({
            "statusCode": 200,
            "message":"Successfully created customer account",
            "data": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "phone": phone,
                "ToS": ToS.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                "timestamp": timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                "cart": cart
            }
        })
        return response

    @customer_ns.expect(get_acc_details)
    def get(self):
        """
        Returns the customer's visible data.
        Visible Data: First name, Last name, E-Mail, Phone Number, and various addresses. 
        Excludes information like password, TOS timestamp, account creation timestamp and cart id since they're unnecessary for our customer. 
        """
        args = get_acc_details.parse_args()
        token = args['Authorization']

        #Here we get all the customer account details. Then we probably save it on backend.
        response = jsonify({"statusCode": 200,
        "message":"Success", "data": {"Auth": token}})
        return response

#########################################################
#   Billing section
#########################################################

add_acc_billing = customer_ns.parser()
add_acc_billing.add_argument('Authorization',
                             help='Customer token',
                             required=True,
                             location='headers')
add_acc_billing.add_argument('billing',
                             help='Billing address JSON object',
                             required=True,
                             location='form')
add_acc_billing.add_argument(
    'is_default',
    help='Whether the address getting updated is going to be the new default',
    required=True,
    location='form')

upd_acc_billing = customer_ns.parser()
upd_acc_billing.add_argument('Authorization',
                             help='Customer token',
                             required=True,
                             location='form')
#We need the old address to find the object we will replace
upd_acc_billing.add_argument('old_billing_address',
                             help='Old billing address JSON object',
                             required=True,
                             location='form')
upd_acc_billing.add_argument('billing',
                             help='New billing address JSON object',
                             required=True,
                             location='form')
upd_acc_billing.add_argument(
    'is_default',
    help='Whether the address getting updated is going to be the new default',
    required=True,
    location='form')

delete_billing_parser = customer_ns.parser()
delete_billing_parser.add_argument('Authorization',
                                    help="Customer Token",
                                    required=True,
                                    location='headers')
delete_billing_parser.add_argument('billing',
                                    help="JSON object of the address to be deleted",
                                    required=True,
                                    location="form")


@customer_ns.route("/billing")  #pagename:port/customer/billing
class CustomerBillingOptions(Resource):
    @customer_ns.response(200, 'Billing address succesfully added')
    @customer_ns.expect(add_acc_billing)
    def post(self):
        '''
        Creates new billing address
        '''
        args = add_acc_billing.parse_args()
        token = args['Authorization']
        billing = args['billing']
        is_default = args['is_default']

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully added a billing address",
            "data": {
                "Auth": token,
                "billing": billing,
                "is_default": is_default
            }
        })
        return response

    @customer_ns.response(200, 'Billing address succesfully updated')
    @customer_ns.expect(upd_acc_billing)
    def put(self):
        '''
        Updates a billing address
        '''
        args = upd_acc_billing.parse_args()
        token = args['Authorization']
        old_billing = args['old_billing_address']
        billing = args['billing']
        is_default = args['is_default']

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully updated a billing address",
            "data": {
                "Auth": token,
                "old_billing_address": old_billing,
                "billing": billing,
                "is_default": is_default
            }
        })
        return response
    @customer_ns.response(200, 'Billing address successfully deleted')
    @customer_ns.expect(delete_billing_parser)
    def delete(self):
        '''
        Deletes one of the user's billing addresses
        '''
        args = delete_billing_parser.parse_args()
        token = args['Authorization']
        billing = args['billing']
        response = jsonify({
            "statusCode": 200,
            "message":"Successfully updated a billing address",
            "data": {
                "Auth": token,
                "billing": billing
            }
        })
        return response


#########################################################
#   Shipping section
#########################################################

add_acc_shipping = customer_ns.parser()
add_acc_shipping.add_argument('Authorization',
                              help='Customer token',
                              required=True,
                              location='form')
add_acc_shipping.add_argument('shipping',
                              help='Shipping address JSON object',
                              required=True,
                              location='form')
add_acc_shipping.add_argument(
    'is_default',
    help='Whether the address getting updated is going to be the new default',
    required=True,
    location='form')

upd_acc_shipping = customer_ns.parser()
upd_acc_shipping.add_argument('Authorization',
                              help='Customer token',
                              required=True,
                              location='form')
#We need the old address to find the object we will replace
upd_acc_shipping.add_argument('old_shipping_address',
                              help='Old billing address JSON object',
                              required=True,
                              location='form')
upd_acc_shipping.add_argument('shipping',
                              help='New shipping address JSON object',
                              required=True,
                              location='form')
upd_acc_shipping.add_argument(
    'is_default',
    help='Whether the address getting updated is going to be the new default',
    required=True,
    location='form')

delete_shipping_parser = customer_ns.parser()
delete_shipping_parser.add_argument('Authorization',
                                   help="Customer Token",
                                   required=True,
                                   location='headers')
delete_shipping_parser.add_argument(
    'shipping',
    help="JSON object of the address to be deleted",
    required=True,
    location="form")


@customer_ns.route("/shipping")  #pagename:port/customer/shipping
class CustomerShippingOptions(Resource):
    @customer_ns.response(200, 'Shipping address succesfully created')
    @customer_ns.expect(add_acc_shipping)
    def post(self):
        '''
        Creates new shipping address
        '''
        args = add_acc_shipping.parse_args()
        token = args['Authorization']
        shipping = args['shipping']
        is_default = args['is_default']

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully",
            "data": {
                "Auth": token,
                "shipping": shipping,
                "is_default": is_default
            }
        })
        return response

    @customer_ns.response(200, 'Shipping address succesfully updated')
    @customer_ns.expect(upd_acc_shipping)
    def put(self):
        '''
        Updates a shipping address
        '''
        args = upd_acc_shipping.parse_args()
        token = args['Authorization']
        old_shipping = args['old_shipping_address']
        shipping = args['shipping']
        is_default = args['is_default']

        response = jsonify({
            "statusCode": 200,
            "message":"Successfully",
            "data": {
                "Auth": token,
                "old_shipping_address": old_shipping,
                "shipping": shipping,
                "is_default": is_default
            }
        })
        return response

    @customer_ns.expect(delete_shipping_parser)
    def delete(self):
        '''
        Deletes one of the user's shipping addresses
        '''
        args = delete_shipping_parser.parse_args()
        token = args['Authorization']
        shipping = args['shipping']
        response = jsonify({
            "statusCode": 200,
            "message": "Successfully updated a shipping address",
            "data": {
                "Auth": token,
                "shipping": shipping
            }
        })
        return response