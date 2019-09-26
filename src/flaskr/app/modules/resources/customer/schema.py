from marshmallow import Schema, fields
from ..reset_token.schema import ResetTokenSchema


class ShippingAddressSchema(Schema):
    address = fields.String()
    between = fields.String()
    country = fields.String()
    state = fields.String()
    city = fields.String()
    zip_code = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    delivery_notes = fields.String()


class BillingAddressSchema(Schema):
    address = fields.String()
    country = fields.String()
    state = fields.String()
    city = fields.String()
    zip_code = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class CustomerSchema(Schema):
    _id = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    password = fields.String()
    reset_token = fields.Nested(ResetTokenSchema)
    phone = fields.String()
    terms_of_service_ts = fields.Time()
    is_guest = fields.Bool()
    shipping_addresses = fields.List(fields.Nested(ShippingAddressSchema))
    billing_addresses = fields.List(fields.Nested(BillingAddressSchema))
    cart = fields.String()
