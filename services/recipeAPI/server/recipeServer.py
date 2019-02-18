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
    """
    async with app.pool.acquire() as connection:
        recipes = await connection.fetch("""
            SELECT id, name, source, pic_url, url FROM recipes
            WHERE pic_url != 'missing'
            ORDER BY RANDOM() LIMIT $1;
        """, amount)

        return json({'recipes': [dict(i) for i in recipes]})


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
        data = request.args
        # print(data['include'])
        # mod_data = [f'%{i}%' for i in data['include']]
        # print(mod_data)

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

if __name__ == '__main__':
    if os.environ['APP_SETTINGS'] == 'DevelopmentConfig':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)
