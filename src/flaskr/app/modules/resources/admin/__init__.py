from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import AdminSchema
from ..password_management import hash_password, verify_hash
from flask_jwt_extended import (create_access_token, create_refresh_token)


class AdminManagement:
    def __init__(self):
        self.collection_name = "admins"
        self.db = Database()

    def login_admin(self, email, password):
        '''
        Attempts to log in an admin. 
        Returns  1, _id  on Success (_id = admin object id)
        Returns  0, None on Wrong Password
        Returns -1, None on Wrong Email

        Keyword arguments:
        email -- The email of the admin
        password -- The password of the admin
        '''

        result = self.db.find(self.collection_name, {"email": email})

        if result == None:
            response = (-1, None)

        else:
            admin = self.dump(result)
            response = (1, admin["_id"]) if verify_hash(
                password, admin["password"]) else (0, None)

        return response

    def find_admin(self, email):
        admin = self.db.find(self.collection_name, {"email": email})
        return self.dump(admin)

    def get_all_admins(self):
        pass

    def create_admin(self, first_name, last_name, email, access):
        admin = self.db.create(self.collection_name, ({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "reset_token": {
                "accessCode": access,
                "attempts": 0,
            },
            "last_login": '',
            "enabled": true
        }))
        return self.dump(admin)

    def delete_admin(self, id, email=None):
        # If the parameter email field is not blank then it tries to delete by email. Otherwise it will look up by _id
        admin = self.db.delete(self.collection_name, ({
            "email": email
        })) if not email == None else self.db.delete(self.collection_name,
                                                     ({
                                                         "_id": id
                                                     }))
        print(self.dump(admin))
        return self.dump(admin)

    def update_admin(self, id, name, password, comment=""):
        pass

    def update_password(self, email, new_password):
        # updated = self.db.update({email:email}, {$set: {password: new_password}})

        new_password = {"$set": {"password": new_password}}
        email = {"first_name": email}
        updated = self.db.update(self.collection_name, email, new_password)

    def create_password(self, code, password, email):
        user = self.db.find(self.collection_name, {"email": email})
        response = jsonify({"": ""})
        if user and user['enabled']:
            if user['reset_token']['accessCode'] == int(code):
                updated = self.db.update(self.collection_name,
                                         {'_id': user['_id']},
                                         {"$set": {
                                             "password": password
                                         }})
                access_token = create_access_token(identity=user['email'])
                refresh_token = create_refresh_token(identity=user['email'])
                response = jsonify({
                    "statusCode": 200,
                    "message": "Successfully created password admin",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            elif user['reset_token']['attempts'] < 2:
                attempts = user['reset_token']['attempts'] + 1
                self.db.update(self.collection_name, {'_id': user['_id']},
                               {"$set": {
                                   "reset_token.attempts": attempts
                               }})
                response = jsonify({
                    "statusCode":
                    200,
                    "message":
                    "Your access code isn't valid, please make another attempt",
                })
            else:
                self.db.update(self.collection_name, {'_id': user['_id']},
                               {"$set": {
                                   "enabled": false
                               }})
                response = jsonify({
                    "statusCode": 200,
                    "message": "Please contact an admin",
                })

        return response

    def dump(self, data):
        return AdminSchema().dump(data).data
