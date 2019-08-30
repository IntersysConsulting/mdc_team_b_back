from flask_restplus import Api, Namespace, Resource
# When you finish your class, add it under this one.
from .product import any_ns as product_any, admin_ns as product_admin
from .order import user_ns as order_user, admin_ns as order_admin
from .cart import any_ns as cart_any
from .customer import guest_ns as customer_guest, customer_ns as customer_user
# from .admin import admin_ns as management_admin
from .admin import admin_ns as management_admin

# Keep this as is for now
api = Api(version="1.0",
          title="eCommerce API",
          description="Bundle of API that feed the eCommerce website")

# After you import your namespaces, import them into the API

# Please load these in alphabetical order for Swagger

###################################
#   User Namespaces
###################################
api.add_namespace(cart_any)
api.add_namespace(customer_user)
api.add_namespace(customer_guest)
# api.add_namespace(order_user)
# api.add_namespace(product_any)
###################################
#   Admin Namespaces
###################################
api.add_namespace(management_admin)
# api.add_namespace(product_admin)
# api.add_namespace(order_admin)

# We will probably add in Blueprinting for versioning of API, but Blueprinting for now should be unnecessary
