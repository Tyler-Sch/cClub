from sanic import Sanic
from sanic.response import json, html
import os
import asyncio
import uvloop
from asyncpg import connect, create_pool
from sanic_cors import CORS


app = Sanic(__name__)

# Currently the various configurations are useless.
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

CORS(app)


@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool = await create_pool(dsn=os.environ.get('DATABASE_URI'), loop=loop)


@app.route('/recipes/<id:int>')
async def getRecipe(request, id):
    """
        returns full recipe in json.
    """

    async with app.pool.acquire() as connection:
        recipe_info = await connection.fetchrow("""
            SELECT * FROM recipes WHERE id = $1;
        """, id)
        results = dict(recipe_info)
        ingredients = await connection.fetch("""
            SELECT original_text FROM ingredients
            WHERE recipe = $1;
        """, id)
        results['ingredients'] = [i['original_text'] for i in ingredients]
        steps = await connection.fetch("""
            SELECT * FROM steps WHERE recipe = $1;
        """, id)
        results['steps'] = [i['step'] for i in steps]
    return json(results)

@app.route('/recipes/random/<amount:int>')
async def get_random_recipes(request, amount):
    """
        get random n recipes. n being amount in the request
        If there is a query string with 'filter' in key data included:
            app will filter OUT food elements of those types

        FILTER NUM MAP {
            100: Dairy and Eggs,
            400: fats and oils,
            500: poultry products,
            700: sausage and lunch meat,
            800: breakfast cereals
            900: Fruits and fruit juices,
            1000: Pork products,
            1100: vegetables,
            1200: Nuts and seeds,
            1300: Beef products,
            1400: Beverages,
            1500: Finfish and shellfishself,
            1600: Legumes,
            1700: lamb, veal, and game,
            2000: Cereal Grains and Pasta,
        }
    """
    async with app.pool.acquire() as connection:
        if not request.args.get('filter'):
            filter = False
            recipes = await connection.fetch("""
                SELECT id, name, source, pic_url, url FROM recipes
                WHERE pic_url != 'missing'
                ORDER BY RANDOM() LIMIT $1;
            """, amount)

        else:
            # should test for validity of data
            filter = True
            data = request.args
            filter_args = [int(i) for i in data['filter']]
            query = """
                SELECT id, name, source, pic_url, url
                FROM recipes r
                WHERE r.id not in (
                    SELECT DISTINCT i.recipe
                    FROM ingredients i INNER JOIN ingredient_information ii
                    ON (i.ingredient = ii.id)
                    WHERE ii.fdgroup_num = ANY($1)
                )
                ORDER BY RANDOM() limit $2
            """
            recipes = await connection.fetch(query, filter_args, amount)

        return json({'recipes': [dict(i) for i in recipes], 'filter': filter})


@app.get('/recipes/filter')
async def get_recipe_restricted(request):

    """
        simple search at the moment. Only include currently worksself.
        Client send request with query string:
            ?include=ingredient1&include=ingredient2


    """
    # might make sense to have this use a looser search
    # maybe using matching% Otherwise it might be way
    # too constrictive
    # COULD ADD A FLAG
    async with app.pool.acquire() as connection:
        if not request.args:
            return json({'status': 'error', 'message': 'no query string'})
        data = request.args

        include_ingredients = await connection.fetch("""
            SELECT id from ingredient_list
            WHERE ingredient = any ($1);
        """, data['include'])
        include_strings = []
        for record in include_ingredients:
            query = f"""SELECT recipe FROM ingredients
            WHERE ingredient = {record['id']}
            """
            include_strings.append(query)
        include_set = await connection.fetch(
            " INTERSECT ".join(include_strings)
        )
        results = await connection.fetch("""
            SELECT id, name, url, pic_url, source
            FROM recipes
            WHERE id = any($1)
            ORDER BY random() LIMIT 300;
        """, include_set)

    return json([dict(i) for i in results])
    # return json(include_set)


@app.get('/recipes/ingredients')
async def fetchRecipes(request):
    data = request.args

    query = """
        SELECT r.id, r.name, i.original_text, il.ingredient, ii.fdgroup_name
        FROM (((ingredients i INNER JOIN recipes r ON i.recipe = r.id )
        INNER JOIN ingredient_list il ON i.ingredient = il.id)
        INNER JOIN ingredient_information ii ON i.ingredient = ii.id)
        WHERE r.id = ANY($1)
    """

    # return json({'data': data, 'recipe_ids': recipe_ids})
    if data.get('recipes') is None or len(data.get('recipes')) == 0:
        return json({
            'status': 'error',
            'message': 'no recipe ids'
        })
    recipe_ids = data['recipes']
    async with app.pool.acquire() as connection:
        results = await connection.fetch(query, [int(i) for i in recipe_ids])

    return json([dict(i) for i in results])


if __name__ == '__main__':
    if os.environ['APP_SETTINGS'] == 'DevelopmentConfig':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)
