from flask import Blueprint
from user_server.userServer import db
from flask import jsonify
users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/')
def index():
    return 'hello world'


@users_blueprint.route('/users/create-new', methods=['POST'])
def create_new_user():
    data = request.get_json()
    return jsonify(data)
