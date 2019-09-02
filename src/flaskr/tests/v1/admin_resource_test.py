import unittest
# from app.modules.resources.admin import AdminManagement
from ...app.modules.resources.admin import AdminManagement


class MyFirstTest(unittest.TestCase):
    def Login(self, email, password):
        AdminManagement.login_admin(email, password)
        self.assertEqual()

    def test_register(self):
        rv = self.register()