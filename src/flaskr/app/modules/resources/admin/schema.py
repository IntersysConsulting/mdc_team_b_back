from marshmallow import Schema, fields
from ..reset_token.schema import ResetTokenSchema


class AdminSchema(Schema):
    _id = fields.String()
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    reset_token = fields.Nested(ResetTokenSchema)
    last_login = fields.DateTime(required=True)
    enable = fields.Bool(required=True)
