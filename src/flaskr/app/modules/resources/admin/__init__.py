from flask import jsonify
from flask_restplus import Resource
from ...db import Database

# This section is a draft for ideas, will be formally worked on later on.

class PasswordManagement():
    def __init__(self):
        self.todo = "Handle additional methods used for administration of passwords"

    def generate_password(self):
        pass

    def hash_pass(self, password):
        pass
    

class AdminManagement(): 
    def __init__(self): 
        self.todo = ""

    def get_all_admins(self):
        pass

    def create_admin(self, name, email, password, comment=""): 
        pass 

    def delete_admin(self, id): 
        pass

    def update_admin(self, id, name, password, comment=""): 
        pass

    