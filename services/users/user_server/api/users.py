from flask import Blueprint


users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/')
def index():
    return 'hello world'

@users_blueprint.route('/users/createuser', methods=['POST'])
