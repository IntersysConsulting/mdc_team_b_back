from marshmallow import Schema, fields
from ..token.schema import ResetTokenSchema


class AdminSchema(Schema):
    _id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    enabled = fields.Bool(required=True)
    reset_token = fields.Nested(ResetTokenSchema)
