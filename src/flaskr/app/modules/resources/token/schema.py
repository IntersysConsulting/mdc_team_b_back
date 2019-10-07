from marshmallow import Schema, fields


class ResetTokenSchema(Schema):
    access_code = fields.String(required=True)
    attempts = fields.String(required=True)
