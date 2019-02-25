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
    headings = ['username', 'password', 'email']
    information = {i: data.get(i) for i in headings}

    # check basic integrity of data (length and make sure it exists)
    # there should probably be more checks here.
    for _, info in information.items():
        if len(info) <= 1 or info is None:
            response['message'] = 'There is a field missing'
            return jsonify(response)

    # check if username exists
    if not User.query.filter_by(username=information['username']).first():
        u = User(
                username=information['username'],
                email=information['email'],
                password=information['password'])
        db.session.add(u)
        db.session.commit()
    else:
        # error for username already exists
        response['message'] = 'user name already taken'
        return jsonify(response)

    # info is valid, create token and respond with json
    token = u.generate_auth_token()
    response['loggedIn'] = True
    response['token'] = token.decode('utf-8')
    response['message'] = 'success'
    return jsonify(response)


@users_blueprint.route('/users/login', methods=['POST'])
def login():
    response = {
                'token': None,
                'message': 'Error',
                'loggedIn': False
                }
    data = request.form
    username, password = [request.form.get(i) for i in ['username', 'password']]
    if username == '' or password == '':
        response['message'] = 'field missing'
        return jsonify(response)
    # Get user
    u = User.query.filter_by(username=username).first()
    # check password
    if not u.check_password(password):
        response['message'] = 'invalid password'
        return jsonify(response)
    # generate a token
    token = u.generate_auth_token().decode('utf-8')
    response['token'] = token
    response['loggedIn'] = True
    response['message'] = 'logged in success'
    return jsonify(response)

@users_blueprint.route('/users/get-recipeLists')
def get_recipe_lists():
    pass
