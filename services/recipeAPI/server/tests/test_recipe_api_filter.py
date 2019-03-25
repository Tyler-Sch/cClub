from server.recipeServer import app


def basic_data_assertion(response, num_recipes):
     assert response.status == 200
     data = response.json
     assert len(data['recipes']) == num_recipes
     assert 'id' in data['recipes'][0]
     assert 'name' in data['recipes'][0]
     assert 'url' in data['recipes'][0]
     assert data['recipes'][0] != data['recipes'][1]
     return data

def test_filter_one_correct_element():
    params = {'filter': 100} # filters out dairy
    request, response = app.test_client.get('/recipes/random/5', params=params)
    data = basic_data_assertion(response, 5)
    assert data['filter'] == True
    # dont know if there's a simple way to test the accuracy of the data
    # without writing raw sql queries (Oh how I miss the ORM)
    # a seperately stocked testing database would make a lot of sense
    # for this senario


def test_filter_multiple_correct_element():
    params = [('filter', i) for i in [100,500,700]]
    request, response = app.test_client.get('/recipes/random/5', params=params)
    data = basic_data_assertion(response, 5)
    assert data['filter'] == True


# def test_filter_mixture_incorrect_and_correct():
#     # currently not handling this type of error, maybe I should though???
#     # maybe it should just be logged instead?
#     params = [('filter', i) for i in [100,500,'not good data']]
#     request, response = app.test_client.get('/recipes/random/5', params=params)
#     data = basic_data_assertion(response, 5)
#     assert data['filter'] == True


def test_filter_no_filter():
    request, response = app.test_client.get('/recipes/random/5')
    data = basic_data_assertion(response, 5)
    assert data['filter'] == False

def test_filter_no_elements():
    params = {'filter': ''}
    request, response = app.test_client.get('/recipes/random/5', params=params)
    basic_data_assertion(response, 5)

def test_filter_no_filter_key():
    params = {'nothing':[1,3,4], 'otherthings': 3}
    request, response = app.test_client.get('/recipes/random/5')
    basic_data_assertion(response, 5)
