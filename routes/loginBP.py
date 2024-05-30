from flask import Blueprint
from controllers.userController import login

login_blueprint = Blueprint("loginbp", __name__)

login_blueprint.route('/', methods=['POST'])(login)