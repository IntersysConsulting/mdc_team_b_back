from flask import jsonify
from ...db import Database
from .schema import ProductSchema
from datetime import datetime
from bson.objectid import ObjectId
# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware.
# Validate operation logic here, not permission to access it.


class UserProduct():
    def __init__(self):
        self.collection_name = "products"
        self.db = Database()

    def GetOne(self, id):
        return self.db.find(self.collection_name, {"_id": ObjectId(id)})

    # def GetAll(self):
    #     pass

    def GetProducts(self, filter, sort, ascending=True, page=0, page_size=None):
        output = []
        selector = {'name': {'$regex': r''}}

        total = self.db.get_count(self.collection_name, selector )
        print("The total I got was {}".format(total))
        products = self.db.find_all(self.collection_name,
                                    selector, sort, ascending, page, page_size=page_size)
        for product in products:
            output.append(self.dump(product))

        return output, total

    def dump(self, data):
        return ProductSchema().dump(data).data


class AdminProduct():
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
        print("Deleting the product {}".format(id))

        found_an_item = self.db.find(self.collection_name,
                                     {"_id": ObjectId(id)})
        items = self.db.delete(self.collection_name, {"_id": ObjectId(id)})
        print("Deleted {} coincidences".format(items))
        response = items if found_an_item else -1
        return response

    def update_product(self, id, name, price, img, digital, description=""):
        print("Updating {}.".format(id))
        found_item = self.db.find(self.collection_name, {"_id": ObjectId(id)})

        if found_item:
            _name = found_item["name"] if name == None else name
            _price = found_item["price"] if price == None else price
            _img = found_item["img"] if img == None else img
            _digital = found_item["digital"] if digital == None else digital
            _description = found_item[
                "description"] if description == None else description
            now = datetime.now()

            result = self.db.update(self.collection_name,
                                    {"_id": ObjectId(id)}, {
                                        "$set": {
                                            "name": _name,
                                            "price": _price,
                                            "img": _img,
                                            "digital": _digital,
                                            "description": _description,
                                            "modified_at": now
                                        }
                                    })

        else:
            result = -1

        return result
