from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager
from ...resources.validation import is_guest_or_customer, is_not_customer_response
#################
# Parser        #
#################

#################
# Method        #
#################


def Get(identity):
    if not is_guest_or_customer(identity):
        response = is_not_customer_response
    else:
        cm = CustomerManager()
        customer = cm.get_data(identity)
        #Here we get all the customer account details. Then we probably save it on backend.
        response = jsonify({
            "statusCode": 200,
            "message": "Success",
            "data": customer
        })
    return response