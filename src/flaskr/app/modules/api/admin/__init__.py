from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ...resources.admin import AdminManagement
# from werkzeug.datastructures import FileStorage
from .get import Get, Parser as get_admin
from .post import Post, Parser as add_admin
from .put import Put, Parser as update_admin
from .delete import Delete, Parser as delete_admin

admin_ns = Namespace(
    "admin/management",
    description="Endpoints that allows admins to manage the store's staff")


@admin_ns.route("/")
@admin_ns.response(403, "Forbidden - User is not an admin")
class Admin(Resource):
    @admin_ns.expect(get_admin)
    def get(self):
        '''
        Returns currently registered admins. Might be sorted A-Z, Z-A, oldest first, newest first.
        '''
        args = get_admin.parse_args()
        return Get(args)

    @admin_ns.response(200, 'Admin was successfully created')
    @admin_ns.expect(add_admin)
    def post(self):
        '''
        Registers a new admin in the database
        '''
        args = add_admin.parse_args()
        return Post(args)

    @admin_ns.response(200, 'Admin was successfully updated')
    @admin_ns.expect(update_admin)
    def put(self):
        '''
        Updates and existing admin information
        '''
        args = update_admin.parse_args()
        return Put(args)

    @admin_ns.response(200, 'Admin was sucessfully deleted')
    @admin_ns.expect(delete_admin)
    def delete(self):
        '''
        Deletes an admin from the database
        '''
        args = delete_admin.parse_args()

        return Delete(args)