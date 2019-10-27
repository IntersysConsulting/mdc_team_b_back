import re
from flask import jsonify
from bson.objectid import ObjectId
from ..order import UserOrder
from ...db import Database
import stripe

stripe.api_key = "sk_test_Xq8C5Ra3nT5aW4PRgrXtQgJv00O7Sw81wo"

class CardManager(object):
    def __init__(self):
        self.orders_status = UserOrder().statuses
        self.collection_name = "customers"
        self.db = Database()


    def add_stripe_id(self, user, record):
        customer = stripe.Customer.create(
            name='{} {}'.format(record['first_name'], record['last_name']),
            email=record['email'],
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
        Add a new card to scripe account, token must be returned by Stripe.js.
        This also will make the new card the default resource
            -2 the user is a guest
            -1  unexpected error
            0   card was added succesfully
        '''

        result = 0
        record = self.db.find(self.collection_name, {"_id": ObjectId(user)})
        if record['is_guest'] is True:
            result = -2
            print(r"A guest can't do this")

        if len(record) and not result :
            if not 'stripe_id' in record:
                result = (self.add_stripe_id(user, record)) * -1 
                record = self.db.find(self.collection_name, {"_id": ObjectId(user)})
            if not result:
                source = stripe.Customer.create_source(
                    record['stripe_id'],
                    source=token
                )
                if result is not -1:
                    stripe.Customer.modify(
                        record['stripe_id'],
                        default_source=source['id']
                    )

        return result

    def get_cards(self, user):
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

    def put_charge_customer(self, user, order_id, card_id):
        '''
        -3  insuficient founds
        -2  card_id format's is wrong
        -1  unexpected error
        0   card was added succesfully
        '''
        error = 0
        verify = re.compile(r'.*card_.*')
        if verify.match(card_id) is None:
            error = -2

        if not error:
            record = self.db.find(self.collection_name, {'_id': ObjectId(user)})
            order = self.db.find('orders', {'_id': ObjectId(order_id)})
            try:
                charge = stripe.Charge.create(
                    amount=order['total'],
                    currency='usd',
                    source=card_id,
                    customer=record['stripe_id']
                )
                if isinstance(charge, stripe.Charge):
                    self.db.update('orders', {"_id": ObjectId(order_id)},
                        {
                            '$set': {
                                'stripe_charge': charge['id'],
                                'status':ObjectId(self.orders_status['Awaiting Fulfillment'])                           
                            }
                        }
                    )

                    print(self.db.find('orders', {'_id': ObjectId(order_id)}))

                else:
                    self.db.update('orders', {"_id": ObjectId(order_id)},
                        {
                            '$set': {  
                                'status':ObjectId(self.orders_status['Declined'])
                            }
                        }
                    )
                    error = -3
            except (stripe.error.InvalidRequestError) as err :
                error = -1
                err_str = err if isinstance(err, stripe.error.InvalidRequestError) else 'The user does not have a registered card'
                print(err_str)
        return error

    def put_charge_guest(self, order_id, token):
        '''
        -3  insuficient founds
        -2  card_id format's is wrong
        -1  unexpected error
        0   card was added succesfully
        '''
        error = 0
        verify = re.compile(r'.*tok_.*')
        if verify.match(token) is None:
            error = -2

        if not error:
            try:
                order = self.db.find('orders', {'_id': ObjectId(order_id)})
                charge = stripe.Charge.create(
                    amount=order['total'],
                    currency='usd',
                    source=token
                )

                if isinstance(charge, stripe.Charge):
                    self.db.update('orders', {"_id": ObjectId(order_id)},
                        {
                            '$set': {  
                                'stripe_charge': charge['id'],
                                'status':ObjectId(self.orders_status['Awaiting Fulfillment'])
                            }
                        }
                    )
                else:
                    self.db.update('orders', {"_id": ObjectId(order_id)},
                        {
                            '$set': {  
                                'status':ObjectId(self.orders_status['Declined'])
                            }
                        }
                    )
                    error = -3
            except (stripe.error.InvalidRequestError) as err :
                error = -1
                err_str = err if isinstance(err, stripe.error.InvalidRequestError) else 'The user does not have a registered card'
                print(err_str)
        return error


    def whos_paying(self, user):
        record = self.db.find(self.collection_name, {'_id': ObjectId(user)})
        if record['is_guest'] is True:
            return False
        return True