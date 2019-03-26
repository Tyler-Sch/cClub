from server.recipeServer import app


def test_get_ingredients():
    params = {'recipes': 456}
    request, response = app.test_client.get(
        '/recipes/ingredients',
        params=params
    )
    assert response.status == 200
    data = response.json

    keys = data[0].keys()
    assert data[0]['id'] == 456
    assert 'name' in keys
    assert 'original_text' in keys
    assert 'fdgroup_name' in keys


def test_get_ingredients_multiple_recipes():
    params = [('recipes', 14), ('recipes', 156)]
    request, response = app.test_client.get(
        '/recipes/ingredients',
        params=params
    )

    assert response.status == 200
    data = response.json
    assert data[0]['id'] == 14
    assert data[-1]['id'] == 156

def test_get_ingredients_no_recipes_passed():
    params = {'recipes': ''}
    request, response = app.test_client.get(
        '/recipes/ingredients',
        params=params
    )
    assert response.status == 200
    data = response.json

    assert 'error' in data['status']
    assert 'no recipe ids' in data['message']

def test_get_ingredients_invalid_key():
    params = {'thisdoesntwork': 342}
    request, response = app.test_client.get(
        '/recipes/ingredients',
        params=params
    )
    assert response.status == 200
    data = response.json

    assert 'error' in data['status']
    assert 'no recipe ids' in data['message']
