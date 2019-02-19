from user_server.userServer import create_app
import pytest
from flask import url_for
from user_server.api.models import User

@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    app.config.from_object('user_server.config.TestingConfig')

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)
    return app

def test_testing(client):
    response = client.get(url_for('users.index'))
    assert response.status_code == 200
    assert b'hello world' in response.data

def test_add_user(app, client):
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
