from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import AdminSchema

from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

# This section is a draft for ideas, will be formally worked on later on.


class PasswordManagement:
    def __init__(self):
        self.todo = "Handle additional methods used for administration of passwords"

    def generate_password(self, password):
        return sha256.hash(password)

    def verify_hash(self, password, hash):
        return sha256.verify(password, hash)


class AdminManagement:
    def __init__(self):
        self.todo = ""
        self.collection_name = "admins"
        self.db = Database()

    def login_admin(self, email, password):
        admin = self.db.find(self.collection_name, {
            "email": email,
            "password": password
        })
        print(self.dump(admin))
        return self.dump(admin)

    def find_admin(self, email):
        admin = self.db.find(self.collection_name, {"email": email})
        return self.dump(admin)

    def get_all_admins(self):
        pass

    def create_admin(self, first_name, last_name, email):
        print('intentando crear admin')
        admin = self.db.create(self.collection_name, ( {
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        } ))
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

    def dump(self, data):
        return AdminSchema(exclude=['_id']).dump(data).data
