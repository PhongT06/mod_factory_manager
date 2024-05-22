from flask import Blueprint
from controllers.employeeController import save, find_all, find_by_id

employee_blueprint = Blueprint('employee_bp', __name__)

employee_blueprint.route('/', methods=['POST'])(save)
employee_blueprint.route('/', methods=['GET'])(find_all)
employee_blueprint.route('/<int:employee_id>', methods=['GET'])(find_by_id)