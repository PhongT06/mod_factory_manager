from marshmallow import fields, validate
from schemas import ma

class EmployeeSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    position = fields.String(required=True, validate=validate.Length(min=2, max=100))

    class Meta:
        fields = ("id", "name", "position")

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)