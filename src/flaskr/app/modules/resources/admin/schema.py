from marshmallow import Schema, fields
from ..reset_token.schema import ResetTokenSchema


class AdminSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    reset_token = fields.Nested(ResetTokenSchema)
    last_login = fields.DateTime(required=True)