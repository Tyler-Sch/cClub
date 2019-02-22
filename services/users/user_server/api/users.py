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
    response = {
        'loggedIn': False,
        'token': None,
        'message': 'pending'
    }
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if username is not None and password is not None and email is not None:
        # check if username exists
        if not User.query.filter_by(username=username).first():
            u = User(username=username, email=email, password=password)
            db.session.add(u)
            db.session.commit()
        else:
            # error for username already exists
            response['message'] = 'user name already taken'
            return jsonify(response)
    else:
        reponse['message'] = 'There is a field missing'
        return jsonify(response)

    token = u.generate_auth_token()
    response['loggedIn'] = True
    response['token'] = token.decode('utf-8')
    response['message'] = 'success'
    return jsonify(response)
