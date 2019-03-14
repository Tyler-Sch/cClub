from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User, RecipeList, Recipes
import json
from tests.testshortcuts import  add_user_via_endpoint, login_user_via_endpoint
from tests.testshortcuts import add_user

def test_create_recipe_list_endpoint(client, session):
    create_data = [session, 'hudson', 'fox@test.com','asdfad', client]
    user_json = add_user_via_endpoint(*create_data)
    token = user_json.get('token')
    user_id = User.query.first().id

    response = client.post(
                    url_for('users.create_recipe_list'),
                    data=json.dumps({
                        'recipeListName': 'test list',
                        'recipes': []
                    }),
                    content_type='application/json',
                    headers={'Authorization': token}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data.get('status') == 'success'
    assert data.get('message') == 'hudson added test list'
    recipe_list = RecipeList.query.first()
    assert recipe_list.list_name == 'test list'
    assert recipe_list.list_creator == user_id
    assert recipe_list.id == data.get('recipeListId')

def test_create_recipe_list_with_recipes(client,session):
    create_data = [session, 'hudson', 'fox@test.com','asdfad', client]
    user_json = add_user_via_endpoint(*create_data)
    token = user_json.get('token')
    user_id = User.query.first().id
    recipeList = [
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 123
        },
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 134
        },
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 145
        },
    ]

    response = client.post(
                    url_for('users.create_recipe_list'),
                    data=json.dumps({
                        'recipeListName': 'test list',
                        'recipes': recipeList
                    }),
                    content_type='application/json',
                    headers={'Authorization': token}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data.get('status') == 'success'
    assert data.get('message') == 'hudson added test list'
    recipe_list = RecipeList.query.first()
    assert recipe_list.list_name == 'test list'
    assert recipe_list.list_creator == user_id
    assert recipe_list.id == data.get('recipeListId')
    assert len(list(Recipes.query.all())) == 3
    assert Recipes.query.first().added_by == user_id
    assert Recipes.query.first().recipe_id == 123


def test_create_recipe_endpoint_no_token(client, session):
    create_data = [session, 'hudson', 'fox@test.com','asdfad', client]
    user_json = add_user_via_endpoint(*create_data)
    token = user_json.get('token')
    user_id = User.query.first().id

    recipeList = [
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 123
        },
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 134
        },
        {
            'name': 'recipe1',
            'url': 'http://blah.com/thisandthat',
            'pic_url': 'http://fakeurl.com/recipe234',
            'id': 145
        },
    ]

    response = client.post(
                    url_for('users.create_recipe_list'),
                    data=json.dumps({
                        'recipeListName': 'test list',
                        'recipes': recipeList
                    }),
                    content_type='application/json',
                    headers={}
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data.get('status') == 'unauthorized'
    assert data.get('message') == 'must be logged in'
