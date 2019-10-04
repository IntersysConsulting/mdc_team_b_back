from flask import jsonify
from flask_restplus.namespace import RequestParser
from ....resources.customer import CustomerManager
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
#################
# Parser        #
#################
Parser = RequestParser()

#################
# Method        #
#################


def Post():
    # This makes a temporary user for a guest
    cm = CustomerManager()

    insert_result = cm.make_guest()

    if insert_result.acknowledged:
        _id = str(insert_result.inserted_id)
        access_token = create_access_token(identity=_id,
                                           expires_delta=timedelta(days=1))
        refresh_token = create_refresh_token(identity=_id)

        response = jsonify({
            "statusCode": 200,
            "message": "Welcome guest!",
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
    else:
        response = jsonify({
            "statusCode": 400,
            "message": "Could not create guest account",
        })

    return response