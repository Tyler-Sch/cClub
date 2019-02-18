import asyncio
import asyncpg
import datetime
import aiofiles
import uvloop
import re
import json
import aiohttp
from asyncio import Queue
import time
import os

"""
    this file should get cleaned up a bit. A cli would be good where you
    specify source file, amount of workers, database address, and
    url for ingredient tagger
"""



async def main(recipe_file, workers, source):
    """
        adds recipes to database created by create_tables.py
        input => recipe file in the form of a dictionary
                with the following keys:
                    - "ingredients" => List of dictionaries
                                        each one contains
                                        ingredient text as a single
                                        key and the text for the
                                        ingredient as a value
                    - "title" => name of the recipe
                    - "url" => url of the recipe
                    - "instructions" => steps to complete the recipe
                => workers is for concurrency
        Output <= None
    """
    recipes = await load_file(recipe_file)
    picture_dict = await load_file('recipes/layer2.json')
    pic_dic = {i['id']:i['images'][0] for i in picture_dict}

    database_address_string = ('postgres://localhost:5435/recipes_test'
                                    '?user=postgres&password=postgres'
                                )
    async with asyncpg.create_pool(database_address_string) as pool:
        q = Queue()
        for recipe in recipes:
            q.put_nowait(recipe)
        async with aiohttp.ClientSession() as sess:
            tasks = [worker(sess, q, i, pool, pic_dic) for i in range(workers)]
            await asyncio.gather(*tasks)




async def worker(sess, q, task_id, connection, picture_dict):
    async with connection.acquire() as con:
        while not q.empty():

            recipe = await q.get()
            name_ = recipe['title']
            url_ = recipe['url']
            date_added_ = datetime.datetime.now()
            source_ = await get_source_from_url(url_)
            try:
                pic_url_ = picture_dict[recipe['id']]['url']
            except KeyError:
                pic_url_ = 'missing'
            id = await create_recipe_row(con, name_, url_, date_added_, source_, pic_url_)
            print(f"{task_id} just added {name_}")
            ing = [i['text'] for i in recipe['ingredients']]
            ingredients = await process_ingredients(ing, sess)
            # have to put these ingredients into database
            if not ingredients:
                continue
            await add_ingredients(ing, ingredients, id, con)
            await add_steps([i['text'] for i in recipe['instructions']], id, con)

async def add_steps(step_list, recipe_id, conn):
    steps = [(i + 1, recipe_id, step_list[i])  for i in range(len(step_list))]
    await conn.copy_records_to_table(
        'steps', records=steps
    )


async def add_ingredients(orig_ing_list, ing_list, recipe_id, conn):
    """
        input =>
            orig_ing_list = orignal list of ingredients to a recipe
            ing_list = POS tagged recipe list format [('word', 'POS')]
            recipe_id = database id of associated recipe
            conn = connection to database
    """

    ing_list = ing_list['ingredients']
    for idx in range(len(ing_list)):
        original_text = orig_ing_list[idx]
        # print(ing_list[idx])
        ingredient = [i[0] for i in ing_list[idx] if i[1] == 'IN']
        ingredient  = " ".join(ingredient)
        qty = " ".join([i[0] for i in ing_list[idx] if i[1] == 'QTY'])
        unit = " ".join([i[0] for i in ing_list[idx] if i[1] == 'UN'])

        ingredient_row = await conn.fetchrow("""
            SELECT * FROM ingredient_list
            WHERE ingredient = $1;
        """, ingredient)

        if not ingredient_row:
            # print('couldnt find ingredient')
            ingredient_id = await conn.fetchval("""
                INSERT INTO ingredient_list(
                    ingredient
                ) VALUES(
                    $1
                ) RETURNING id;
            """, ingredient)
        else:
            ingredient_id = ingredient_row['id']

        await conn.execute("""
            INSERT INTO ingredients(
                recipe,
                ingredient,
                original_text,
                qty,
                unit
            ) VALUES(
                $1, $2, $3, $4, $5
            );
        """, recipe_id, ingredient_id, original_text, qty, unit)


async def load_file(recipeJson):
    async with aiofiles.open(recipeJson, mode='r') as f:
        contents = json.loads(await f.read())
        return contents

async def get_source_from_url(url):
    search = re.search('https?:\/\/w{0,3}\.?(\w+)\.', url)
    if not search:
        return 'unknown'
    return search.group(1)

async def create_recipe_row(conn, name, url, date_added, source, pic_url):

    id = await conn.fetchval("""
        INSERT INTO recipes(
                name,
                pic_url,
                url,
                source,
                date_added
            ) VALUES($1, $2, $3, $4, $5)
            RETURNING id;
    """, name, pic_url, url, source, date_added)
    return id


async def process_ingredients(ingredient_list, session):
    """
        calls outside server using an RNN to tag ingredient parts of speech
        INPUT =>
                - ingredient dictonary, in the form of:
                    {'ingredients': [
                            '1/2 cup of ingredient 1',
                            'pinch of salt',
                            'etc etc etc'
                     ]}

                - session an aiohttp ClientSession connection

        OUTPUT => list of POS tagged recipes
    """
    data = {'ingredients': ingredient_list}
    url = 'http://localhost:5001/ingredients'
    async with session.post(url, data=data) as response:
        try:
            r = await response.json()
        except:
            print(f'error with ingredients for recipe {url}')
            r = None
        return r



if __name__ == '__main__':

    start = time.time()
    for i in os.listdir('recipes'):
        print(f'inserting recipes from {i}')
        if i == 'layer2.json' or i == 'millionRecipesSub.json':
            continue
        else:
            asyncio.get_event_loop().run_until_complete(main(f'recipes/{i}', 5, '1MRecipes'))
    end = time.time()
    print(f'time taken: {end - start}')
