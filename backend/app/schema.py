from marshmallow import Schema, ValidationError, fields, validates_schema


class LoginSchema(Schema):
    usernameOrEmail = fields.String(required=True)
    password = fields.String(required=True)

    @validates_schema
    def validate_login(self, data, **kwargs):
        if not data.get("usernameOrEmail"):
            raise ValidationError("Email or username must be provided")
        if not data.get("password"):
            raise ValidationError("Password must be provided.")


class SignupSchema(Schema):
    fullName = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


login_schema = LoginSchema()
signup_schema = SignupSchema()
