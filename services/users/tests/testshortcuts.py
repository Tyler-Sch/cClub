from flask import url_for
import json
from user_server.api.models import User, RecipeList


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

def add_recipe_list(session, userid, listname):
    r = RecipeList(list_creator=userid, list_name=listname)
    session.add(r)
    session.commit()
    return r
