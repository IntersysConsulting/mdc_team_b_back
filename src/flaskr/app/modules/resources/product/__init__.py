from flask import jsonify
from ...db import Database
from .schema import ProductSchema
from datetime import datetime
from bson.objectid import ObjectId
import re
# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware.
# Validate operation logic here, not permission to access it.


class UserProduct():
    def __init__(self):
        self.collection_name = "products"
        self.db = Database()

    def get_one(self, id):
        return self.dump(
            self.db.find(self.collection_name, {"_id": ObjectId(id)}))

    def make_search(self, search):
        pattern = '.*' + re.escape(search) + '.*'
        return re.compile(pattern, re.IGNORECASE)

    def get_products(self,
                     search,
                     digital,
                     sort,
                     ascending=True,
                     page=0,
                     page_size=None):
        output = []
        if search != None:
            selector = {'name': self.make_search(search)}
        else:
            selector = {'name': {'$regex': r''}}

        if digital == 1:
            selector['digital'] = True
        elif digital == -1:
            selector['digital'] = False

        total = self.db.get_count(self.collection_name, selector)

        products = self.db.find_all(self.collection_name,
                                    selector,
                                    sort,
                                    ascending,
                                    page,
                                    page_size=page_size)
        for product in products:
            output.append(self.dump(product))

        return output, total

    def dump(self, data):
        return ProductSchema().dump(data).data


class AdminProduct():
    def __init__(self):
        self.collection_name = "products"
        self.db = Database()

    def create_product(self, name, price, img, digital, description):
        now = datetime.now()
        new_product = self.make_product(name,
                                        price,
                                        img,
                                        digital,
                                        description,
                                        created_at=now,
                                        modified_at=now)
        print("The new product is {}".format(new_product))

        return self.db.create(self.collection_name, new_product)

    def delete_product(self, id):
        print("Deleting the product {}".format(id))

        found_an_item = self.db.find(self.collection_name,
                                     {"_id": ObjectId(id)})
        if found_an_item:
            response = self.db.delete(self.collection_name,
                                      {"_id": ObjectId(id)})
        else:
            response = -1
        return response

    def update_product(self, product_id, name, price, img, digital,
                       description):
        print("Updating {}.".format(product_id))
        found_item = self.db.find(self.collection_name,
                                  {"_id": ObjectId(product_id)})

        if found_item:
            new_product = self.make_product(name,
                                            price,
                                            img,
                                            digital,
                                            description,
                                            modified_at=datetime.now())
            response = self.db.update(self.collection_name,
                                      {"_id": ObjectId(product_id)},
                                      {"$set": new_product})
        else:
            response = -1

        return response

    def make_product(self,
                     name,
                     price,
                     img,
                     digital,
                     description,
                     created_at=None,
                     modified_at=None):
        product = {}
        if not name == None:
            product['name'] = name
        if not price == None:
            product['price'] = int(price)
        if not img == None:
            product['img'] = img
        if not digital == None:
            product['digital'] = digital
        if not description == None:
            product['description'] = description
        if not created_at == None:
            product['created_at'] = created_at
        if not modified_at == None:
            product['modified_at'] = modified_at
        return product