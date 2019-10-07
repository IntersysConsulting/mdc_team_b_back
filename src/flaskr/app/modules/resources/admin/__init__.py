from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import AdminSchema
from ..password_management import hash_password, verify_hash
from flask_jwt_extended import (create_access_token, create_refresh_token)
from pymongo import errors
import random
from ..mail.reset_password import send_reset_password_email


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
            response = (1, admin) if verify_hash(
                password, admin["password"]) else (0, None)

        return response

    def find_admin(self, email):
        admin = self.db.find(self.collection_name, {"email": email})
        return self.dump(admin)

    def get_all_admins(self, sort, page, page_size, field, value):
        query = None
        if field == None:
            query = {}
        else:
            field = field.lower()
            if field == "email":
                # Check for email
                query = {"email": {'$regex': value}}
            elif field == "name":
                query = {
                    "$or": [{
                        "first_name": {
                            '$regex': value
                        }
                    }, {
                        "last_name": {
                            '$regex': value
                        }
                    }]
                }
                # Check for name
            else:
                # Invalid field
                response = -1, 0

        if not query == None:
            list_of_admins = self.db.find_all(self.collection_name,
                                              query,
                                              next_page=page, page_size=page_size)
            total_admins = self.db.get_count(self.collection_name, query)
            admins = []
            for admin in list_of_admins:
                admins.append(
                    self.dump(admin,
                              exclude=["password", "reset_token.access_code"]))
            response = admins, total_admins

        return response

    def create_admin(self, first_name, last_name, email):
        try:
            admin = self.db.create(self.collection_name, ({
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "enabled": True
            }))

            if admin != None:
                # If the admin exists, it requests a code
                res, code = self.request_reset(email)
                if code != None:
                    # If we were able to request resetting the password
                    result = 1
                else:
                    # If we failed to request the password reset
                    result = -2
            else:
                result = 0
        except errors.DuplicateKeyError:
            #There is an admin with that email already!
            result = -1
        return result

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

    def request_reset(self, email):
        user = self.db.find(self.collection_name, {"email": email})
        if user == None:
            response = -1, None
        elif user["enabled"] == False:
            response = -2, None
        elif "reset_token" in user.keys():
            response = -3, None
        else:
            accessCode = random.randint(1000, 10000)
            send_reset_password_email(accessCode, email)
            response = self.db.update(self.collection_name, {'email': email}, {
                "$set": {
                    "reset_token": {
                        "access_code": hash_password(str(accessCode)),
                        "attempts": 0
                    }
                }
            }), accessCode

        print("A token reset was asked by {} and I returned {}".format(
            email, response))
        return response

    def reset_password(self, code, password, email):
        user = self.db.find(self.collection_name, {"email": email})

        if user == None:
            # The user does not exist
            response = -1, None
        elif not 'reset_token' in user.keys():
            # The user did not request to get their password changed
            response = -2, None
        elif user['enabled'] == False:
            # The user's account has been disabled
            response = -3, None
        elif not verify_hash(code, user['reset_token']['access_code']):
            # The user's reset token does not match
            if user['reset_token']['attempts'] >= 2:
                # The user has provided the wrong code too many times
                self.db.update(self.collection_name, {'_id': user['_id']}, {
                    "$set": {
                        "enabled": False,
                        "reset_token.attempts":
                        user['reset_token']['attempts'] + 1
                    }
                })
                # The user's account has been disabled due to exceeding the maximum amount of requests
                response = -3, None
            else:
                # The user provided a wrong token to reset their password an acceptable number of times
                self.db.update(self.collection_name, {'_id': user['_id']}, {
                    "$set": {
                        "reset_token.attempts":
                        user['reset_token']['attempts'] + 1
                    }
                })
                # The user may continue to attempt resetting their password
                response = 0, None
        else:
            # The user exists, wants their password changed, hasn't been disabled and submitted the correct access code
            result = self.db.update(self.collection_name, {'_id': user['_id']},
                                    {
                                        "$set": {
                                            "password": hash_password(password)
                                        },
                                        "$unset": {
                                            "reset_token": ""
                                        }
                                    })
            access_token = create_access_token(identity=user['email'])
            refresh_token = create_refresh_token(identity=user['email'])
            if result == 1:
                # The user was successfully updated

                response = 1, user['_id']
            else:
                # For some reason we could not update the server
                response = -4, None

        return response

    def dump(self, data, exclude=[]):
        return AdminSchema(exclude=exclude).dump(data).data
