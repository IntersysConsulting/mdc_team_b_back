from marshmallow import Schema, fields


class AdminSchema(Schema):
    _id = fields.String()
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    last_login = fields.DateTime(required=True)
    enabled = fields.Bool(required=True)
