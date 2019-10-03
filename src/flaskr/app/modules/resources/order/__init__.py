from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from datetime import datetime
from bson.objectid import ObjectId
from ..cart import CartManager
from ..product import UserProduct
from ..customer import CustomerManager
# In this file we implement methods that serve as a middle point between the exposed endpoint and the
# actual middleware.
# Validate operation logic here, not permission to access it.


class UserOrder():
    def __init__(self):
        self.collection_name = "orders"
        self.db = Database()
        tmp_statuses = self.db.find_all("order_statuses", {})
        self.statuses = {}
        for i in range(len(tmp_statuses)):
            key = tmp_statuses[i]["name"]
            value = str(tmp_statuses[i]["_id"])
            self.statuses[key] = value

    def find_in_checkout_order(self, user_id):
        return self.db.find(
            self.collection_name, {
                "customer_id": ObjectId(user_id),
                "status": ObjectId(self.statuses["In checkout"])
            })

    def make_order(self, cart, user_id):
        '''
        Returns an order dictionary based off a user's cart
        '''
        up = UserProduct()

        products_in_cart = cart["products"]
        products_in_order = []
        total = 0
        #Here's a mess of variables:
        #   products_in_cart = Product list gotten from the cart, includes product id and quantity
        #   cart_product = iterator of products_in_cart, used to get quantity
        #   db_product = Product from the database, includes name, price and digital, gotten from the _id in cart_product
        #   products_in_order = Output list of all the order_product variant of products

        for cart_product in products_in_cart:
            db_product = up.GetOne(cart_product["product"])
            # This is an instance of a product in the order
            order_product = {
                "name": db_product["name"],
                "unitary_price": db_product["price"],
                "digital": db_product["digital"],
                "quantity": cart_product["quantity"]
            }
            # Add up the total of the order
            total += db_product["price"] * cart_product["quantity"]
            # Append the product to the order
            products_in_order.append(order_product)
        # After all the items have been added to the order we finish it up
        new_order = {
            "customer_id": ObjectId(user_id),
            "status": ObjectId(self.statuses["In checkout"]),
            "products": products_in_order,
            "total": total
        }

        return new_order

    def checkout_order(self, user_id):
        cm = CartManager()
        cart = cm.get_cart(user_id)
        if self.find_in_checkout_order(user_id) != None:
            # User already has an order in checkout
            response = -2
        elif not cart:
            # User has no cart, we can't issue an order
            response = -1
        else:
            # User can checkout this order
            order = self.make_order(cart, user_id)
            response = 1 if self.db.create(self.collection_name,
                                           order) != None else 0

        return response

    def finish_order(self, user_id, shipping, billing, payment):
        # TODO: Implement payment
        order = self.find_in_checkout_order(user_id)
        if order == None:
            #Customer didn't POST before PUTting
            response = -1
        else:
            cm = CustomerManager()
            customer = cm.get_data(user_id)
            billing_address = customer["billing_addresses"][billing]
            shipping_address = customer["shipping_addresses"][shipping]
            response = self.db.update(
                self.collection_name, {"_id": order["_id"]}, {
                    "$set": {
                        "billing_address": billing_address,
                        "shipping_address": shipping_address,
                        "payment": payment
                    }
                })

        return response

    def GetUserOrders(self, user_id, filter, sort, ascending=True, page=0):
        Database.find_all(self.collection_name,
                          {'field': {
                              '$regex': r'^the-regex'
                          }}, sort, ascending, page)
        pass


class AdminOrder():
    def __init__(self):
        self.todo = "Implement this class with actions only an admin can do"

    def GetAll(self, filter, sort, ascending=True, page=0):
        Database.find_all(self.collection_name,
                          {'field': {
                              '$regex': r'^the-regex'
                          }}, sort, ascending, page)
        pass

    def change_order_status(self, id, status):
        pass
