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
    "customers",
    description="Endpoints that interact with guest and customer accounts")

#########################################################
#   Guest Account section
#########################################################

update_guest_info_parser = guest_ns.parser()

#update_guest_info_parser.add_argument('ToS', help='ToS code', required=True, location='form') # This is not a code. Instead it should be a timestamp generated in the back end. Nobody should have access to modifying this field

#########################################################
#   Billing section
#########################################################

add_acc_billing = customer_ns.parser()

upd_acc_billing = customer_ns.parser()

delete_billing_parser = customer_ns.parser()

#########################################################
#   Shipping section
#########################################################

add_acc_shipping = customer_ns.parser()

upd_acc_shipping = customer_ns.parser()

delete_shipping_parser = customer_ns.parser()


@customer_ns.route("/shipping")  #pagename:port/customer/shipping
class CustomerShippingOptions(Resource):
    @customer_ns.response(200, 'Shipping address succesfully created')
    @customer_ns.expect(add_acc_shipping)
    def post(self):
        '''
        Creates new shipping address
        '''
        args = add_acc_shipping.parse_args()

        return ShippingPost(args)

    @customer_ns.response(200, 'Shipping address succesfully updated')
    @customer_ns.expect(upd_acc_shipping)
    def put(self):
        '''
        Updates a shipping address
        '''
        args = upd_acc_shipping.parse_args()
        return ShippingPut(args)

    @customer_ns.expect(delete_shipping_parser)
    def delete(self):
        '''
        Deletes one of the user's shipping addresses
        '''
        args = delete_shipping_parser.parse_args()
        return ShippingDelete(args)