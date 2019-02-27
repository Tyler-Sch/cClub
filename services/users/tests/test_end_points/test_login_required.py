from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User
import json
from tests.testshortcuts import  add_user_via_endpoint, login_user_via_endpoint
from tests.testshortcuts import add_user
import time

def post_to_test_login_decorator(client, header_dict):
    response = client.get(
        url_for('users.loginreq'),
        data=json.dumps({}),
        content_type='application/json',
        headers=header_dict
    )
    return response


def test_login_required_wrapper_not_authorized(client):
    response = post_to_test_login_decorator(client, {})
    data = response.get_json()
    assert 'unauthorized' in data.get('status')
    assert response.status_code == 401


def test_login_required_bad_signature(client, session):
    user_json = add_user_via_endpoint(
                                    session, 'hudson',
                                    'fox@test.com', 'adfa', client)
    token = user_json.get('token')
    assert token is not None
    response = post_to_test_login_decorator(
                                        client,
                                        dict(Authorization=token + 'a')
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data.get('message') == 'please login again'
    assert data.get('status') == 'invalid token'


def test_logindecorator_expired_token(client, session):
    u = add_user(session)
    token = u.generate_auth_token(1)
    assert token is not None
    time.sleep(2)

    response = post_to_test_login_decorator(client, dict(Authorization=token))
    assert response.status_code == 401
    data = response.get_json()
    assert data.get('message') == 'please login again'
    assert data.get('status') == 'invalid token'

def test_logindecorator_token_valid(client, session):
    user_json = add_user_via_endpoint(
                                    session, 'hudson',
                                    'fox@test.com', 'adfa', client)
    token = user_json.get('token')
    user_id = User.query.first().id
    assert token is not None

    response = post_to_test_login_decorator(client, dict(Authorization=token))
    assert response.status_code == 200
    data = response.get_json()
    assert data.get('message') == 'working'
    assert data.get('user') == user_id
