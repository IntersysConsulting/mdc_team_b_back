from ...db import Database
from bson.objectid import ObjectId
from datetime import datetime


class CartManager():
    def __init__(self):
        self.collection_name = "carts"
        self.db = Database()

    def put_in_cart(self, customer_id, product_id, quantity):
        cart = self.db.find(self.collection_name,
                            {"user": ObjectId(customer_id)})
        if cart == None:
            # Cart doesn't exist, make a new cart
            print(
                "The customer {} does not have a cart yet, making one for it.".
                format(customer_id))
            cart_id = self.make_new_cart(customer_id)
            # Since the cart is new we must push a value
            command = "$push"
            where = "products"
        else:
            cart_id = cart["_id"]
            #This line makes a list with all the product ids, then asks what the index of the product_id is.
            try:
                index_to_insert_on = [x['product'] for x in cart['products']
                                      ].index(product_id)
                # Updates a field
                command = "$set"
                where = "products.{}".format(index_to_insert_on)
            except:
                # .index raises an exception if the value doesn't exist on the array, so, it means we must push instead of $set
                command = "$push"
                where = "products"

        result = self.db.update(
            self.collection_name, {"_id": ObjectId(cart_id)},
            {command: {
                where: {
                    "product": product_id,
                    "quantity": quantity
                }
            }})
        print("Tried to {} the product in the cart and resulted on {}".format(
            command, result))
        return result

    def make_new_cart(self, customer_id):
        now = datetime.now()
        result = self.db.create(self.collection_name, {
            "user": ObjectId(customer_id),
            "last_updated": now,
            "products": []
        })
        return result.inserted_id

    # def find_index_of_product_in_cart(self, product, cart):
    #     self.db.aggregate(self.collection_name, {
    #         "_id": ObjectId(cart),
    #     })
