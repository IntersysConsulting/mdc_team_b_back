from marshmallow import Schema, fields


class ResetTokenSchema(Schema):
    token = fields.String(required=True)
    codeAccess = fields.String(required=True)
    tries = fields.String(required=True)
