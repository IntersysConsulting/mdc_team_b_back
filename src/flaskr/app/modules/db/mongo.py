import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from urllib.parse import quote_plus



class Mongo:
    def __init__(self):
        protocol = 'mongodb+srv://'
        user, password = 'ibp-user', 'LuvOUo9Zcadyl8xc'
        server = 'teamb-cluster-ogtju.mongodb.net'
        options = 'test?retryWrites=true&w=majority'
        database = 'ecommerce'

        mongo_url = "{0}{1}:{2}@{3}/{4}".format(protocol, user, password, server, options)
        # protocol = 'mongodb://'
        # user = 'intersys'
        # password = 's3cureP@ssw0rd'
        # server = '127.0.0.1'
        # port = '27001'        
        # database = webproject
        # mongo_url = protocol + user + ':' + quote_plus(password) + '@' + server + ':' + port

        self.db = MongoClient(mongo_url)[database]

    def find_all(self, table, selector, sort, _ascending, _next_page, _page_size):  
        if(sort!=None):
            # If it requires sorting
            sortType = ASCENDING if _ascending else DESCENDING            
            return self.db[table].find(selector).sort(sort, sortType).skip(_next_page*_page_size).limit(_page_size)
        # If it is unsorted             
        return self.db[table].find(selector).skip(_next_page*_page_size).limit(_page_size)

    def find(self, table, selector):        
        return self.db[table].find_one(selector)

    def create(self, table, user):
        return self.db[table].insert_one(user)
        
    def update(self, table, selector, user):
        return self.db[table].replace_one(selector, user).modified_count

    def delete(self, table, selector):
            return self.db[table].delete_one(selector).deleted_count