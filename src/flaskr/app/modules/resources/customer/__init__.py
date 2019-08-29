from flask import jsonify
from flask_restplus import Resource
from ...db import Database

# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware. 
# Validate operation logic here, not permission to access it.  

class Customer(): 
    
    def __init__(self): 
        self.collection_name = "orders"

    def add(self, name, email, pwd, timestamp, is_guest, phone, ToS, reset):#could be just self, user_obj, idk if timestamp doesn't go here
        pass

    def updateInfo(self, user_id, user_obj):
        pass

    def GetUserData(self, user_id):         
        Database.find_all(self.collection_name, user_id)
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

    