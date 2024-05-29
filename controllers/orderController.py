from flask import request, jsonify
from schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from services import orderService
from auth import token_auth


@token_auth.login_required
def save():
    try:
        raw_data = request.json
        print(raw_data)
        logged_in_user = token_auth.current_user()
        raw_data['customer_id'] = logged_in_user.id
        print(raw_data)
        order_data = order_schema.load(raw_data)
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

def find_all():
    orders = orderService.find_all()
    return orders_schema.jsonify(orders)


