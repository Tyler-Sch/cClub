from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User


def test_testing(client):
    response = client.get(url_for('users.index'))
    assert response.status_code == 200
    assert b'hello world' in response.data

def test_add_user(app, client, session):
    response = client.post(
                url_for('users.create_new_user'),
                data={
                        'username': 'potato',
                        'email': 'chip@example.com',
                        'password': 'chips'
                    }
                )
    assert response.status_code == 200
    assert User.query.first().username == 'potato'
    assert User.query.first().email == 'chip@example.com'

    data = response.get_json()
    assert data.get('message') == 'success'
    assert data.get('loggedIn') == True

def add_user_via_endpoint(session, user, email, pw, client):
    response = client.post(
            url_for('users.create_new_user'),
            data={
                'username': user,
                'email': email,
                'password': pw
            }
        )
    return response.get_json()

def test_add_user_already_exists(session, client):
    response1 = client.post(
                            url_for('users.create_new_user'),
                            data={
                                'username': 'hudson',
                                'email': 'fox@example.com',
                                'password': 'chip'
                            }
    )
    assert response1.status_code == 200
    assert len(list(User.query.all())) == 1

    response2 = client.post(
                            url_for('users.create_new_user'),
                            data={
                                'username': 'hudson',
                                'email': 'potato@example.com',
                                'password': 'chipz'
                            }
    )
    assert response2.status_code == 200
    data = response2.get_json()
    assert data['message'] == 'user name already taken'
    assert data['token'] == None


def test_cant_make_user_with_out_username_or_password(session, client):
    response = client.post(
                            url_for('users.create_new_user'),
                            data={
                                'username': '',
                                'email': 'thisshouldntwork@exampl.com',
                                'password': 'blank'
                            }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'There is a field missing'
    assert data['loggedIn'] == False
    assert data['token'] == None

    response = client.post(
                            url_for('users.create_new_user'),
                            data={
                                'username': 'hudsaroni',
                                'email': 'hfs@testtest.com',
                                'password': ''
                            }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'There is a field missing'
    assert data['loggedIn'] == False


def test_can_get_user_id_from_token(session, client):
    response = client.post(
                            url_for('users.create_new_user'),
                            data={
                                'username': 'hudson',
                                'email': 'fox@example.com',
                                'password': 'chip'
                            }
    )
    tok = response.get_json()['token']
    u = User.query.first()
    userid = u.id
    user_through_token = User.verify_auth_token(tok)
    assert userid == user_through_token.id
    assert u.username == user_through_token.username
    assert u.email == user_through_token.email
