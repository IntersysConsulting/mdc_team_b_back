from .mongo import Mongo

_Page_Size = 10

class Database(object):
    def __init__(self, adapter=Mongo):
        self.client = adapter()        
        
    def find_all(self, table, selector, sort, asc=True, next_page=0, page_size = _Page_Size):
        return self.client.find_all(table, selector, sort, asc, next_page, page_size)
    def find  (self, table, selector):
        return self.client.find(table, selector)
    
    def create(self, table, element):
        return self.client.create(table, element)
    def update(self, table, selector, element):
        return self.client.update(table, selector, element)
    def delete(self, table, selector):
        return self.client.delete(table, selector)