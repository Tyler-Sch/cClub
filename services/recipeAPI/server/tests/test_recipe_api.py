from server.recipeServer import app


def test_is_this_thing_on():
    print('yes this thing is on')

# It would probably good to spin up a test database
# for running these tests

def test_get_recipe():
    request, response = app.test_client.get('/recipes/325')
    assert response.status == 200
    data = response.json
    assert 'ingredients' in data.keys()
    assert 'steps' in data.keys()
    assert 'name' in data.keys()
    assert 'url' in data.keys()

def test_recipes_not_same():
    request1, response1 = app.test_client.get('/recipes/325')
    request2, response2 = app.test_client.get('/recipes/326')
    assert response1.status == 200
    assert response2.status == 200
    assert response1.json['name'] != response2.json['name']

def test_random_recipes():
    # test random recipes dont match
    request, response = app.test_client.get('/recipes/random/2')
    assert response.status == 200
    data = response.json
    assert data['recipes'][0]['name'] != data['recipes'][1]['name']
    assert len(data['recipes']) == 2
    # test variable length works
    request, response = app.test_client.get('/recipes/random/10')
    assert response.status == 200
    data = response.json
    assert len(data['recipes']) == 10

def test_restricted_recipe_search():
    search_item1 = 'chicken'
    search_item2 = 'cheese'
    request, response = app.test_client.get(
        f'/recipes/filter?include={search_item1}&include={search_item2}',
    )
    assert response.status == 200
    data = response.json
    assert len(data) > 1
    for recipe in data:
        request, response2 = app.test_client.get(f'/recipes/{recipe["id"]}')
        recipe_data = response2.json
        search_item1_in_recipe = False
        search_item2_in_recipe = False
        for ingredient in recipe_data['ingredients']:
            if search_item1 in ingredient.lower():
                search_item1_in_recipe = True
            if search_item2 in ingredient.lower():
                search_item2_in_recipe = True
        assert (search_item1_in_recipe and search_item2_in_recipe) == True
