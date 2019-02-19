from flask import Blueprint
from user_server.userServer import db
from flask import jsonify, request
from user_server.api.models import User
users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/')
def index():
    return 'hello world'


@users_blueprint.route('/users/create-new', methods=['POST'])
def create_new_user():
    return jsonify({'test': 'success'})
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password:
        # username or password missing
        return None
    else:
        # check if username exists
        if len(User.query.filter_by(username=username)) == 0:
            u = User(username=username, email=email, password=password)
            db.add(u)
            db.commit()
        else:
            # error for username already exists
            return None

    token = u.generate_auth_token()
    return jsonify({'token': token})
