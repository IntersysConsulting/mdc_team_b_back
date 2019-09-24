from marshmallow import Schema, fields


class ProductSchema(Schema):
    _id = fields.String()
    name = fields.String()
    price = fields.Int()
    img = fields.String()
    description = fields.String()
    digital = fields.Bool()
    created_at = fields.Time()
    modified_at = fields.Time()
