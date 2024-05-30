from flask import request, jsonify
from schemas.userSchema import users_schema, user_schema
from services import userService
from marshmallow import ValidationError
from caching import cache


def save():
    try:
        # Validate and deserialize the request data
        user_data = user_schema.load(request.json)
        user_save = userService.save(user_data)
        return user_schema.jsonify(user_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# @cache.cached(timeout=60)
def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    users = userService.find_all(page, per_page)
    return users_schema.jsonify(users), 200


def get_token():
    try:
        user_data = user_schema.load(request.json)
        token = userService.get_token(user_data['username'], user_data['password'])
        if token:
            resp = {
                "status": "success",
                "message": "You have successfully authenticated yourself",
                "token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401 # 401 - HTTP Status - Unauthorized
    except ValidationError as err:
        return jsonify(err.messages), 400


def get_user(user_id):
    user = userService.get_user(user_id)
    if user:
        return user_schema.jsonify(user)
    else:
        resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
        return jsonify({'error': f'A user with ID {user_id} does not exist'}), 404
    
def login():
    try:
        user_data = user_schema.load(request.json)
        token = userService.login(user_data['username'], user_data['password'])
        if token:
            resp = {
                "status": "success",
                "message": "You have successfully logged in",
                "token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401
    except ValidationError as err:
        return jsonify(err.messages), 400