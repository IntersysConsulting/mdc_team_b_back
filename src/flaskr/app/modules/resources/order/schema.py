from marshmallow import Schema, fields
from ..customer.schema import BillingAddressSchema, ShippingAddressSchema


class OrderProductSchema(Schema):
    name = fields.Str()
    unitary_price = fields.Int()
    digital = fields.Bool()
    quantity = fields.Int()


class OrderSchema(Schema):
    _id = fields.Str()
    customer_id = fields.Str()
    status = fields.Str()
    products = fields.List(fields.Nested(OrderProductSchema))
    total = fields.Int()
    billing_address = fields.Nested(BillingAddressSchema)
    shipping_address = fields.Nested(ShippingAddressSchema)
    payment = fields.Str()