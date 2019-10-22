from flask import jsonify
from bson.objectid import ObjectId
from ...db import Database
import stripe

stripe.api_key = "sk_test_wCw3IAbkVh8jar3XopHWW6IB00FzBJsAya"

class CardManager(object):
    def __init__(self):
        self.collection_name = "customers"
        self.db = Database()


    def add_stripe_id(self, user):
        customer = stripe.Customer.create(
            description='Stripe Customer account for {}'.format(user)
        )
        
        return not self.db.update(self.collection_name, {"_id": ObjectId(user)},
                        { "$set": {
                                "stripe_id" : customer.id
                            }
                        }
        ) 

    def add_card(self, user, token):        
        '''
        Add a new card to scripe account, token must be returned by Stripe.js
            -1  unexpected error
            0   card was added succesfully
        '''

        result = 0
        record = self.db.find(self.collection_name, {"_id": ObjectId(user)})
        if len(record):
            if not 'stripe_id' in record:
                result = (self.add_stripe_id(user)) * -1 
                record = self.db.find(self.collection_name, {"_id": ObjectId(user)})
            if not result:
                if stripe.Customer.create_source(
                    record['stripe_id'],
                    source=token
                ) is None:
                    result = -1
        return result

    def get_cards(self, user, limit=10):
        '''
        This endpoint it's gonna return all the customer's info
        '''

        record = self.db.find(self.collection_name, {'_id': ObjectId(user)})
        try:
            customer = stripe.Customer.retrieve(record['stripe_id'])
        except KeyError:
            customer = None
        return customer

    def delete_card(self, user, card_id):
        '''
        Delete card from stripe account, this is action is performed
        using the card id. Will return true if the card was deleted
        '''
        record = self.db.find(self.collection_name, {'_id': ObjectId(user)})
        try:
            response = stripe.Customer.delete_source(
                record['stripe_id'],
                card_id
            )['deleted']
        except KeyError:
            response = False
    
        return response