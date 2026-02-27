from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserOutSchema(Schema):
    id = fields.Int()
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()