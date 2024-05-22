from marshmallow import fields, validate
from schemas import ma
from schemas.productSchema import ProductIdSchema

class ProductionSchema(ma.Schema):
    id = fields.Integer(required=False) 
    product_id = fields.Integer(required=True)
    quantity_produced = fields.Integer(required=True, validate=validate.Range(min=1))
    date_produced = fields.Date(required=True)
    product = fields.Nested("ProductIdSchema", required=False)

    class Meta:
        fields = ("id", "product_id", "quantity_produced", "date_produced", "product")

production_schema = ProductionSchema()
production_schemas = ProductionSchema(many=True)