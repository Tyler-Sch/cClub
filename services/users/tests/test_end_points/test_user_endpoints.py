from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User
import json

def test_testing(client):
    response = client.get(url_for('users.index'))
    assert response.status_code == 200
    assert b'hello world' in response.data

def add_user_via_endpoint(session, user, email, pw, client):
    response = client.post(
            url_for('users.create_new_user'),
            data=json.dumps({
                'username': user,
                'email': email,
                'password': pw
            }),
            content_type='application/json'
        )
    assert response.status_code == 200
    return response.get_json()

def test_add_user(app, client, session):

    args = [session, 'potato', 'chip@example.com', 'chips', client]
    data = add_user_via_endpoint(*args)
    assert User.query.first().username == 'potato'
    assert User.query.first().email == 'chip@example.com'

    assert data.get('message') == 'success'
    assert data.get('loggedIn') == True


def test_add_user_already_exists(session, client):
    args = [session, 'hudson', 'fox@example.com', 'chip', client]
    response1 = add_user_via_endpoint(*args)
    assert len(list(User.query.all())) == 1

    data = add_user_via_endpoint(*args)
    assert data['message'] == 'user name already taken'
    assert data['token'] == None


def test_cant_make_user_with_out_username_or_password(session, client):
    args = [session, '', 'thishouldnotwork@stuff.com', 'blank', client]
    data = add_user_via_endpoint(*args)
    assert data['message'] == 'There is a field missing'
    assert data['loggedIn'] == False
    assert data['token'] == None

    args = [session, 'hudsaphone', 'hfs@test.com', '', client]
    data = add_user_via_endpoint(*args)
    assert data['message'] == 'There is a field missing'
    assert data['loggedIn'] == False


def test_can_get_user_id_from_token(session, client):
    args = [session, 'hudson', 'fox@example.com', 'chip', client]
    data = add_user_via_endpoint(*args)
    tok = data['token']
    u = User.query.first()
    userid = u.id
    user_through_token = User.verify_auth_token(tok)
    assert userid == user_through_token.id
    assert u.username == user_through_token.username
    assert u.email == user_through_token.email


def test_password_gets_hashed_via_endpoint(session, client):
    args = [session, 'hudson', 'potato@example.com', 'chips', client]
    data = add_user_via_endpoint(*args)
    u = User.query.filter_by(username='hudson')[0]
    password_hash = u.password_hash
    assert 'chips' != password_hash
    assert u.email == 'potato@example.com'
    assert u.check_password('chips') == True

def add_user(session, username='hudson',
             email='chip@example.com', password='chips'):
    u = User(username=username, email=email, password=password)
    session.add(u)
    session.commit()
    return u


def login_user_via_endpoint(client, username, password):
    response = client.post(
        url_for('users.login'),
        data=json.dumps({
            'username': username,
            'password': password
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    return response.get_json()

def test_user_login(session, client):
    # DONT FORGET TO WRITE THESE TESTS
    u = add_user(session)
    assert len(list(User.query.all())) == 1

    data = login_user_via_endpoint(client, 'hudson', 'chips')
    assert 'logged in success' in data['message']
    assert data['loggedIn']
    token = data['token']
    assert User.verify_auth_token(token) == u

def test_user_login_no_password_and_no_username(session, client):
    u = add_user(session)

    # test no username
    data = login_user_via_endpoint(client, '', 'chips')
    assert 'field missing' in data['message']
    assert data['token'] is None

    # test no password
    data = login_user_via_endpoint(client, 'hudson', '')
    assert 'field missing' in data['message']
    assert data['token'] is None

def test_user_cannot_login_with_wrong_pword(session, client):
    u = add_user(session)
    data = login_user_via_endpoint(client, 'hudson', 'wrongpassword')
    assert 'invalid password' in data['message']
    assert not data['loggedIn']
    assert data['token'] is None
