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
    assert data.get('message') == 'test list added to hudson list'
    assert RecipeList.query.first().list_name == 'test list'
    assert RecipeList.query.first().list_creator == user_id

def test_create_recipe_list_with_recipes(client,session):
    create_data = [session, 'hudson', 'fox@test.com','asdfad', client]
    user_json = add_user_via_endpoint(*create_data)
    token = user_json.get('token')
    user_id = User.query.first().id

    response = client.post(
                    url_for('users.create_recipe_list'),
                    data=json.dumps({
                        'recipeListName': 'test list',
                        'recipes': [123, 134, 145]
                    }),
                    content_type='application/json',
                    headers={'Authorization': token}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data.get('status') == 'success'
    assert data.get('message') == 'test list added to hudson list'
    assert RecipeList.query.first().list_name == 'test list'
    assert RecipeList.query.first().list_creator == user_id
    assert len(list(Recipes.query.all())) == 3
    assert Recipes.query.first().added_by == user_id
    assert Recipes.query.first().recipe_id == 123
