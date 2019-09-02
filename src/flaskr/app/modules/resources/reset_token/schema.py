from marshmallow import Schema, fields


class ResetTokenSchema(Schema):
    token = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
