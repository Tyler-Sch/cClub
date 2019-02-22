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
