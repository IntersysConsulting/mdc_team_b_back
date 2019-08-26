from flask_restplus import Api, Namespace, Resource
from .product import any_ns, admin_ns 



api = Api(
    version="1.0", 
    title="eCommerce API", 
    description="Bundle of API that feed the eCommerce website"
)

api.add_namespace(any_ns)
api.add_namespace(admin_ns)


