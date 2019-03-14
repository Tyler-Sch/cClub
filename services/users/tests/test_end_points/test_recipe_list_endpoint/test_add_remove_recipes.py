from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User, RecipeList, Recipes
import json
from tests.testshortcuts import  add_user_via_endpoint, login_user_via_endpoint
from tests.testshortcuts import add_user, add_recipe_list

def test_add_recipe_to_recipe_list(client,session):
    # construct user
    u = add_user(session)
    token = u.generate_auth_token().decode('utf-8')
    recipe_list = add_recipe_list(session, u.id, 'test list')

    # add recipes via endpoint
    recipe_data = [{
        'name': 'potatos',
        'url': 'http://recipes.com/potatoesforeverone',
        'pic_url': 'http://somanypictures.of.potatoes.com',
        'id': 123
    }]

    response = client.post(
        url_for('users.add_recipes_to_list'),
        data=json.dumps({
            'targetListId': recipe_list.id,
            'recipes': recipe_data
        }),
        content_type="application/json",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert len(recipe_list.recipes) == 1

    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == f'{recipe_list.list_name} updated'
    assert len(data['updatedRecipes']) == 1
    assert data['updatedRecipes'][0]['name'] == Recipes.query.first().recipe_name


def test_add_multiple_recipes_to_recipe_list(client,session):
    # construct user
    u = add_user(session)
    token = u.generate_auth_token().decode('utf-8')
    recipe_list = add_recipe_list(session, u.id, 'test list')

    # add recipes via endpoint
    recipe_data = [
        {
            'name': 'potatos',
            'url': 'http://recipes.com/potatoesforeverone',
            'pic_url': 'http://somanypictures.of.potatoes.com',
            'id': 123
        },
        {
            'name': 'potatos with other stfuf',
            'url': 'http://recipes.com/potatoesforeverone',
            'pic_url': 'http://somanypictures.of.potatoes.com',
            'id': 124
        },
        {
            'name': 'stuffed potatos',
            'url': 'http://recipes.com/potatoesforeverone',
            'pic_url': 'http://somanypictures.of.potatoes.com',
            'id': 125
        },
    ]

    response = client.post(
        url_for('users.add_recipes_to_list'),
        data=json.dumps({
            'targetListId': recipe_list.id,
            'recipes': recipe_data
        }),
        content_type="application/json",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert len(recipe_list.recipes) == 3

    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == f'{recipe_list.list_name} updated'
    assert len(data['updatedRecipes']) == 3
    assert data['updatedRecipes'][0]['name'] == Recipes.query.first().recipe_name
