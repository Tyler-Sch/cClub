from user_server.userServer import create_app
from user_server.api.models import User
from user_server.userServer import db as _db
import sqlalchemy
import os
import pytest

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

@pytest.fixture(scope='session')
def db(app, request):

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()
    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()
    request.addfinalizer(teardown)
    return session

def test_add_user(session):
    new_user = User(username='potato', email='chip@example.com')
    session.add(new_user)
    session.commit()
    assert User.query.first().username == 'potato'

def test_add_two_users(session):
    user1 = User(username='hudson', email='hfs@example.com')
    user2 = User(username='stephanie', email='scurry@example.com')
    session.add(user1)
    session.add(user2)
    session.commit()

    assert len(User.query.all()) == 2
    assert User.query.first().username == 'hudson'
    assert User.query.all()[1].username == 'stephanie'

    user3 = User(username='tyler', email='tyler@fakeemail.com')
    session.add(user3)
    session.commit()
    assert len(User.query.all()) == 3
    assert User.query.all()[-1].username == 'tyler'
    assert User.query.first().email == 'hfs@example.com'

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'hello world' in response.data

def create_user(session, username='hudson', email='hfs@example.com'):
    u = User(username=username, email=email)
    session.add(u)
    session.commit()
    return u

def test_user_login_token(session):
    u = create_user(session)
    test_id = u.id
    assert len(User.query.all()) == 1
    test_hash = u.generate_auth_token()
    assert '1' != test_hash
    get_id_from_hash = User.verify_auth_token(test_hash)
    assert get_id_from_hash != None
    assert get_id_from_hash.id == test_id

def test_two_users_dont_have_same_hash(session):
    pass
