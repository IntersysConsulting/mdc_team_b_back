from flask import Blueprint, jsonify
from flask_restplus import Api, Namespace, Resource
from flask_cors import CORS

import jwt
import flask_jwt_extended

# When you finish your class, add it under this one.
from .product import any_ns as product_any, admin_ns as product_admin
from .order import user_ns as order_user, admin_ns as order_admin
from .payment import any_ns as cards_any
from .cart import any_ns as cart_any
from .customer import customer_ns as customer_user
from .identity import identity_ns as identity_user
from .admin import admin_ns as management_admin
from .session import customer_ns as session_customer, admin_ns as session_admin
from ..auth import authorizations

v1_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
cors = CORS(v1_blueprint, resorces={r'*': {"origins": '*'}})
# CORS(v1_blueprint)

# Keep this as is for now
api = Api(v1_blueprint,
          authorizations=authorizations,
          security='jwt',
          version="1.0",
          title="eCommerce API",
          description="Bundle of API that feed the eCommerce website")

#Handlers for jwt exceptions


@api.errorhandler(jwt.ExpiredSignatureError)
def handle_validation_signature(error):
    return jsonify({
        "statusCode": 401,
        "message": "Invalid or missing credentials",
        "data": {
            "Auth": error.message
        }
    })


@api.errorhandler(flask_jwt_extended.exceptions.NoAuthorizationError)
def handle_validation_error(error):
    return jsonify({
        "statusCode": 401,
        "message": "Invalid or missing credentials",
        "data": {
            "Auth": error.message
        }
    })


# After you import your namespaces, import them into the API

# Please load these in alphabetical order for Swagger

###################################
#   User Namespaces
###################################
api.add_namespace(cards_any)
api.add_namespace(cart_any)
api.add_namespace(customer_user)
api.add_namespace(identity_user)
api.add_namespace(order_user)
api.add_namespace(product_any)
api.add_namespace(session_customer)
###################################
#   Admin Namespaces
###################################
api.add_namespace(management_admin)
api.add_namespace(order_admin)
api.add_namespace(product_admin)
api.add_namespace(session_admin)
