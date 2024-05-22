from flask import request, jsonify
from schemas.productionSchema import production_schema, production_schemas
from services import productionService
from marshmallow import ValidationError

def save():
    try:
        production_data = production_schema.load(request.json)
        production_save = productionService.save(production_data)
        return production_schema.jsonify(production_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

def find_all():
    production_records = productionService.find_all()
    return production_schemas.jsonify(production_records), 200

def find_by_id(production_id):
    production_record = productionService.find_by_id(production_id)
    if production_record:
        return production_schema.jsonify(production_record), 200
    else:
        return jsonify({'error': 'Production record not found'}), 404