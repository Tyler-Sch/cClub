import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgres://localhost:5435/recipes_dev'
        '?user=postgres&password=postgres')

    await conn.execute("""
        DROP TABLE IF EXISTS recipes, ingredient_list, ingredients, steps;
    """)
    await conn.execute("""
        CREATE TABLE recipes (
            id serial PRIMARY KEY,
            name text NOT NULL,
            pic_url TEXT,
            url TEXT,
            source TEXT,
            source_meta TEXT,
            date_added timestamp
        );
    """)
    await conn.execute("""
        CREATE TABLE ingredient_list (
            ingredient TEXT UNIQUE,
            id SERIAL PRIMARY KEY
        );
    """)
    await conn.execute("""
        CREATE TABLE ingredients (
            id SERIAL,
            recipe INTEGER NOT NULL,
            ingredient INTEGER NOT NULL,
            original_text TEXT,
            qty TEXT,
            unit TEXT,
            PRIMARY KEY (recipe, id),
            FOREIGN KEY (recipe) REFERENCES recipes (id),
            FOREIGN KEY (ingredient) REFERENCES ingredient_list (id)
        );
    """)
    await conn.execute("""
        CREATE TABLE steps (
            step_num INTEGER,
            recipe INTEGER,
            step text NOT NULL,
            PRIMARY KEY (recipe, step_num),
            FOREIGN KEY (recipe) REFERENCES recipes (id)
        );
    """)
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
