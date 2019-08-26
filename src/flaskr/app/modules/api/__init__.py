from flask_restplus import Api, Namespace, Resource
# When you finish your class, add it under this one.
from .product import any_ns, admin_ns 

# Keep this as is for now
api = Api(
    version="1.0", 
    title="eCommerce API", 
    description="Bundle of API that feed the eCommerce website"
)

# After you import your namespaces, import them into the API
api.add_namespace(any_ns)
api.add_namespace(admin_ns)

# We will probably add in Blueprinting for versioning of API, but Blueprinting for now should be unnecessary
