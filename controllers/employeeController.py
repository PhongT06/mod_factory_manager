from flask import request, jsonify
from schemas.employeeSchema import employee_schema, employees_schema
from services import employeeService
from marshmallow import ValidationError

def save():
    try:
        employee_data = employee_schema.load(request.json)
        employee_save = employeeService.save(employee_data)
        return employee_schema.jsonify(employee_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

def find_all():
    employees = employeeService.find_all()
    return employees_schema.jsonify(employees), 200

def find_by_id(employee_id):
    employee = employeeService.find_by_id(employee_id)
    if employee:
        return employee_schema.jsonify(employee), 200
    else:
        return jsonify({'error': 'Employee not found'}), 404