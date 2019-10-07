from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.customer import CustomerManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from datetime import timedelta
#################
# Parser        #
#################
Parser = RequestParser()
Parser.add_argument("email",
                    help="Customer's e-mail tied to their account.",
                    required=False,
                    location="form")
Parser.add_argument("password",
                    help="Customer's password.",
                    required=False,
                    location="form")
#################
# Method        #
#################


def Post(args):
    email = args['email']
    password = args['password']

    print("The user {} is trying to log in.".format(email))
    cm = CustomerManager()

    result, customer = cm.login(email, password)

    if result == 1:
        access_token = create_access_token(identity=customer["_id"], expires_delta=timedelta(days=1))
        refresh_token = create_refresh_token(identity=customer["_id"])

        response = jsonify({
            "statusCode": 200,
            "message": "Welcome customer",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "customer_name": "{} {}".format(customer["first_name"], customer["last_name"])
        })
    elif result == 0:
        response = jsonify({"statusCode": 400, "message": "Wrong password"})
    elif result == -1:
        response = jsonify({"statusCode": 400, "message": "Wrong email"})
    else:
        response = jsonify({"statusCode": 400, "message": "Unexpected error"})
    return response