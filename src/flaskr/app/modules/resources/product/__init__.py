from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from .schema import ProductSchema
from datetime import datetime

# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware.
# Validate operation logic here, not permission to access it.


class UserProduct():
    def __init__(self):
        self.collection_name = "products"
        self.db = Database()

    def GetOne(self):
        pass

    def GetAll(self):
        pass

    def GetProducts(self, filter, sort, ascending=True, page=0):
        print("Trying to get all products with {} as filter and {} as sort".
              format(filter, sort))
        output = []
        products = self.db.find_all(self.collection_name,
                                    {'name': {
                                        '$regex': r'[a-zA-Z]*'
                                    }}, sort, ascending, page)
        for product in products:
            output.append(self.dump(product))
        return output

    def dump(self, data):
        return ProductSchema(exclude=['_id']).dump(data).data


class AdminProduct(UserProduct):
    def __init__(self):
        self.collection_name = "products"
        self.db = Database()

    def create_product(self, name, price, img, digital, description=""):
        now = datetime.now()
        new_product = {
            "name": name,
            "price": price,
            "img": img,
            "description": description,
            "digital": digital,
            "created_at": now,
            "modified_at": now
        }
        print("The new product is {}".format(new_product))
        items = self.db.create(self.collection_name, new_product)
        print("The database returned {}".format(items))

        return items

    def delete_product(self, id):
        pass

    def update_product(self, id, name, price, img, digital, description=""):
        pass
