from flask_restplus import Api, Namespace, Resource
# When you finish your class, add it under this one.
import .product as product
import .order as order
# Keep this as is for now
api = Api(
    version="1.0", 
    title="eCommerce API", 
    description="Bundle of API that feed the eCommerce website"
)

# After you import your namespaces, import them into the API
api.add_namespace(product.any_ns)
api.add_namespace(product.admin_ns)
api.add_namespace(order.any_ns)
api.add_namespace(order.admin_ns)

# We will probably add in Blueprinting for versioning of API, but Blueprinting for now should be unnecessary
