from .mongo import Mongo

_Page_Size = 10


class Database(object):
    def __init__(self, adapter=Mongo):
        self.client = adapter()

    def find_all(self,
                 table,
                 selector,
                 sort,
                 asc=True,
                 next_page=0,
                 page_size=None):
        get_page_size = _Page_Size if page_size == None else page_size
        print(
            "Querying with table: {} selector: {} sort: {} page:{} page_size:{}"
            .format(table, selector, sort, next_page, get_page_size))
        result = self.client.find_all(table, selector, sort, asc, next_page,
                                      get_page_size)
        print("The database returned {} results".format(len(result)))
        return result

    def get_count(self, table, selector):
        return self.client.get_count(table, selector)

    def find(self, table, selector):
        return self.client.find(table, selector)

    def create(self, table, element):
        return self.client.create(table, element)

    def update(self, table, selector, element):
        return self.client.update(table, selector, element)

    def delete(self, table, selector):
        return self.client.delete(table, selector)

    def aggregate(self, table, query):
        return self.client.aggregate(table, query)