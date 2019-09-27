from flask import jsonify
from flask import Blueprint, request
from flask_restplus import Resource, fields, Namespace
from ...resources.admin import AdminManagement
# from werkzeug.datastructures import FileStorage
from .get import Get, Parser as get_admin_parser
from .post import Post, Parser as add_admin_parser
from .put import Put, Parser as update_admin_parser
from .delete import Delete, Parser as delete_admin_parser
from .reset.put import Put as ResetPut, Parser as reset_password_parser
from .reset.post import Post as ResetPost, Parser as request_password_parser

from ...auth import authorizations

admin_ns = Namespace(
    "admin/management",
    authorizations=authorizations,
    description="Endpoints that allows admins to manage the store's staff")


@admin_ns.route("/")
@admin_ns.doc(security="jwt")
@admin_ns.response(403, "Forbidden - User is not an admin")
class Admin(Resource):
    @admin_ns.expect(get_admin_parser)
    def get(self):
        '''
        Returns currently registered admins. May be sorted A-Z, Z-A, oldest first, newest first.
        '''
        args = get_admin_parser.parse_args()
        return Get(args)

    @admin_ns.response(200, 'Admin was successfully created')
    @admin_ns.expect(add_admin_parser)
    def post(self):
        '''
        Registers a new admin in the database
        '''
        args = add_admin_parser.parse_args()
        return Post(args)

    @admin_ns.response(200, 'Admin was successfully updated')
    @admin_ns.expect(update_admin_parser)
    def put(self):
        '''
        Updates the issuing admin's information
        '''
        return Put(request.json)

    @admin_ns.response(200, 'Admin was sucessfully deleted')
    @admin_ns.expect(delete_admin_parser)
    def delete(self):
        '''
        Deletes an admin from the database
        '''
        args = delete_admin_parser.parse_args()

        return Delete(args)


@admin_ns.route("/reset")
class PasswordReset(Resource):
    @admin_ns.expect(request_password_parser)
    def post(self):
        '''
        Requests a password reset for an admin
        '''
        args = request_password_parser.parse_args()
        return ResetPost(args)

    @admin_ns.expect(reset_password_parser)
    def put(self):
        '''
        Allows an admin to reset their password if they requested it
        '''
        args = reset_password_parser.parse_args()
        return ResetPut(args)
