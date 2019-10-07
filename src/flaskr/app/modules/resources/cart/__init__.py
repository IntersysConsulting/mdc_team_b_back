from ...db import Database
from bson.objectid import ObjectId
from datetime import datetime
from .schema import CartSchema
from ...resources.product import UserProduct

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
            try:
                #This line makes a list with all the product ids, then asks what the index of the product_id is.
                products = [str(x['product']) for x in cart['products']]
                index_to_insert_on = products.index(product_id)
                command = "$set"
                where = "products.{}".format(index_to_insert_on)
            except:
                # .index raises an exception if the value doesn't exist on the array, so, it means we must push instead of $set
                command = "$push"
                where = "products"


        result = self.db.update(self.collection_name,
                                {"_id": ObjectId(cart_id)}, {
                                    command: {
                                        where: {
                                            "product": ObjectId(product_id),
                                            "quantity": quantity
                                        }
                                    }
                                })

        print("Tried to {} the product in the cart and resulted on {}".format(
            command, result))
        return result, self.get_cart_info(cart_id)

    def make_new_cart(self, customer_id):
        now = datetime.now()
        result = self.db.create(self.collection_name, {
            "user": ObjectId(customer_id),
            "last_updated": now,
            "products": []
        })
        # Also updates the customer with their cart ID
        self.db.update("customers", {"_id": ObjectId(customer_id)},
                       {"$set": {
                           "cart": ObjectId(result.inserted_id)
                       }})
        return result.inserted_id

    def get_cart_info(self, cart_id):
        cart = self.db.find(self.collection_name, {"_id": ObjectId(cart_id)})
        products = [x['quantity'] for x in cart['products']]
        total = sum(products)
        unique = (len(products))
        return total, unique

    def get_cart(self, user):
        up = UserProduct()
        cart = CartSchema(exclude=['_id', 'user']).dump(
            self.db.find(self.collection_name, {"user": ObjectId(user)})).data 

        product_list = []         
        for product in cart['products']:
            print("Product = {}".format(product))
            _product =  up.get_one(product["product"])
            product_list.append({
                "_id":_product["_id"], 
                "price":_product["price"], 
                "image":_product["img"], 
                "name":_product["name"], 
                "quantity":product["quantity"]
            })

        cart["products"] = product_list
        print("The cart is {}".format(cart))
        return cart

    def delete_cart(self, user, pid, cart):
        '''
        In this case result will be:
            -1 unexpected error
            0 if the product was not in the cart
            1 if the item could be erased from the cart
            2 if the product did not exist
        '''
        result = 0
        us = UserProduct()

        cart_id = self.db.find(self.collection_name,
                            {"user": ObjectId(user)})['_id']

        #self.db.delete(self.collection_name, {"user": ObjectId(user)})

        if not us.get_one(pid) :
            result = 2
        else:
            try:
                products = [str(x['product']) for x in cart['products']]
                index_to_insert_on = products.index(pid)
                command = "$pull"
                where = "products"

                print(index_to_insert_on)

                result = self.db.update(self.collection_name,
                                {"_id": ObjectId(cart_id)}, {
                                    command: {
                                        where: {
                                            "product": ObjectId(pid)
                                        }
                                    }
                                })


            except:
                print('There is no product {} in the cart'.format(pid))
                result = 0

        return result

    def empty_cart(self, customer_id):
        '''
        Empties the customer's cart after doing a purchase
        '''
        cart = self.db.find(self.collection_name, {"user":ObjectId(customer_id)})
        if cart != None:
            response = self.db.update(self.collection_name, {"user":ObjectId(customer_id)}, {"$set":{"products":[]}})
        else:
            # User does not have a cart
            response = -1
        return response
