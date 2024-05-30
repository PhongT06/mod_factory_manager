from marshmallow import fields
from schemas import ma

class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)


users_schema = UserSchema(many=True, exclude=["password"])
