from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ...resources.customer import Customer
# FileStorage allows us to import files from http requests.
from werkzeug.datastructures import FileStorage
from datetime import datetime
from .get import Get, Parser as get_account_parser
from .post import Post, Parser as add_account_parser
from .put import Put as Put, Parser as update_account_parser
from .guest.post import Post as GuestPost
from .billing.post import Post as BillingPost, Parser as add_billing_parser
from .billing.put import Put as BillingPut, Parser as update_billing_parser
from .billing.delete import Delete as BillingDelete, Parser as delete_billing_parser
from .shipping.post import Post as ShippingPost, Parser as add_shipping_parser
from .shipping.put import Put as ShippingPut, Parser as update_shipping_parser
from .shipping.delete import Delete as ShippingDelete, Parser as delete_shipping_parser

guest_ns = Namespace(
    "customers/guest",
    description="Endpoints that allow users to work with guest accounts")
customer_ns = Namespace(
    "customers",
    description="Endpoints that interact with guest and customer accounts")

#########################################################
#   Guest Account section
#########################################################


@guest_ns.route("/")
class GuestOptions(Resource):
    def post(self):
        '''
        Creates guest account so guest can use a cart
        '''
        return GuestPost()


#########################################################
#   Customer Account section
#########################################################


@customer_ns.route("/")  #pagename:port/customer/
class CustomerOptions(Resource):
    @customer_ns.response(200, 'Account succesfully created')
    @customer_ns.expect(add_account_parser)
    def post(self):
        '''
        Creates a new account. 
        Passes the old guest auth token as a parameter to modify the document in the database.
        This allows us to retain shipping and billing addresses that were previously assigned, and to retain the user's cart after they sign up.
        In reality it should only respond with the Authorization token
        '''
        args = add_account_parser.parse_args()
        return Post(args)

    @customer_ns.expect(get_account_parser)
    def get(self):
        """
        Returns the customer's visible data.
        Visible Data: First name, Last name, E-Mail, Phone Number, and various addresses. 
        Excludes information like password, TOS timestamp, account creation timestamp and cart id since they're unnecessary for our customer. 
        """
        args = get_account_parser.parse_args()

        return Get(args)

    @customer_ns.response(200, 'Successfully updated guest information')
    @customer_ns.expect(update_account_parser)
    def put(self):
        '''
        When a guest wants to finish a purchase we get their information to be stored in their guest account. 
        '''
        args = update_account_parser.parse_args()

        return Put(args)


#########################################################
#   Billing section
#########################################################


@customer_ns.route("/billing")  #pagename:port/customer/billing
class CustomerBillingOptions(Resource):
    @customer_ns.response(200, 'Billing address succesfully added')
    @customer_ns.expect(add_billing_parser)
    def post(self):
        '''
        Creates new billing address
        '''
        args = add_billing_parser.parse_args()

        return BillingPost(args)

    @customer_ns.response(200, 'Billing address succesfully updated')
    @customer_ns.expect(update_billing_parser)
    def put(self):
        '''
        Updates a billing address
        '''
        args = update_billing_parser.parse_args()

        return BillingPut(args)

    @customer_ns.response(200, 'Billing address successfully deleted')
    @customer_ns.expect(delete_billing_parser)
    def delete(self):
        '''
        Deletes one of the user's billing addresses
        '''
        args = delete_billing_parser.parse_args()

        return BillingDelete(args)


#########################################################
#   Shipping section
#########################################################


@customer_ns.route("/shipping")  #pagename:port/customer/shipping
class CustomerShippingOptions(Resource):
    @customer_ns.response(200, 'Shipping address succesfully created')
    @customer_ns.expect(add_shipping_parser)
    def post(self):
        '''
        Creates new shipping address
        '''
        args = add_shipping_parser.parse_args()

        return ShippingPost(args)

    @customer_ns.response(200, 'Shipping address succesfully updated')
    @customer_ns.expect(update_shipping_parser)
    def put(self):
        '''
        Updates a shipping address
        '''
        args = update_shipping_parser.parse_args()
        return ShippingPut(args)

    @customer_ns.expect(delete_shipping_parser)
    def delete(self):
        '''
        Deletes one of the user's shipping addresses
        '''
        args = delete_shipping_parser.parse_args()
        return ShippingDelete(args)