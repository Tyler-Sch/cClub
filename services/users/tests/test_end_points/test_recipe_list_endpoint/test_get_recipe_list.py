from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User, RecipeList, Recipes
import json
from tests.testshortcuts import  add_user_via_endpoint, login_user_via_endpoint
from tests.testshortcuts import add_user


def add_recipe_list(session, user, list_name):
    recipe_list = RecipeList(list_creator=user.id, list_name=list_name)
    session.add(recipe_list)
    user.recipe_lists.append(recipe_list)
    session.commit()
    return recipe_list

def test_get_recipe_list(session, client):
    user = add_user(session)
    token = user.generate_auth_token()
    recipe_list = add_recipe_list(session, user, 'test list')

    assert RecipeList.query.count() == 1
    response = client.get(
                    url_for('users.get_recipe_lists'),
                    headers={'Authorization': token}
    )

    assert response.status_code == 200

    data = response.get_json()['recipeList'][0]
    assert data['listName'] == 'test list'
    assert data['creator'] == user.id
    assert data['recipes'] == []

def test_user_can_get_multiple_lists(session, client):
    user = add_user(session)
    token = user.generate_auth_token()
    recipe_list1 = add_recipe_list(session, user, 'test list 1')
    recipe_list2 = add_recipe_list(session, user, 'test list 2')

    assert RecipeList.query.count() == 2

    response = client.get(
                        url_for('users.get_recipe_lists'),
                        headers={'Authorization': token}
    )
    assert response.status_code == 200

    data = response.get_json()['recipeList']
    for list_ in data:
        assert list_['creator'] == user.id
        assert 'test list' in list_['listName']
        assert len(list_['recipes']) == 0

def test_multipe_users_can_share_recipe_list(session, client):
    user1 = add_user(session)
    user2 = add_user(session, 'potato', 'chip@test.com', 'asdfa')
    recipe_list = add_recipe_list(session, user1, 'test list')
    user2.recipe_lists.append(recipe_list)
    assert RecipeList.query.count() == 1
    assert user1 in RecipeList.query.first().users
    assert user2 in RecipeList.query.first().users

    token_u1 = user1.generate_auth_token()
    response_u1 = client.get(
                            url_for('users.get_recipe_lists'),
                            headers={'Authorization': token_u1}
    )
    assert response_u1 == 200
    data = response_u1.get_json()['recipeList'][0]
    assert data['listName'] == 'test list'

    token_u2 = user2.generate_auth_token()
    response_u2 = client.get(
                            url_for('users.get_recipe_lists'),
                            headers={'Authorization': token_u2}
    )
    assert response_u2 == 200
    data = response_u1.get_json()['recipeList'][0]
    assert data['listName'] == 'test list'
    assert len(data['users']) == 2
    assert [user1.id, user1.username] in data['users']
    assert [user2.id, user2.username] in data['users']
