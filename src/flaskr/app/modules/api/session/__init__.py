from flask import jsonify
from flask_restplus import Resource, fields, Namespace, reqparse

from .customer.post import Post as CustomerPost, Parser as customer_login_parser
from .customer.delete import Delete as CustomerDelete, Parser as customer_logout_parser
from .customer.put import Put as CustomerPut, Parser as customer_refresh_token_parser
from .admin.post import Post as AdminPost, Parser as admin_login_parser
from .admin.delete import Delete as AdminDelete, Parser as admin_logout_parser
from .admin.put import Put as AdminPut, Parser as admin_refresh_token_parser
from flask_jwt_extended import (jwt_refresh_token_required, get_jwt_identity)

customer_ns = Namespace(
    "session",
    description="Endpoints that allow customers to interact with their session"
)

admin_ns = Namespace(
    "admin/session",
    description="Endpoints that allow admins to interact with their session")


@customer_ns.route("/")
@customer_ns.response(401, "Invalid Credentials")
class CustomerSession(Resource):
    @customer_ns.expect(customer_refresh_token_parser)
    def put(self):
        '''
        √ Allows the customer refresh the token
        The Authentication: Bearer [] header must use the refresh_token, not the access token.
        '''
        args = customer_refresh_token_parser.parse_args()
        return AdminPut(args)

    @customer_ns.expect(customer_login_parser)
    def post(self):
        '''
        √ Allows the customer to log in with their email and password
        '''
        args = customer_login_parser.parse_args()
        return CustomerPost(args)

    @customer_ns.expect(customer_logout_parser)
    def delete(self):
        '''
        NYI Allows the customer to log out of their current session
        '''
        args = customer_logout_parser.parse_args()
        return CustomerDelete(args)


@admin_ns.route("/")
@admin_ns.response(401, "Invalid Credentials")
class AdminSession(Resource):
    @admin_ns.expect(admin_refresh_token_parser)
    def put(self):
        '''
        √ Allows the admin refresh the token
        The Authentication: Bearer [] header must use the refresh_token, not the access token.
        '''
        args = admin_refresh_token_parser.parse_args()
        return AdminPut(args)

    @admin_ns.expect(admin_login_parser)
    def post(self):
        '''
        √ Allows the admin to log in with their email and password
        '''
        args = admin_login_parser.parse_args()
        return AdminPost(args)

    @admin_ns.expect(admin_logout_parser)
    def delete(self):
        '''
        NYI Allows the admin to log out of their current session
        '''
        args = admin_logout_parser.parse_args()
        return AdminDelete(args)
