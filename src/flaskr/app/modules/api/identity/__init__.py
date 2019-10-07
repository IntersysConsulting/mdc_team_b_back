from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from .get import Get

identity_ns = Namespace(
    "identity",
    description=
    "An endpoint that lets the user get information about themselves.")


@identity_ns.route("/")
class Identity(Resource):
    @jwt_required
    def get(self):
        '''
        √ Returns "Guest", "Customer" or "Admin" depending on the user's JWT token. 
        '''
        identity = get_jwt_identity()
        return Get(identity)
