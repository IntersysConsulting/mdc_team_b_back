from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ..resources.customer import Customer
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage
import datetime

guest_ns = Namespace("customers/guest", description="APIs for customer data for unregistered users")
customer_ns = Namespace("customers", description="APIs for customer data for registered users")

# Guest section
update_guest_info_parser = guest_ns.parser()
update_guest_info_parser.add_argument('token', help='Guest token', required=True, location='headers')
update_guest_info_parser.add_argument('first_name', help='Customer first name', required=True, location='form')
update_guest_info_parser.add_argument('last_name', help='Customer last name', required=True, location='form')
update_guest_info_parser.add_argument('email', help='Customer email', required=True, location='form')
update_guest_info_parser.add_argument('phone', help='Customer phone number', required=True, location='form')
#update_guest_info_parser.add_argument('ToS', help='ToS code', required=True, location='form') # This is not a code. Instead it should be a timestamp generated in the back end. Nobody should have access to modifying this field

@guest_ns.route("/")
class GuestOptions(Resource):
    def post(self):
        '''
        Creates guest account so guest can use a cart
        '''
        first_name = " " #illustrative, you wont actually send these empty strings in the POST
        last_name = " "
        email = " "
        pwd = " "
        phone = " "
        ToS = 0
        is_guest = True #you probably won't need to send this field also
        timestamp = 1 #timestamp shouldn't be added here, this is just illustrating that a timestamp is created when you create an account
        cart = 1 #a cart is created when you make an account

        response = jsonify({"statusCode":201, "data":{"first_name":first_name, "last_name":last_name,"email":email, "pwd":pwd, "phone":phone, "ToS":ToS, "is_guest":is_guest, "timestamp": timestamp, "cart":cart}})
        return response

    @guest_ns.response(204, 'Order successfully updated')
    @guest_ns.expect(update_guest_info_parser)
    def put(self):
        '''
        Updates guest account in order to create an order
        '''
        args = update_guest_info_parser.parse_args()
        token = args['token']
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        # This endpoint was reached thanks to them accepting the TOS, so the timestamp should just be now.
        # We should not let anyone send a timestamp as this could lead to fake timestamps.
        ToS = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") #An indicative that the ToS were accepted

        response = jsonify({"statusCode":204, "data":{"Auth":token, "first_name":first_name, "last_name":last_name, "email":email, "phone":phone, "ToS":ToS}})
        return response



# Customer Section

create_new_acc_parser = customer_ns.parser()
create_new_acc_parser.add_argument('token', help='Token the guest had before making their account.', required=True, location='headers')
create_new_acc_parser.add_argument('first_name', help='Customer first name', required=True, location='form')
create_new_acc_parser.add_argument('last_name', help='Customer last name', required=True, location='form')
create_new_acc_parser.add_argument('email', help='Customer email', required=True, location='form')
create_new_acc_parser.add_argument('pwd', help='Customer password', required=True, location='form')
create_new_acc_parser.add_argument('phone', help='Customer phone number', required=True, location='form')
# create_new_acc_parser.add_argument('ToS', help='ToS code', required=True, location='form')  # This is not a code. Instead it should be a timestamp generated in the back end. Nobody should have access to modifying this field

get_acc_details = customer_ns.parser()
get_acc_details.add_argument('token', help='Customer token', required=True, location='headers')

@customer_ns.route("/") #pagename:port/customer/
class CustomerOptions(Resource):
    @customer_ns.response(201, 'Account succesfully created')
    @customer_ns.expect(create_new_acc_parser)
    def post(self):
        '''
        Creates new account
        '''
        args = create_new_acc_parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        pwd = args['pwd']
        phone = args['phone']
        ToS = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        timestamp = 1 #timestamp shouldn't be added here, this is just illustrating that a timestamp is created when you create an account
        cart = 1 #a cart is created when you make an account

        response = jsonify({"statusCode":201, "data":{"first_name":first_name, "last_name":last_name, "email":email, "pwd":pwd, "phone":phone, "ToS":ToS, "timestamp": timestamp, "cart":cart}})
        return response

    @customer_ns.expect(get_acc_details)
    def get(self):
        """
        Returns all the customer account details
        """
        args = get_acc_details.parse_args()
        token = args['token']

        #Here we get all the customer account details. Then we probably save it on backend.
        response = jsonify({"statusCode":200, "data":{"Auth":token}})
        return response


add_acc_billing = customer_ns.parser()
add_acc_billing.add_argument('token', help='Customer token', required=True, location='form')
add_acc_billing.add_argument('billing', help='Billing address JSON object', required=True, location='form')
add_acc_billing.add_argument('is_default', help='Whether the address getting updated is going to be the new default', required=True, location='form')

upd_acc_billing = customer_ns.parser()
upd_acc_billing.add_argument('token', help='Customer token', required=True, location='form')
#We need the old address to find the object we will replace
upd_acc_billing.add_argument('old_billing_address', help='Old billing address JSON object', required=True, location='form')
upd_acc_billing.add_argument('billing', help='New billing address JSON object', required=True, location='form')
upd_acc_billing.add_argument('is_default', help='Whether the address getting updated is going to be the new default', required=True, location='form')

@customer_ns.route("/billing") #pagename:port/customer/billing
class CustomerBillingOptions(Resource):
    @customer_ns.response(201, 'Billing address succesfully created')
    @customer_ns.expect(add_acc_billing)
    def post(self):
        '''
        Creates new billing address
        '''
        args = add_acc_billing.parse_args()
        token = args['token']
        billing = args['billing']
        is_default = args['is_default']

        response = jsonify({"statusCode":201, "data":{"Auth":token, "billing":billing, "is_default":is_default}})
        return response

    @customer_ns.response(204, 'Billing address succesfully updated')
    @customer_ns.expect(upd_acc_billing)
    def put(self):
        '''
        Updates a billing address
        '''
        args = upd_acc_billing.parse_args()
        token = args['token']
        old_billing = args['old_billing_address']
        billing = args['billing']
        is_default = args['is_default']

        response = jsonify({"statusCode":204, "data":{"Auth":token, "old_billing_address":old_billing, "billing":billing, "is_default":is_default}})
        return response

add_acc_shipping = customer_ns.parser()
add_acc_shipping.add_argument('token', help='Customer token', required=True, location='form')
add_acc_shipping.add_argument('shipping', help='Shipping address JSON object', required=True, location='form')
add_acc_shipping.add_argument('is_default', help='Whether the address getting updated is going to be the new default', required=True, location='form')

upd_acc_shipping = customer_ns.parser()
upd_acc_shipping.add_argument('token', help='Customer token', required=True, location='form')
#We need the old address to find the object we will replace
upd_acc_shipping.add_argument('old_shipping_address', help='Old billing address JSON object', required=True, location='form')
upd_acc_shipping.add_argument('shipping', help='New shipping address JSON object', required=True, location='form')
upd_acc_shipping.add_argument('is_default', help='Whether the address getting updated is going to be the new default', required=True, location='form')

@customer_ns.route("/shipping") #pagename:port/customer/shipping
class CustomerShippingOptions(Resource):
    @customer_ns.response(201, 'Shipping address succesfully created')
    @customer_ns.expect(add_acc_shipping)
    def post(self):
        '''
        Creates new shipping address
        '''
        args = add_acc_shipping.parse_args()
        token = args['token']
        shipping = args['shipping']
        is_default = args['is_default']

        response = jsonify({"statusCode":201, "data":{"Auth":token, "shipping":shipping, "is_default":is_default}})
        return response

    @customer_ns.response(204, 'Shipping address succesfully updated')
    @customer_ns.expect(upd_acc_shipping)
    def put(self):
        '''
        Updates a shipping address
        '''
        args = upd_acc_shipping.parse_args()
        token = args['token']
        old_shipping = args['old_shipping_address']
        shipping = args['shipping']
        is_default = args['is_default']

        response = jsonify({"statusCode":204, "data":{"Auth":token, "old_shipping_address":old_shipping, "shipping":shipping, "is_default":is_default}})
        return response