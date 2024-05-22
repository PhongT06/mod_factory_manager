from flask import request, jsonify
from schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from services import orderService



def save():
    try:
        order_data = order_schema.load(request.json)
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    orders = orderService.find_all(page, per_page)
    return orders_schema.jsonify(orders)
