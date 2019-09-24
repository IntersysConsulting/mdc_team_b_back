import unittest
# from app.modules.resources.admin import AdminManagement
from app.modules.resources.product import AdminProduct
from pymongo.errors import DuplicateKeyError


class ProductResourceTestCase(unittest.TestCase):
    def getProducts(self):
        pm = AdminProduct()
        self.assertIn("sample_product", pm.getProducts())

    # def login(self, email, password):
    #     am = AdminManagement()
    #     return am.login_admin(email, password)

    # def register(self, email, password, first_name, last_name):
    #     am = AdminManagement()
    #     return am.create_admin(first_name, last_name, email, password)

    # def find(self, email):
    #     am = AdminManagement()
    #     return am.find_admin(email)

    # def test_create_admin(self):
    #     self.assertEqual(
    #         {},
    #         self.register("burrito@email.com", "password", "Bu", "rrito"),
    #     )

    # def test_find_admin(self):
    #     rv = self.find("burrito@email.com")
    #     self.assertEqual(
    #         rv, {
    #             "last_name": "rrito",
    #             "first_name": "Bu",
    #             "email": "burrito@email.com",
    #             "password": "password",
    #         })
