from flask import jsonify
from flask_restplus import Resource
from ...db import Database

# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware. 
# Validate operation logic here, not permission to access it.  

class UserOrder(): 
    
    def __init__(self): 
        self.collection_name = "orders"

    def add(self, user, shipping, billing, items, timestamp):
        pass

    def GetUserOrders(self, user, filter, sort, ascending=True, page=0):         
        Database.find_all(self.collection_name, {'field':{'$regex':r'^the-regex'}}, sort, ascending, page)
        pass


class AdminOrder(): 
    def __init__(self): 
        self.todo = "Implement this class with actions only an admin can do"

    def GetAll(self, filter, sort, ascending=True, page=0):
        Database.find_all(self.collection_name, {'field':{'$regex':r'^the-regex'}}, sort, ascending, page)
        pass
    
    def change_order_status(self, id, status): 
        pass

    