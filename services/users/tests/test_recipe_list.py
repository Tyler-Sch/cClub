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


def add_recipe_list(session, userid, listname):
    r = RecipeList(list_creator=userid, list_name=listname)
    session.add(r)
    session.commit()
    return r


def test_create_recipe_list(session):
    u = create_user(session)
    r = add_recipe_list(session, u.id, 'test recipe list')

    assert RecipeList.query.first().list_name == 'test recipe list'
    assert len(list(RecipeList.query.all())) == 1


def add_recipe_to_recipe_list(session, list_id, recipe_id, user_id):
    recipe = Recipes(list_id, recipe_id, user_id)
    session.add(recipe)
    session.commit()
    return recipe


def test_add_recipes_to_recipe_list(session):
    u = create_user(session)
    r = add_recipe_list(session, u.id, 'test recipe list')
    assert RecipeList.query.first() == r

    recipe1 = add_recipe_to_recipe_list(session, r.id, 123, u.id)

    assert Recipes.query.first() == recipe1
    recipe2 = add_recipe_to_recipe_list(session, r.id, 124, u.id)

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

def test_multiple_users_can_add_to_same_recipelist(session):
    u1 = create_user(session)
    u2 = create_user(session, 'potato', 'spud@example.com', 'adfasfsa')
    assert len(list(User.query.all())) == 2
    # add recipe list, created by u1
    r = add_recipe_list(session, u1.id, 'testing more')
    u1.recipe_lists.append(r)
    u2.recipe_lists.append(r)
    assert u1 in r.users
    assert u2 in r.users
    # add recipes by both users
    recipe1 = add_recipe_to_recipe_list(session, r.id, 1, u1.id)
    assert recipe1 in r.recipes
    assert len(r.recipes) == 1

    recipe2 = add_recipe_to_recipe_list(session, r.id, 2, u2.id)
    assert recipe2 in r.recipes
    assert len(r.recipes) == 2
    assert recipe2.added_by == u2.id

def test_multiple_users_can_add_same_recipes_to_different_list(session):
    u1 = create_user(session)
    u2 = create_user(session, 'potato', 'chipz@test.com', 'adfas')
    r1 = add_recipe_list(session, u1.id, 'user1 recipe list')
    u1.recipe_lists.append(r1)
    r2 = add_recipe_list(session, u2.id, 'user2 recipe list')
    u2.recipe_lists.append(r2)

    recipe1 = add_recipe_to_recipe_list(session, r1.id, 123, u1.id)
    recipe2 = add_recipe_to_recipe_list(session, r2.id, 123, u2.id)

    assert len(list(Recipes.query.all())) == 2
    assert recipe1 in r1.recipes
    assert recipe2 in r2.recipes
    assert recipe2 not in r1.recipes
    assert recipe1 not in r2.recipes

def test_user_can_add_same_recipe_to_different_lists(session):
    u = create_user(session)
    r = add_recipe_list(session, u.id, 'recipe list')
    u.recipe_lists.append(r)
    r2 = add_recipe_list(session, u.id, 'recipe list2')
    u.recipe_lists.append(r2)

    assert len(u.recipe_lists) == 2
    assert r in u.recipe_lists
    assert r2 in u.recipe_lists

    recipe = add_recipe_to_recipe_list(session, r.id, 123, u.id)
    recipe_same = add_recipe_to_recipe_list(session, r2.id, 123, u.id)

    assert len(list(Recipes.query.all())) == 2
    assert len(r.recipes) == 1
    assert len(r2.recipes) == 1
    assert r.recipes[0].recipe_id == r2.recipes[0].recipe_id
