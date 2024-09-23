from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class SignupSchema(Schema):
    fullName = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_schema = LoginSchema()
signup_schema = SignupSchema()
