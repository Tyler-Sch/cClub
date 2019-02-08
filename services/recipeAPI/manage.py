import click
import os
from server.recipeServer import app
import pytest
from server.tests import test_recipe_api

@click.group()
def main():
    pass

@main.command()
def start():
    if os.environ['APP_SETTINGS'] == 'DevelopmentConfig':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)

@main.command()
def test():
    pytest.main(['-x', 'server'])

@main.command()
def test_basic():
    test_recipe_api.test_is_this_thing_on()
    test_recipe_api.test_basic_get()
if __name__ == "__main__":

    main()
