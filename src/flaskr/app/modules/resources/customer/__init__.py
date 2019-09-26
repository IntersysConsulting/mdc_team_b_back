from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from pymongo import errors
from .schema import CustomerSchema
from datetime import datetime
from ..password_management import hash_password, verify_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from bson.objectid import ObjectId


#
class CustomerManager():
    def __init__(self):
        self.collection_name = "customers"
        self.db = Database()

    def make_guest(self):
        new_user = {"is_guest": True}
        result = self.db.create(self.collection_name, new_user)
        return result

    def add(self, _id, first_name, last_name, email, password, phone):
        now = datetime.now()
        # _id = get_jwt_identity()
        print("An account is trying to be created with the id: {}".format(_id))
        try:
            is_user_guest = self.db.find(self.collection_name, {
                "_id": ObjectId(_id),
                "is_guest": True
            })
            if is_user_guest:
                email_is_available = (self.db.find(self.collection_name,
                                                   {"email": email}) == None)

                if email_is_available:
                    new_user = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": hash_password(password),
                        #"reset_token":"",
                        "phone": phone,
                        "terms_of_service_ts": now,
                        "is_guest": False,
                        "shipping_addresses": {},
                        "billing_addresses": {},
                        "cart": ""
                    }

                    print("Making this new user: {}".format(new_user))
                    result = self.db.update(self.collection_name,
                                            {"_id": ObjectId(_id)},
                                            {"$set": new_user})
                    # result = self.db.create(self.collection_name, new_user)
                    print("The database returned: {}".format(result))
                    result = 1

                else:
                    result = -1
            else:
                result = -2
        except:
            result = 0
        return result

    def login(self, email, password):
        '''
        Attempts to log in an customer. 
        Returns  1, _id  on Success (_id = customer object id)
        Returns  0, None on Wrong Password
        Returns -1, None on Wrong Email

        Keyword arguments:
        email -- The email of the customer
        password -- The password of the customer
        '''

        result = self.db.find(self.collection_name, {
            "email": email,
            "is_guest": False
        })

        if result == None:
            response = (-1, None)
        else:
            customer = self.dump(result)
            response = (1, customer["_id"]) if verify_hash(
                password, customer["password"]) else (0, None)

        return response

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

    def dump(self, data):
        return CustomerSchema().dump(data).data