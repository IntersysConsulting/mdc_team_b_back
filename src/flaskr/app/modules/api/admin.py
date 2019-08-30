from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from ..resources.admin import AdminManagement
from werkzeug.datastructures import FileStorage

admin_ns = Namespace("admin/management", description="APIs for administration of store admins ")

# Get admins
get_admin = admin_ns.parser()
get_admin.add_argument('sort', type=int, help='ID of the Sorting method to be used', required=False)
get_admin.add_argument('page', type=int, help='Page the request is asking for', required=False)

#Add admin
add_admin = admin_ns.parser()
add_admin.add_argument('first_name', help='First name of the admin to be registered', required=True, location='form')
add_admin.add_argument('last_name', help='Last name of the admin to be registered', required=True, location='form')
add_admin.add_argument('email', help='Email address under which the admin will be registered', required=True, location='form')

#Update admin
update_admin = admin_ns.parser()
update_admin.add_argument('id', type=int, help='ID of the admin that will be updated', required=True, location='form')
update_admin.add_argument('current_password', help='Current password of admin', required=True, location='form')
update_admin.add_argument('first_name', help='First name of the admin', required=True, location='form')
update_admin.add_argument('last_name', help='Last name of the admin', required=True, location='form')
update_admin.add_argument('new_password', help='Password that will replace the current one', required=False, location='form')

#Delete admin
delete_admin = admin_ns.parser()
delete_admin.add_argument('id', type=int, help='ID of the admin to be deleted', required=True, location='form')


@admin_ns.route("/")
@admin_ns.response(404, " Admin not found")
@admin_ns.response(403, "Forbidden - User is not an admin")

class Admin(Resource):
    @admin_ns.expect(get_admin)
    def get(self):
        '''
        Returns currently registered admins. Might be sorted A-Z, Z-A, oldest first, newest first.
        '''
        args = get_admin.parse_args()
        sort = 0 if not args['sort'] else args['sort']
        page = 0 if not args['page'] else args['page']
        response = jsonify({
            "statusCode": 200,
            "data": {
                "sort": sort,
                "page": page
            }
        })
        return response

    @admin_ns.response(201, 'Admin was successfully created')
    @admin_ns.expect(add_admin)
    def post(self):
        '''
        Registers a new admin in the database
        '''
        args = add_admin.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']

        response = jsonify({
            "statusCode": 200,
            "data": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        })
        return response

    @admin_ns.response(204, 'Admin was successfully updated')
    @admin_ns.expect(update_admin)
    def put(self):
        '''
        Updates and existing admin information
        '''
        args = update_admin.parse_args()
        admin_id = args['id']
        current_password = args['current_password']
        first_name = args['first_name']
        last_name = args['last_name']
        new_password = '' if not args['new_password'] else args['new_password']

        response = jsonify({
            "statusCode": 200,
            "data": {
                "id": admin_id,
                "current_password": current_password,
                "first_name": first_name,
                "last_name": last_name,
                "new_password": new_password
            }
        })
        return response

    @admin_ns.response(204, 'Admin was sucessfully deleted')
    @admin_ns.expect(delete_admin)
    def delete(self):
        '''
        Deletes an admin from the database
        '''
        args = delete_admin.parse_args()
        admin_id = args['id']

        response = jsonify({
            "statusCode": 200, 
            "data": {
                "id": admin_id
            }
        })
        return response
