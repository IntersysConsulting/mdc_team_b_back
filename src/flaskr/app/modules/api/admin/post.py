from flask import jsonify, render_template, Flask
from flask_mail import Message, Mail
from flask_restplus.namespace import RequestParser
from ...resources.admin  import AdminManagement
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

import random

app = Flask(__name__)

#################
# Parser        #
#################
Parser = RequestParser()

Parser.add_argument('first_name',
                    help='First name of the admin to be registered',
                    required=True,
                    location='form')
Parser.add_argument('last_name',
                    help='Last name of the admin to be registered',
                    required=True,
                    location='form')
Parser.add_argument(
    'email',
    help='Email address under which the admin will be registered',
    required=True,
    location='form')

#################
# Method        #
#################


def Post(args):
    first_name = args['first_name']
    last_name = args['last_name']
    email = args['email']

    am = AdminManagement()
    if am.find_admin(email):
        return jsonify({
            'message': 'User {} already exists'.format(email)
        })

    try:
        access = random.randint(1000, 10000)
        am.create_admin(first_name, last_name, email, access)


        msg = Message("Welcome",
                      sender='itersysecommerce@gmail.com',
                      recipients=['banda1915@gmail'])
                      # recipients=[email])

        with app.open_resource("../../../templates/logo.jpg") as fp:
            msg.attach('logo.jpg','image/jpg', fp.read(), 'inline', headers=[['Content-ID','<Myimage>'],])
        msg.html = render_template('email.html', link=access)

        mail = Mail()
        mail.send(msg)

        return jsonify({
            "statusCode": 200,
            "message": "Successfully created new admin",
            "data": {
                "first_name": first_name,
                "last_name": last_name,
                "password": "",
                "reset_token": {
                    'codeAccess': access,
                    # 'create_at': ''
                },
                # "last_login": ''
            }
        })
    except Exception:
        return jsonify({
            'message': Exception
        })
