from flask import Blueprint
from user_server.userServer import db
from flask import jsonify, request, g
from user_server.api.models import User, RecipeList, Recipes
from flask_cors import CORS
from user_server.api.logindecorator import login_required

users_blueprint = Blueprint('users', __name__)
CORS(users_blueprint)


#@users_blueprint.route('/')
#def index():
#    return 'hello world'


@users_blueprint.route('/users/check-login', methods=['GET'])
@login_required
def check_logged_in():
    # if this function fires then it's past the login required decorator
    return jsonify({
        'loggedIn': True,
        'token': g.user.generate_auth_token().decode('utf-8')
        })


@users_blueprint.route('/users/create-new', methods=['POST'])
def create_new_user():
    """
        takes post request with username, password, and email in json format
        if success, adds user to database and returns JWT
    """
    response = {
        'loggedIn': False,
        'token': None,
        'message': 'pending'
    }
    data = request.get_json()
    headings = ['username', 'password', 'email']
    information = {i: data.get(i) for i in headings}

    # check basic integrity of data (length and make sure it exists)
    # there should probably be more checks here.
    for _, info in information.items():
        if len(info) <= 1 or info is None:
            response['message'] = 'There is a field missing'
            return jsonify(response)

    # check if username exists
    if not User.query.filter_by(username=information['username']).first():
        u = User(
                username=information['username'],
                email=information['email'],
                password=information['password'])
        db.session.add(u)
        db.session.commit()
    else:
        # error for username already exists
        response['message'] = 'user name already taken'
        return jsonify(response)

    # info is valid, create token and respond with json
    token = u.generate_auth_token()
    response['loggedIn'] = True
    response['token'] = token.decode('utf-8')
    response['message'] = 'success'
    return jsonify(response)


@users_blueprint.route('/users/login', methods=['POST'])
def login():
    response = {
                'token': None,
                'message': 'Error',
                'loggedIn': False
                }
    data = request.get_json()
    username, password = [data.get(i) for i in ['username', 'password']]
    if username == '' or password == '':
        response['message'] = 'field missing'
        return jsonify(response)
    # Get user
    u = User.query.filter_by(username=username).first()
    # need a check to make sure user exists
    # check password
    if not u.check_password(password):
        response['message'] = 'invalid password'
        return jsonify(response)
    # generate a token
    token = u.generate_auth_token().decode('utf-8')
    response['token'] = token
    response['loggedIn'] = True
    response['message'] = 'logged in success'
    return jsonify(response)


@users_blueprint.route('/test/logindec', methods=['GET'])
@login_required
def loginreq():
    return jsonify({'message': 'working', 'user': g.user.id})


@users_blueprint.route('/users/create-new-recipe-list', methods=['POST'])
@login_required
def create_recipe_list():
    """
        needs json object with following information:
            - list_name (recipeListName)
            - can contain recipes to add in a list of recipes {
                recipe_name, url, pic_url
            }

        are there any other errors I need to account for here? Could add
        general catch for the entire block...
    """
    data = request.get_json()
    user = g.user
    recipe_list_name = data.get('recipeListName')
    new_recipe_list = RecipeList(
        list_creator=user.id,
        list_name=recipe_list_name
    )
    db.session.add(new_recipe_list)
    db.session.commit()
    for recipe in data.get('recipes'):
        new_recipe = Recipes(
                            recipe_name=recipe['name'],
                            recipe_url=recipe['url'],
                            pic_url=recipe['pic_url'],
                            recipe_list_id=new_recipe_list.id,
                            recipe_id=recipe['id'],
                            added_by=user.id
        )
        db.session.add(new_recipe)

    if data.get('recipes'):
        db.session.commit()
    user.recipe_lists.append(new_recipe_list)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': f'{user.username} added {recipe_list_name}',
        'recipeListId': new_recipe_list.id
    })


@users_blueprint.route('/users/get-recipeLists', methods=['GET'])
@login_required
def get_recipe_lists():
    # maybe divide this up so this endpoint doesnt return recipes
    # dont know how big lists would get
    user = g.user
    current_recipe_lists = user.recipe_lists
    recipe_lists = []
    for list_ in current_recipe_lists:
        list_dict = {}
        list_dict['listName'] = list_.list_name
        list_dict['creator'] = list_.list_creator
        list_dict['createdDate'] = list_.created_date
        list_dict['recipes'] = [{
                            'id': r.recipe_id,
                            'name': r.recipe_name,
                            'url': r.recipe_url,
                            'pic_url': r.pic_url
                            } for r in list_.recipes]
        list_dict['users'] = [[u.id, u.username] for u in list_.users]
        list_dict['listId'] = [list_.id]
        recipe_lists.append(list_dict)
    return jsonify({
        'recipeList': recipe_lists
    })


@users_blueprint.route('/users/add-recipes-to-list', methods=['POST'])
@login_required
def add_recipes_to_list():
    """
        request data = {'targetListId': int, 'recipes': [list of recipes]}
        ( each recipe needs following keys: {'name', 'url','pic_url','id'})

        return json {
            'status':string,
            'message':string,
            updatedRecipes:[list of all recipes in list]

            }
    """
    data = request.get_json()
    user = g.user
    target_list_id = data.get('targetListId')
    current_recipe_list = RecipeList.query.filter_by(id=target_list_id).first()
    previous_recipes = [r.recipe_id for r in current_recipe_list.recipes]
    for recipe in data.get('recipes'):
        if recipe['id'] in previous_recipes:
            continue
        else:
            new_recipe = Recipes(
                                recipe_name=recipe['name'],
                                recipe_url=recipe['url'],
                                pic_url=recipe['pic_url'],
                                recipe_list_id=target_list_id,
                                recipe_id=recipe['id'],
                                added_by=user.id
            )
            db.session.add(new_recipe)
    db.session.commit()
    updatedRecipeList = RecipeList.query.filter_by(id=target_list_id).first()
    return jsonify({
        'status': 'success',
        'message': f'{updatedRecipeList.list_name} updated',
        'updatedRecipes': [r.get_dict() for r in updatedRecipeList.recipes]
    })


@users_blueprint.route('/users/remove-recipe', methods=['POST'])
@login_required
def remove_recipe_from_list():
    # what happens when target is not found???
    """
        Input:
            post request with dictionary:
                {
                    'targetList': id,
                    'targetRecipe': id
                }
        Output:
            json response:
                {
                    'status': ['success', 'fail'],
                    'message': 'message about what happened'
                    updatedRecipes: [list of all recipes in target list]
                }
    """

    data = request.get_json()
    target = (data['targetList'], data['targetRecipe'])
    recipe = Recipes.query.get(target)
    recipe_name = recipe.recipe_name

    db.session.delete(recipe)
    db.session.commit()

    updatedRecipeList = RecipeList.query.filter_by(id=target[0]).first()
    response = {
        'status': 'success',
        'message': f'deleted {recipe_name} from target list',
        'updatedRecipes': [r.get_dict() for r in updatedRecipeList.recipes]
    }
    return jsonify(response)
