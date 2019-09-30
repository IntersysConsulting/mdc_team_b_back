from marshmallow import Schema, fields


class CartProductSchema(Schema):
    product = fields.String()
    quantity = fields.Int()


class CartSchema(Schema):
    _id = fields.String()
    user = fields.String()
    last_updated = fields.Time()
    products = fields.List(fields.Nested(CartProductSchema))