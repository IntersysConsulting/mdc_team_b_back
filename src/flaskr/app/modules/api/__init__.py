from flask_restplus import Api, Namespace, Resource
# When you finish your class, add it under this one.
from .product import any_ns as product_any, admin_ns as product_admin
from .order   import user_ns as order_user, admin_ns as order_admin, any_ns as order_guest
from .cart    import any_ns as cart_any


# Keep this as is for now
api = Api(
    version="1.0", 
    title="eCommerce API", 
    description="Bundle of API that feed the eCommerce website"
)

# After you import your namespaces, import them into the API
api.add_namespace(product_any)
api.add_namespace(product_admin)
api.add_namespace(order_guest)
api.add_namespace(order_user)
api.add_namespace(order_admin)
api.add_namespace(cart_any)


# We will probably add in Blueprinting for versioning of API, but Blueprinting for now should be unnecessary
