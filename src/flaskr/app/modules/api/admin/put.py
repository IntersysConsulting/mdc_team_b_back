from flask import jsonify, request, make_response
from flask_restplus.namespace import RequestParser, request
from ...resources.admin  import AdminManagement

#################
# Parser        #
#################
Parser = RequestParser()
# Parser.add_argument('Authorization',
#                     help="Admin's session token",
#                     required=True)
# Parser.add_argument('current_password',
#                     help='Current password of admin',
#                     required=True,
#                     location='form')
Parser.add_argument('password',
                    help='Current password of admin',
                    required=True,
                    location='form')
# Parser.add_argument('first_name',
#                     help='First name of the admin',
#                     required=True,
#                     location='form')
# Parser.add_argument('last_name',
#                     help='Last name of the admin',
#                     required=True,
#                     location='form')
# Parser.add_argument('new_password',
#                     help='Password that will replace the current one',
#                     required=False,
#                     location='form')

#################
# Method        #
#################

def Put(args):
    # current_password = args['current_password']
    # first_name = args['first_name']
    # last_name = args['last_name']
    # new_password = '' if not args['new_password'] else args['new_password']
    #
    # codeAccess = args['codeAccess']
    email = args['email']
    #
    # am = AdminManagement()
    #
    # # admin = am.find_admin(email)
    # # if admin['codeAccess'] == codeAccess:
    # # am.update_password(email, new_password)
    # am.update_password(first_name, new_password)


    response = jsonify({
        "statusCode": 200,
        "message": "Successfully updated admin",
        "data": {
            "current_password": email,
            "first_name": '',
            "last_name": '',
            "new_password": ''
        }
    })

    return response
