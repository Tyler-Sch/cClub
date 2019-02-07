from sanic import Sanic
from sanic.response import json, html
import os
import asyncio
import uvloop
from asyncpg import connect, create_pool
import config


app = Sanic(__name__)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool = await create_pool(dsn=os.environ.get('DATABASE_URI'), loop=loop)



@app.route('/recipes/<id:int>')
async def getRecipe(request, id):
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
    async with app.pool.acquire() as connection:
        recipes = await connection.fetch("""
            SELECT id, name, source, pic_url, url FROM recipes
            ORDER BY RANDOM() LIMIT $1;
        """, amount)

        return json({'recipes': [dict(i) for i in recipes]})


@app.get('/recipes/filter')
async def get_recipe_restricted(request):
    async with app.pool.acquire() as connection:
        data = request.args
        include_ingredients = await connection.fetch("""
            SELECT id from ingredient_list
            WHERE ingredient = any($1);
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

    return json(include_set)

if __name__ == '__main__':
    if os.environ['APP_SETTINGS'] == 'DevelopmentConfig':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)
