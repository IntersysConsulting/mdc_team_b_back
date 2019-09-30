from flask import jsonify
from flask_restplus.namespace import RequestParser
from ...resources.customer import CustomerManager
from ...resources.validation import is_customer, is_not_customer_response
#################
# Parser        #
#################

#################
# Method        #
#################


def Get(identity):
    if not is_customer(identity):
        response = is_not_customer_response
    else:
        cm = CustomerManager()
        customer = cm.get_data(identity)
        print("We got this customer: {}".format(customer))
        #Here we get all the customer account details. Then we probably save it on backend.
        response = jsonify({
            "statusCode": 200,
            "message": "Success",
            "data": customer
        })
    return response