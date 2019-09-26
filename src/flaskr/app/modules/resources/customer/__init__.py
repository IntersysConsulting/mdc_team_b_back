from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import CustomerSchema
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token)


class CustomerManager():
    def __init__(self):
        self.collection_name = "orders"
        self.db = Database()

    def add(self,
            first_name,
            last_name,
            email,
            password,
            phone,
            is_guest=False):
        now = datetime.now()

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            #"reset_token":"",
            "phone": phone,
            "terms_of_service_ts": now,
            "is_guest": is_guest,
            "shipping_addresses": {},
            "billing_addresses": {},
            "cart": ""
        }

        print("Making this new user: {}".format(new_user))

        pass

    def updateInfo(self, user_id, user_obj):
        pass

    def GetUserData(self, user_id):
        db.find_all(self.collection_name, user_id)
        pass

    def add_billing(self, user_id, billing_obj):
        pass

    def update_billing(self, user_id, billing_obj_id, billing_obj):
        pass

    def delete_billing(self, user_id, billing_obj_id):
        pass

    def add_shipping(self, user_id, shipping_obj):
        pass

    def update_shipping(self, user_id, shipping_obj_id, shipping_obj):
        pass

    def delete_shipping(self, user, shipping_obj_id):
        pass
