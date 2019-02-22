from user_server.api.models import User


from tests.fixture_base import app, db, session


def test_add_user(session):
    new_user = User(
                    username='potato',
                    email='chip@example.com',
                    password='test'
                    )
    session.add(new_user)
    session.commit()
    assert User.query.first().username == 'potato'

def test_add_two_users(session):
    user1 = User(username='hudson', email='hfs@example.com', password='test')
    user2 = User(
                username='stephanie',
                email='scurry@example.com',
                password='test2'
                )
    session.add(user1)
    session.add(user2)
    session.commit()

    assert len(User.query.all()) == 2
    assert User.query.first().username == 'hudson'
    assert User.query.all()[1].username == 'stephanie'

    user3 = User(
                username='tyler',
                email='tyler@fakeemail.com',
                password='test3'
                )
    session.add(user3)
    session.commit()
    assert len(User.query.all()) == 3
    assert User.query.all()[-1].username == 'tyler'
    assert User.query.first().email == 'hfs@example.com'

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'hello world' in response.data

def create_user(session, username='hudson', email='hfs@example.com', pw='test'):
    u = User(username=username, email=email, password=pw)
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
