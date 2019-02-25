from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User, RecipeList, Recipes


def create_user(
                session, username="hudson",
                email='potato@example.com', password='hfs'
                ):
    u = User(username=username, email=email, password=password)
    session.add(u)
    session.commit()
    return u


def test_create_recipe_list(session):
    u = create_user(session)
    r = RecipeList(list_creator=u.id, list_name='test recipe list')
    session.add(r)
    session.commit()

    assert RecipeList.query.first().list_name == 'test recipe list'
    assert len(list(RecipeList.query.all())) == 1

def add_recipe_list(session, userid, listname):
    r = RecipeList(list_creator=userid, list_name=listname)
    session.add(r)
    session.commit()
    return r

def test_add_recipes_to_recipe_list(session):
    u = create_user(session)
    r = add_recipe_list(session, u.id, 'test recipe list')
    assert RecipeList.query.first() == r

    recipe1 = Recipes(r.id, 123)
    session.add(recipe1)
    session.commit()

    assert Recipes.query.first() == recipe1
    recipe2 = Recipes(r.id, 124)
    session.add(recipe2)
    session.commit()

    assert len(list(Recipes.query.all())) == 2
    # make sure recipes can be retrieved through RecipeList
    recipe_list = RecipeList.query.first().recipes
    assert len(recipe_list) == 2
    assert recipe_list[0].recipe_id == 123
    assert recipe_list[1].recipe_id == 124

def test_verify_recall_recipe_list_from_user(session):
    u = create_user(session)
    r = add_recipe_list(session, u.id, 'test_recipe list')
    r2 = add_recipe_list(session, u.id, 'test2 recipe list')
    u.recipe_lists.append(r)
    u.recipe_lists.append(r2)
    assert r.users[0] == u

    recipelist_list = u.recipe_lists
    assert r in recipelist_list
    assert r2 in recipelist_list
    assert len(recipelist_list) == 2

def test_multiple_users_can_share_recipe_list(session):
    u1 = create_user(session)
    u2 = create_user(session, 'potato', 'spud@example.com', 'afaaf')
    assert len(list(User.query.all())) == 2

    r = add_recipe_list(session, u1.id, 'test two can share')
    u1.recipe_lists.append(r)
    u2.recipe_lists.append(r)

    assert r in u1.recipe_lists
    assert r in u2.recipe_lists

    assert r.users[0] == u1
    assert r.users[1] == u2
    assert len(r.users) == 2
