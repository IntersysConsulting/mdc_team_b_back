import unittest
# from app.modules.resources.admin import AdminManagement
from app.modules.resources.admin import AdminManagement


class AdminResourceTestCase(unittest.TestCase):
    def login(self, email, password):
        am = AdminManagement()
        return am.login_admin(email, password)

    def register(self, email, first_name, last_name):
        am = AdminManagement()
        return am.create_admin(first_name, last_name, email)

    def find(self, email):
        am = AdminManagement()
        return am.find_admin(email)

    def test_register(self):
        self.register("burrito@email.com", "Bu", "rrito")
        rv = self.find("burrito@email.com")
        del rv['_id']

        self.assertDictEqual(
            rv, {
                "last_name": "rrito",
                "first_name": "Bu",
                "email": "burrito@email.com",
                "enabled" : True
            })

