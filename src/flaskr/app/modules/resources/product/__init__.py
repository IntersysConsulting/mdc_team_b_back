from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import ProductSchema

# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware.
# Validate operation logic here, not permission to access it.


class UserProduct():
    def __init__(self):
        self.collection_name = "products"

    def GetOne(self):
        pass

    def GetAll(self):
        pass

    def GetProducts(self, filter, sort, ascending=True, page=0):
        print("Trying to get all products with {} as filter and {} as sort".
              format(filter, sort))
        db = Database()
        output = []
        products = db.find_all(self.collection_name,
                               {'name': {
                                   '$regex': r'[a-zA-Z]*'
                               }}, sort, ascending, page)
        for product in products:
            output.append(self.dump(product))
        return 1

    def dump(self, data):
        return ProductSchema(exclude=['_id']).dump(data).data


class AdminProduct(UserProduct):
    def __init__(self):
        self.todo = "Implement this class with actions only an admin can do"

    def create_product(self, name, price, image, digital, comment=""):
        pass

    def delete_product(self, id):
        pass

    def update_product(self, id, name, price, image, digital, comment=""):
        pass
